# Standard Library
import csv
import logging
import time
from io import BytesIO

# Third-Party
import pydf
from auth0.v3.authentication import GetToken
from auth0.v3.exceptions import Auth0Error
from auth0.v3.management import Auth0
from django_rq import job
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from PyPDF2 import PdfFileMerger
from django.core.mail import EmailMessage
from django_rq import job
from django.db.models import Avg
from django.db.models import Q
from django.db.models import Sum
from django.db.models import Max

# Django
from django.apps import apps
from django.conf import settings
from django.core.cache import cache
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.validators import ValidationError
from django.core.validators import validate_email
from django.db.models import Count
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.utils.timezone import localdate

log = logging.getLogger(__name__)

# Utility
def build_email(template, context, subject, to, cc=[], bcc=[], attachments=[]):
    # Clean as necessary
    # Remove commas
    to = [x.replace(",", "") for x in to]
    cc = [x.replace(",", "") for x in cc]
    bcc = [x.replace(",", "") for x in bcc]

    # Remove duplicate emails, keeping only the first
    full = []
    clean_to = []
    clean_cc = []
    clean_bcc = []
    for address in to:
        if not address.partition("<")[2].partition(">")[0] in full:
            clean_to.append(address)
        full.append(address.partition("<")[2].partition(">")[0])
    for address in cc:
        if not address.partition("<")[2].partition(">")[0] in full:
            clean_cc.append(address)
        full.append(address.partition("<")[2].partition(">")[0])
    for address in bcc:
        if not address.partition("<")[2].partition(">")[0] in full:
            clean_bcc.append(address)
        full.append(address.partition("<")[2].partition(">")[0])

    body = render_to_string(template, context)
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email='Barberscore <admin@barberscore.com>',
        to=clean_to,
        cc=clean_cc,
        bcc=clean_bcc,
    )
    for attachment in attachments:
        with attachment[1].open() as f:
            email.attach(attachment[0], f.read(), attachment[2])
    return email


def check_account(account):
    User = apps.get_model('api.user')
    try:
        user = User.objects.get(
            username=account[0],
        )
    except User.DoesNotExist:
        # Delete orphan
        auth0 = get_auth0()
        auth0.users.delete(account[0])
        return "Deleted: {0}".format(account[0])
    # Delete accounts with no valid email
    if not user.person.email:
        auth0 = get_auth0()
        auth0.users.delete(account[0])
        return "Deleted: {0}".format(account[0])
    # Ensure sync
    check = any([
        user.person.email != account[1],
        user.person.common_name != account[2],
    ])
    if check:
        auth0 = get_auth0()
        email = user.person.email.lower()
        name = user.person.common_name
        payload = {
            'email': email,
            'email_verified': True,
            'app_metadata': {
                'name': name,
            }
        }
        auth0.users.update(user.username, payload)
        return "Updated: {0}".format(account[0])
    return "Skipped: {0}".format(account[0])


def create_or_update_account_from_person(person):
    user = getattr(person, 'user', None)
    if user:
        if user.is_staff:
            raise ValueError('Staff should not have accounts')
        auth0 = get_auth0()
        email = person.email.lower()
        name = person.common_name
        payload = {
            'email': email,
            'email_verified': True,
            'app_metadata': {
                'name': name,
            }
        }
        account = auth0.users.update(user.username, payload)
        created = False
    else:
        auth0 = get_auth0()
        password = get_random_string()
        email = person.email.lower()
        name = person.common_name
        payload = {
            'connection': 'Default',
            'email': email,
            'email_verified': True,
            'password': password,
            'app_metadata': {
                'name': name,
            }
        }
        account = auth0.users.create(payload)
        created = True
    return account, created


def delete_account_from_person(person):
    user = getattr(person, 'user', None)
    if not user:
        return "No user for person"
    auth0 = get_auth0()
    username = user.username
    # Delete Auth0
    auth0.users.delete(username)
    return "Deleted: {0}".format(username)


def person_post_save_handler(person):
    User = apps.get_model('api.user')
    if person.email:
        account, created = create_or_update_account_from_person(person)
        if created:
            User.objects.create_user(
                username=account['user_id'],
                person=person,
            )
    else:
        delete_account_from_person(person)
    return


def user_post_delete_handler(user):
    if user.is_staff:
        return
    auth0 = get_auth0()
    auth0.users.delete(user.username)
    return "Deleted: {0}".format(user.username)


def send_complete_email_from_appearance(appearance):
    Appearance = apps.get_model('api.appearance')
    Panelist = apps.get_model('api.panelist')
    Score = apps.get_model('api.score')

    # Context
    group = appearance.group
    stats = Score.objects.select_related(
        'song__appearance__group',
        'song__appearance__round__session',
        'song__appearance__round',
        'panelist',
    ).filter(
        song__appearance__group=appearance.group,
        song__appearance__round__session=appearance.round.session,
        panelist__kind=Panelist.KIND.official,
    ).aggregate(
        max=Max(
            'song__appearance__round__num',
        ),
        tot_points=Sum(
            'points',
        ),
        mus_points=Sum(
            'points',
            filter=Q(
                panelist__category=Panelist.CATEGORY.music,
            )
        ),
        per_points=Sum(
            'points',
            filter=Q(
                panelist__category=Panelist.CATEGORY.performance,
            )
        ),
        sng_points=Sum(
            'points',
            filter=Q(
                panelist__category=Panelist.CATEGORY.singing,
            )
        ),
        tot_score=Avg(
            'points',
        ),
        mus_score=Avg(
            'points',
            filter=Q(
                panelist__category=Panelist.CATEGORY.music,
            )
        ),
        per_score=Avg(
            'points',
            filter=Q(
                panelist__category=Panelist.CATEGORY.performance,
            )
        ),
        sng_score=Avg(
            'points',
            filter=Q(
                panelist__category=Panelist.CATEGORY.singing,
            )
        ),
    )
    appearances = Appearance.objects.select_related(
        'group',
        'round',
        'round__session',
    ).prefetch_related(
        'songs__scores',
        'songs__scores__panelist',
    ).filter(
        group=appearance.group,
        round__session=appearance.round.session,
    ).annotate(
        tot_points=Sum(
            'songs__scores__points',
            filter=Q(
                songs__scores__panelist__kind=Panelist.KIND.official,
            ),
        ),
        mus_points=Sum(
            'songs__scores__points',
            filter=Q(
                songs__scores__panelist__kind=Panelist.KIND.official,
                songs__scores__panelist__category=Panelist.CATEGORY.music,
            ),
        ),
        per_points=Sum(
            'songs__scores__points',
            filter=Q(
                songs__scores__panelist__kind=Panelist.KIND.official,
                songs__scores__panelist__category=Panelist.CATEGORY.performance,
            ),
        ),
        sng_points=Sum(
            'songs__scores__points',
            filter=Q(
                songs__scores__panelist__kind=Panelist.KIND.official,
                songs__scores__panelist__category=Panelist.CATEGORY.singing,
            ),
        ),
        tot_score=Avg(
            'songs__scores__points',
            filter=Q(
                songs__scores__panelist__kind=Panelist.KIND.official,
            ),
        ),
        mus_score=Avg(
            'songs__scores__points',
            filter=Q(
                songs__scores__panelist__kind=Panelist.KIND.official,
                songs__scores__panelist__category=Panelist.CATEGORY.music,
            ),
        ),
        per_score=Avg(
            'songs__scores__points',
            filter=Q(
                songs__scores__panelist__kind=Panelist.KIND.official,
                songs__scores__panelist__category=Panelist.CATEGORY.performance,
            ),
        ),
        sng_score=Avg(
            'songs__scores__points',
            filter=Q(
                songs__scores__panelist__kind=Panelist.KIND.official,
                songs__scores__panelist__category=Panelist.CATEGORY.singing,
            ),
        ),
    )

    # Monkeypatch
    for key, value in stats.items():
        setattr(group, key, value)
    for a in appearances:
        songs = a.songs.prefetch_related(
            'scores',
            'scores__panelist',
        ).order_by(
            'num',
        ).annotate(
            tot_score=Avg(
                'scores__points',
                filter=Q(
                    scores__panelist__kind=Panelist.KIND.official,
                ),
            ),
            mus_score=Avg(
                'scores__points',
                filter=Q(
                    scores__panelist__kind=Panelist.KIND.official,
                    scores__panelist__category=Panelist.CATEGORY.music,
                ),
            ),
            per_score=Avg(
                'scores__points',
                filter=Q(
                    scores__panelist__kind=Panelist.KIND.official,
                    scores__panelist__category=Panelist.CATEGORY.performance,
                ),
            ),
            sng_score=Avg(
                'scores__points',
                filter=Q(
                    scores__panelist__kind=Panelist.KIND.official,
                    scores__panelist__category=Panelist.CATEGORY.singing,
                ),
            ),
            tot_points=Sum(
                'scores__points',
                filter=Q(
                    scores__panelist__kind=Panelist.KIND.official,
                ),
            ),
            mus_points=Sum(
                'scores__points',
                filter=Q(
                    scores__panelist__kind=Panelist.KIND.official,
                    scores__panelist__category=Panelist.CATEGORY.music,
                ),
            ),
            per_points=Sum(
                'scores__points',
                filter=Q(
                    scores__panelist__kind=Panelist.KIND.official,
                    scores__panelist__category=Panelist.CATEGORY.performance,
                ),
            ),
            sng_points=Sum(
                'scores__points',
                filter=Q(
                    scores__panelist__kind=Panelist.KIND.official,
                    scores__panelist__category=Panelist.CATEGORY.singing,
                ),
            ),
        )
        for song in songs:
            penalties_map = {
                10: "†",
                30: "‡",
                40: "✠",
                50: "✶",
            }
            items = " ".join([penalties_map[x] for x in song.penalties])
            song.penalties_patched = items
        a.songs_patched = songs
    group.appearances_patched = appearances
    context = {'group': group}

    template = 'emails/appearance_complete.txt'
    subject = "[Barberscore] CSA for {0}".format(
        appearance.group.name,
    )
    to = appearance.group.get_officer_emails()
    cc = appearance.round.session.convention.get_drcj_emails()
    cc.extend(appearance.round.session.convention.get_ca_emails())

    if appearance.csa:
        pdf = appearance.csa.file
    else:
        pdf = appearance.get_csa()
    file_name = '{0} {1} Session {2} CSA'.format(
        appearance.round.session.convention.name,
        appearance.round.session.get_kind_display(),
        appearance.group.name,
    )
    attachments = [(
        file_name,
        pdf,
        'application/pdf',
    )]

    email = build_email(
        template=template,
        context=context,
        subject=subject,
        to=to,
        cc=cc,
        attachments=attachments,
    )
    return email.send()


def send_invite_email_from_entry(entry):
    template = 'emails/entry_invite.txt'
    context = {'entry': entry}
    subject = "[Barberscore] Contest Invitation for {0}".format(
        entry.group.name,
    )
    to = entry.group.get_officer_emails()
    cc = entry.session.convention.get_drcj_emails()
    cc.extend(entry.session.convention.get_ca_emails())
    email = build_email(
        template=template,
        context=context,
        subject=subject,
        to=to,
        cc=cc,
    )
    return email.send()


def send_withdraw_email_from_entry(entry):
    # Send confirmation email
    template = 'emails/entry_withdraw.txt'
    context = {'entry': entry}
    subject = "[Barberscore] Withdrawl Notification for {0}".format(
        entry.group.name,
    )
    to = entry.group.get_officer_emails()
    cc = entry.session.convention.get_drcj_emails()
    cc.extend(entry.session.convention.get_ca_emails())
    email = build_email(
        template=template,
        context=context,
        subject=subject,
        to=to,
        cc=cc,
    )
    return email.send()


def send_submit_email_from_entry(entry):
    template = 'emails/entry_submit.txt'
    contestants = entry.contestants.filter(
        status__gt=0,
    ).order_by('contest__award__name')
    context = {
        'entry': entry,
        'contestants': contestants,
    }
    subject = "[Barberscore] Submission Notification for {0}".format(
        entry.group.name,
    )
    to = entry.group.get_officer_emails()
    cc = entry.session.convention.get_drcj_emails()
    cc.extend(entry.session.convention.get_ca_emails())
    email = build_email(
        template=template,
        context=context,
        subject=subject,
        to=to,
        cc=cc,
    )
    return email.send()


def send_approve_email_from_entry(entry):
    template = 'emails/entry_approve.txt'
    repertories = entry.group.repertories.order_by(
        'chart__title',
    )
    contestants = entry.contestants.filter(
        status__gt=0,
    ).order_by(
        'contest__award__name',
    )
    members = entry.group.members.filter(
        status__gt=0,
    ).order_by(
        'person__last_name',
        'person__first_name',
    )
    context = {
        'entry': entry,
        'repertories': repertories,
        'contestants': contestants,
        'members': members,
    }
    subject = "[Barberscore] Approval Notification for {0}".format(
        entry.group.name,
    )
    to = entry.group.get_officer_emails()
    cc = entry.session.convention.get_drcj_emails()
    cc.extend(entry.session.convention.get_ca_emails())
    email = build_email(
        template=template,
        context=context,
        subject=subject,
        to=to,
        cc=cc,
    )
    return email.send()


def send_psa_from_panelist(panelist):
    context = {'panelist': panelist}

    template = 'emails/panelist_complete.txt'
    subject = "[Barberscore] PSA for {0}".format(
        panelist.person.common_name,
    )
    to = ["{0} <{1}>".format(panelist.person.common_name, panelist.person.email)]
    cc = panelist.round.session.convention.get_ca_emails()

    if panelist.psa:
        pdf = panelist.psa.file
    else:
        pdf = panelist.get_psa()
    file_name = '{0} PSA'.format(
        panelist,
    )
    attachments = [(
        file_name,
        pdf,
        'application/pdf',
    )]

    email = build_email(
        template=template,
        context=context,
        subject=subject,
        to=to,
        cc=cc,
        attachments=attachments,
    )
    return email.send()


def send_publish_email_from_round(round):
    Appearance = apps.get_model('api.appearance')
    Group = apps.get_model('api.group')
    Panelist = apps.get_model('api.panelist')
    group_ids = round.appearances.filter(
        is_private=False,
    ).exclude(
        # Don't include advancers on OSS
        draw__gt=0,
    ).exclude(
        # Don't include mic testers on OSS
        num__lte=0,
    ).values_list('group__id', flat=True)
    completes = Group.objects.filter(
        id__in=group_ids,
    ).prefetch_related(
        'appearances',
        'appearances__songs__scores',
        'appearances__songs__scores__panelist',
        'appearances__round__session',
    ).annotate(
        tot_points=Sum(
            'appearances__songs__scores__points',
            filter=Q(
                appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                appearances__round__session=round.session,
            ),
        ),
        per_points=Sum(
            'appearances__songs__scores__points',
            filter=Q(
                appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                appearances__songs__scores__panelist__category=Panelist.CATEGORY.performance,
                appearances__round__session=round.session,
            ),
        ),
        sng_points=Sum(
            'appearances__songs__scores__points',
            filter=Q(
                appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                appearances__songs__scores__panelist__category=Panelist.CATEGORY.singing,
                appearances__round__session=round.session,
            ),
        ),
        tot_score=Avg(
            'appearances__songs__scores__points',
            filter=Q(
                appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                appearances__round__session=round.session,
            ),
        ),
    ).order_by(
        '-tot_points',
        '-sng_points',
        '-per_points',
    )

    # Draw Block
    if round.kind != round.KIND.finals:
        # Get advancers
        advancers = round.appearances.filter(
            status=Appearance.STATUS.advanced,
        ).select_related(
            'group',
        ).order_by(
            'draw',
        ).values_list(
            'draw',
            'group__name',
        )
        advancers = list(advancers)
        try:
            mt = round.appearances.get(
                draw=0,
            ).group.name
            advancers.append(('MT', mt))
        except Appearance.DoesNotExist:
            pass
    else:
        advancers = None

    # Outcome Block
    items = round.outcomes.select_related(
        'award',
    ).order_by(
        'num',
    ).values_list(
        'num',
        'award__name',
        'name',
    )
    outcomes = []
    for item in items:
        outcomes.append(
            (
                "{0} {1}".format(item[0], item[1]),
                item[2],
            )
        )

    context = {
        'round': round,
        'advancers': advancers,
        'completes': completes,
        'outcomes': outcomes,
    }
    template = 'emails/round_publish.txt'
    subject = "[Barberscore] {0} Results".format(
        round,
    )
    to = round.session.convention.get_ca_emails()
    cc = round.session.convention.get_drcj_emails()
    cc.extend(round.get_judge_emails())
    bcc = round.session.get_participant_emails()

    if round.oss:
        pdf = round.oss.file
    else:
        pdf = round.get_oss()
    file_name = '{0} {1} {2} OSS'.format(
        round.session.convention.name,
        round.session.get_kind_display(),
        round.get_kind_display(),
    )
    attachments = [(
        file_name,
        pdf,
        'application/pdf',
    )]
    context['bcc'] = [x.partition(" <")[0] for x in bcc]

    email = build_email(
        template=template,
        context=context,
        subject=subject,
        to=to,
        cc=cc,
        bcc=bcc,
        attachments=attachments,
    )
    return email.send()


def send_publish_report_email_from_round(round):
    template = 'emails/round_publish_report.txt'
    context = {
        'round': round,
    }
    subject = "[Barberscore] {0} Reports".format(
        round,
    )
    to = round.session.convention.get_ca_emails()
    cc = round.session.convention.get_drcj_emails()
    cc.extend(round.get_judge_emails())
    attachments = []
    if round.sa:
        pdf = round.sa.file
    else:
        pdf = round.get_sa()
    file_name = '{0} {1} {2} SA'.format(
        round.session.convention.name,
        round.session.get_kind_display(),
        round.get_kind_display(),
    )
    attachments = [(
        file_name,
        pdf,
        'application/pdf',
    )]

    email = build_email(
        template=template,
        context=context,
        subject=subject,
        to=to,
        cc=cc,
        attachments=attachments,
    )
    return email.send()


def send_open_email_from_session(session):
    template = 'emails/session_open.txt'
    context = {'session': session,}
    subject = "[Barberscore] {0} Session is OPEN".format(
        session,
    )
    to = session.convention.get_drcj_emails()
    cc = session.convention.get_ca_emails()
    bcc = session.get_district_emails()
    context['bcc'] = [x.partition(" <")[0] for x in bcc]
    email = build_email(
        template=template,
        context=context,
        subject=subject,
        to=to,
        cc=cc,
        bcc=bcc,
    )
    return email.send()


def send_close_email_from_session(session):
    template = 'emails/session_close.txt'
    context = {'session': session}
    subject = "[Barberscore] {0} Session is CLOSED".format(
        session,
    )
    to = session.convention.get_drcj_emails()
    cc = session.convention.get_ca_emails()
    bcc = session.get_district_emails()
    context['bcc'] = [x.partition(" <")[0] for x in bcc]
    email = build_email(
        template=template,
        context=context,
        subject=subject,
        to=to,
        cc=cc,
        bcc=bcc,
    )
    return email.send()


def send_verify_email_from_session(session):
    template = 'emails/session_verify.txt'
    approved_entries = session.entries.filter(
        status=session.entries.model.STATUS.approved,
    ).order_by('draw')
    context = {
        'session': session,
        'approved_entries': approved_entries,
    }
    subject = "[Barberscore] {0} Session Draw".format(
        session,
    )
    to = session.convention.get_drcj_emails()
    cc = session.convention.get_ca_emails()
    bcc = session.get_participant_emails()
    context['bcc'] = [x.partition(" <")[0] for x in bcc]
    email = build_email(
        template=template,
        context=context,
        subject=subject,
        to=to,
        cc=cc,
        bcc=bcc,
    )
    return email.send()


def send_verify_report_email_from_session(session):
    template = 'emails/session_verify_report.txt'
    context = {
        'session': session,
    }
    subject = "[Barberscore] {0} Session Draft Reports".format(
        session,
    )
    to = session.convention.get_drcj_emails()
    cc = session.convention.get_ca_emails()
    attachments = []
    if session.drcj_report:
        xlsx = session.drcj_report.file
    else:
        xlsx = session.get_drcj()
    file_name = '{0} {1} Session DRCJ Report DRAFT'.format(
        session.convention.name,
        session.get_kind_display(),
    )
    attachments.append((
        file_name,
        xlsx,
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    ))
    if session.legacy_report:
        xlsx = session.legacy_report.file
    else:
        xlsx = session.get_legacy()
    file_name = '{0} {1} Session Legacy Report DRAFT'.format(
        session.convention.name,
        session.get_kind_display(),
    )
    attachments.append((
        file_name,
        xlsx,
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    ))
    email = build_email(
        template=template,
        context=context,
        subject=subject,
        to=to,
        cc=cc,
        attachments=attachments,
    )
    return email.send()


def send_package_email_from_session(session):
    template = 'emails/session_package.txt'
    approved_entries = session.entries.filter(
        status=session.entries.model.STATUS.approved,
    ).order_by('draw')
    context = {
        'session': session,
        'approved_entries': approved_entries,
    }
    subject = "[Barberscore] {0} Session Starting".format(
        session,
    )
    to = session.convention.get_drcj_emails()
    cc = session.convention.get_ca_emails()
    bcc = session.get_participant_emails()
    context['bcc'] = [x.partition(" <")[0] for x in bcc]
    email = build_email(
        template=template,
        context=context,
        subject=subject,
        to=to,
        cc=cc,
        bcc=bcc,
    )
    return email.send()


def send_package_report_email_from_session(session):
    template = 'emails/session_package_report.txt'
    context = {
        'session': session,
    }
    subject = "[Barberscore] {0} Session FINAL Reports".format(
        session,
    )
    to = session.convention.get_drcj_emails()
    cc = session.convention.get_ca_emails()

    attachments = []
    if session.drcj_report:
        xlsx = session.drcj_report.file
    else:
        xlsx = session.get_drcj()
    file_name = '{0} {1} Session DRCJ Report FINAL'.format(
        session.convention.name,
        session.get_kind_display(),
    )
    attachments.append((
        file_name,
        xlsx,
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    ))
    if session.legacy_report:
        xlsx = session.legacy_report.file
    else:
        xlsx = session.get_legacy()
    file_name = '{0} {1} Session Legacy Report FINAL'.format(
        session.convention.name,
        session.get_kind_display(),
    )
    attachments.append((
        file_name,
        xlsx,
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    ))
    email = build_email(
        template=template,
        context=context,
        subject=subject,
        to=to,
        cc=cc,
        attachments=attachments,
    )
    return email.send()


def save_csa_from_appearance(appearance):
    return appearance.save_csa()


def save_psa_from_panelist(panelist):
    content = panelist.get_psa()
    return panelist.psa.save('psa', content, save=False)


def save_reports_from_round(round):
    oss = round.get_oss()
    round.oss.save('oss', oss, save=False)
    sa = round.get_sa()
    round.sa.save('sa', sa, save=False)
    return round.save()

def check_member(member):
    if not member.group.mc_pk:
        raise RuntimeError("Not an MC entity.")
    Join = apps.get_model('bhs.join')
    Member = apps.get_model('api.member')
    try:
        join = Join.objects.filter(
            structure__id=member.group.mc_pk,
            subscription__human__id=member.person.mc_pk,
            paid=True,
            deleted__isnull=True,
        ).latest(
            'modified',
            '-inactive_date',
        )
    except Join.DoesNotExist:
        gone = str(member)
        member.delete()
        return gone, "Deleted"
    return Member.objects.update_or_create_from_join(join)


def check_officer(officer):
    if not officer.group.mc_pk:
        raise RuntimeError("Not an MC group.")
    if not officer.office.mc_pk:
        raise RuntimeError("Not an MC office.")
    Role = apps.get_model('bhs.role')
    Officer = apps.get_model('api.officer')
    try:
        role = Role.objects.filter(
            structure__id=officer.group.mc_pk,
            human__id=officer.person.mc_pk,
        ).latest(
            'modified',
            'created',
        )
    except Role.DoesNotExist:
        gone = str(officer)
        officer.delete()
        return gone, "Deleted"
    return Officer.objects.update_or_create_from_role(role)


def get_auth0():
    auth0_api_access_token = cache.get('auth0_api_access_token')
    if not auth0_api_access_token:
        client = GetToken(settings.AUTH0_DOMAIN)
        response = client.client_credentials(
            settings.AUTH0_CLIENT_ID,
            settings.AUTH0_CLIENT_SECRET,
            settings.AUTH0_AUDIENCE,
        )
        cache.set(
            'auth0_api_access_token',
            response['access_token'],
            timeout=response['expires_in'],
        )
        auth0_api_access_token = response['access_token']
    auth0 = Auth0(
        settings.AUTH0_DOMAIN,
        auth0_api_access_token,
    )
    return auth0


def get_accounts(path='barberscore.csv'):
    with open(path) as f:
        next(f)  # Skip headers
        reader = csv.reader(f, skipinitialspace=True)
        rows = [row for row in reader]
        return rows
