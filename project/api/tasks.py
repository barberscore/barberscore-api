# Standard Libary
import csv
import logging
import time
import tempfile
from django.core.files.base import ContentFile
from django.core.files import File
from PyPDF2 import PdfFileMerger

# Third-Party
import pydf
from auth0.v3.authentication import GetToken
from auth0.v3.exceptions import Auth0Error
from auth0.v3.management import Auth0
from django_rq import job
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from django.db.models import Q
from django.utils.timezone import localdate

# Django
from django.apps import apps
from django.conf import settings
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.core.validators import validate_email
from django.core.validators import ValidationError
from django.utils.text import slugify
from django.db.models import Count
from django.db.models import Q

log = logging.getLogger(__name__)


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


@job('low')
def create_account(user):
    auth0 = get_auth0()
    email = user.email.lower()
    name = user.name.strip()
    random = get_random_string()
    status = user.get_status_display()
    bhs_id = user.bhs_id
    if user.current_through:
        current_through = user.current_through.isoformat()
    else:
        current_through = None
    pk = str(user.id)
    payload = {
        'connection': 'Default',
        'email': email,
        'email_verified': True,
        'password': random,
        'app_metadata': {
            'pk': pk,
            'status': status,
            'name': name,
            'bhs_id': bhs_id,
            'current_through': current_through,
        }
    }
    account = auth0.users.create(payload)
    user.username = account['user_id']
    user.save()
    return account


@job('low')
def update_account(user):
    auth0 = get_auth0()
    name = user.name
    email = user.email
    status = user.get_status_display()
    bhs_id = user.bhs_id
    if user.current_through:
        current_through = user.current_through.isoformat()
    else:
        current_through = None
    pk = str(user.id)
    payload = {
        'email': email,
        'email_verified': True,
        'user_metadata': None,
        'app_metadata': {
            'pk': pk,
            'status': status,
            'name': name,
            'bhs_id': bhs_id,
            'current_through': current_through,
        }
    }
    account = auth0.users.update(user.username, payload)
    return account


@job('low')
def delete_account(user):
    auth0 = get_auth0()
    # Delete Auth0
    auth0.users.delete(user.username)
    return


@job('low')
def link_account(user):
    Person = apps.get_model('api.person')
    auth0 = get_auth0()
    account = auth0.users.get(user.username)
    email = account['email'].lower()
    person, created = Person.objects.get_or_create(email=email)
    return person


@job('low')
def unlink_user_account(user):
    client = get_auth0()
    user_id = user.username.partition('|')[2]
    client.users.unlink_user_account(
        user.account_id,
        'auth0',
        user_id,
    )
    return


@job('low')
def relink_user_account(user):
    client = get_auth0()
    user_id = user.account_id.partition('|')[2]
    payload = {
        'provider': 'email',
        'user_id': user_id,
    }
    client.users.link_user_account(
        user.username,
        payload,
    )
    return


@job
def create_legacy_report(session):
    Entry = apps.get_model('api.entry')
    wb = Workbook()
    ws = wb.active
    fieldnames = [
        'oa',
        'contestant_id',
        'group_name',
        'group_type',
        'song_number',
        'song_title',
    ]
    ws.append(fieldnames)
    entries = session.entries.filter(
        status__in=[
            Entry.STATUS.approved,
        ]
    ).order_by('draw')
    for entry in entries:
        oa = entry.draw
        group_name = entry.group.name.encode('utf-8').strip()
        group_type = entry.group.get_kind_display()
        if group_type == 'Quartet':
            contestant_id = entry.group.bhs_id
        elif group_type == 'Chorus':
            contestant_id = entry.group.code
        else:
            raise RuntimeError("Improper Entity Type")
        i = 1
        for repertory in entry.group.repertories.order_by('chart__title'):
            song_number = i
            song_title = repertory.chart.title.encode('utf-8').strip()
            i += 1
            row = [
                oa,
                contestant_id,
                group_name,
                group_type,
                song_number,
                song_title,
            ]
            ws.append(row)
    file = save_virtual_workbook(wb)
    content = ContentFile(file)
    return content


@job
def create_drcj_report(session):
    Entry = apps.get_model('api.entry')
    Group = apps.get_model('api.group')
    Member = apps.get_model('api.member')
    wb = Workbook()
    ws = wb.active
    fieldnames = [
        'OA',
        'Group Name',
        'Representing',
        'Evaluation?',
        'Score/Eval-Only?',
        'BHS ID',
        'Group Status',
        'Repertory Count',
        'Estimated MOS',
        'Members Expiring',
        'Tenor',
        'Lead',
        'Baritone',
        'Bass',
        'Director/Participant(s)',
        'Award(s)',
        'Chapter(s)',
    ]
    ws.append(fieldnames)
    entries = session.entries.filter(
        status__in=[
            Entry.STATUS.approved,
        ]
    ).order_by('draw')
    for entry in entries:
        oa = entry.draw
        group_name = entry.group.name
        representing = entry.representing
        evaluation = entry.is_evaluation
        private = entry.is_private
        bhs_id = entry.group.bhs_id
        repertory_count = entry.group.repertories.filter(
            status__gt=0,
        ).count()
        group_status = entry.group.get_status_display()
        repertory_count = entry.group.repertories.filter(
            status__gt=0,
        ).count()
        participant_count = entry.pos
        members = entry.group.members.filter(
            status__gt=0,
        )
        expiring_count = members.filter(
            person__user__current_through__lte=session.convention.close_date,
        ).count()
        participants = entry.participants
        awards_list = []
        contestants = entry.contestants.filter(
            status__gt=0,
        ).order_by('contest__award__name')
        for contestant in contestants:
            awards_list.append(contestant.contest.award.name)
        awards = "\n".join(filter(None, awards_list))
        parts = {}
        part = 1
        while part <= 4:
            try:
                member = members.get(
                    part=part,
                )
            except Member.DoesNotExist:
                parts[part] = None
                part += 1
                continue
            except Member.MultipleObjectsReturned:
                parts[part] = None
                part += 1
                continue
            member_list = []
            member_list.append(
                member.person.nomen,
            )
            member_list.append(
                member.person.email,
            )
            member_list.append(
                member.person.phone,
            )
            member_detail = "\n".join(filter(None, member_list))
            parts[part] = member_detail
            part += 1
        if entry.group.kind == entry.group.KIND.quartet:
            persons = members.values_list('person', flat=True)
            cs = Group.objects.filter(
                members__person__in=persons,
                members__status__gt=0,
                kind=Group.KIND.chorus,
            ).distinct(
            ).order_by(
                'parent__name',
            ).values_list(
                'parent__name',
                flat=True
            )
            chapters = "\n".join(cs)
        elif entry.group.kind == entry.group.KIND.chorus:
            try:
                chapters = entry.group.parent.name
            except AttributeError:
                chapters = None
        row = [
            oa,
            group_name,
            representing,
            evaluation,
            private,
            bhs_id,
            group_status,
            repertory_count,
            participant_count,
            expiring_count,
            parts[1],
            parts[2],
            parts[3],
            parts[4],
            participants,
            awards,
            chapters,
        ]
        ws.append(row)
    file = save_virtual_workbook(wb)
    content = ContentFile(file)
    return content


@job
def create_contact_report(session):
    Entry = apps.get_model('api.entry')
    wb = Workbook()
    ws = wb.active
    fieldnames = [
        'group',
        'admin',
        'email',
        'cell',
    ]
    ws.append(fieldnames)
    entries = session.entries.filter(
        status__in=[
            Entry.STATUS.approved,
        ]
    ).order_by('group__name')
    for entry in entries:
        admins = entry.group.officers.filter(
            status__gt=0,
        )
        for admin in admins:
            group = entry.group.nomen
            person = admin.person.nomen
            email = admin.person.email
            cell = admin.person.cell_phone
            row = [
                group,
                person,
                email,
                cell,
            ]
            ws.append(row)
    file = save_virtual_workbook(wb)
    content = ContentFile(file)
    return content


@job
def create_roster_report(group):
    Member = apps.get_model('api.member')
    wb = Workbook()
    ws = wb.active
    fieldnames = [
        'BHS ID',
        'First Name',
        'Last Name',
        'Expiration Date',
        'Status',
    ]
    ws.append(fieldnames)
    members = group.members.filter(
        status=Member.STATUS.active,
    ).order_by('person__last_name', 'person__first_name')
    for member in members:
        bhs_id = member.person.bhs_id
        first_name = member.person.first_name
        last_name = member.person.last_name
        expiration = member.person.user.current_through
        status = member.person.get_status_display()
        row = [
            bhs_id,
            first_name,
            last_name,
            expiration,
            status,
        ]
        ws.append(row)
    file = save_virtual_workbook(wb)
    content = ContentFile(file)
    return content


@job
def create_chart_report():
    Chart = apps.get_model('api.chart')
    wb = Workbook()
    ws = wb.active
    fieldnames = [
        'PK',
        'Title',
        'Arrangers',
        'Composers',
        'Lyricists',
        'Holders',
        'Status',
    ]
    ws.append(fieldnames)
    charts = Chart.objects.order_by('title', 'arrangers')
    for chart in charts:
        pk = str(chart.pk)
        title = chart.title
        arrangers = chart.arrangers
        composers = chart.composers
        lyricists = chart.lyricists
        holders = chart.holders
        status = chart.get_status_display()
        row = [
            pk,
            title,
            arrangers,
            composers,
            lyricists,
            holders,
            status,
        ]
        ws.append(row)
    file = save_virtual_workbook(wb)
    content = ContentFile(file)
    return content


@job
def create_variance_report(appearance):
    Score = apps.get_model('api.score')
    Panelist = apps.get_model('api.panelist')
    songs = appearance.songs.order_by('num')
    scores = Score.objects.filter(
        kind=Score.KIND.official,
        song__in=songs,
    ).order_by(
        'category',
        'panelist__person__last_name',
        'song__num',
    )
    panelists = appearance.round.panelists.filter(
        kind=Panelist.KIND.official,
        category__gt=Panelist.CATEGORY.ca,
    ).order_by(
        'category',
        'person__last_name',
    )
    context = {
        'appearance': appearance,
        'songs': songs,
        'scores': scores,
        'panelists': panelists,
    }
    rendered = render_to_string('variance.html', context)
    file = pydf.generate_pdf(rendered, enable_smart_shrinking=False)
    content = ContentFile(file)
    appearance.variance_report.save(
        "{0}-variance-report".format(
            slugify(appearance.competitor.group.name),
        ),
        content,
    )
    appearance.save()
    return


@job
def create_sung_report(round):
    Song = apps.get_model('api.song')
    appearances = round.appearances.filter(
        draw__isnull=False,
    ).order_by(
        'draw',
    )
    for appearance in appearances:
        songs = Song.objects.filter(
            appearance__competitor=appearance.competitor,
        ).distinct().order_by(
            'appearance__round__num',
            'num',
        )
        sungs = []
        for song in songs:
            try:
                title = song.chart.nomen
            except AttributeError:
                title = "Unknown (Not in Repertory)"
            row = "{0} Song {1}: {2}".format(
                song.appearance.round.get_kind_display(),
                song.num,
                title,
            )
            sungs.append(row)
        appearance.sungs = sungs

    context = {
        'appearances': appearances,
        'round': round,
    }
    rendered = render_to_string('sung.html', context)
    file = pydf.generate_pdf(
        rendered,
        page_size='Letter',
        orientation='Portrait',
        margin_top='5mm',
        margin_bottom='5mm',
    )
    content = ContentFile(file)
    return content


@job
def create_round_oss(round):
    Competitor = apps.get_model('api.competitor')
    Contest = apps.get_model('api.contest')
    Panelist = apps.get_model('api.panelist')
    Contestant = apps.get_model('api.contestant')
    Round = apps.get_model('api.round')
    competitors = round.session.competitors.filter(
        # status=Competitor.STATUS.finished,
        appearances__round=round,
        appearances__draw__isnull=True,
        is_private=False,
    ).select_related(
        'group',
        'entry',
    ).prefetch_related(
        'entry__contestants',
        'entry__contestants__contest',
        'appearances',
        'appearances__round',
        'appearances__songs',
        'appearances__songs__chart',
        'appearances__songs__scores',
        'appearances__songs__scores__panelist',
        'appearances__songs__scores__panelist__person',
    ).order_by(
        '-tot_points',
        '-sng_points',
        '-per_points',
        'group__name',
    )
    for competitor in competitors:
        # Monkey-patch contesting
        contestants = competitor.entry.contestants.filter(
            status=Contestant.STATUS.included,
        ).order_by('contest__num').values_list('contest__num', flat=True)
        if contestants:
            competitor.contestants = contestants
        else:
            competitor.contestants = ""
    # Eval Only
    privates = round.session.competitors.filter(
        status=Competitor.STATUS.finished,
        appearances__round=round,
        is_private=True,
    ).select_related(
        'group',
        'entry',
    ).order_by(
        'group__name',
    )
    privates = privates.values_list('group__name', flat=True)
    if round.kind != round.KIND.finals:
        advancers = round.appearances.filter(
            draw__isnull=False,
        ).select_related(
            'competitor__group',
        ).order_by(
            'draw',
        )
    else:
        advancers = None
    contests = round.session.contests.filter(
        status=Contest.STATUS.included,
        contestants__status__gt=0,
    ).select_related(
        'award',
        'group',
    ).distinct(
    ).order_by(
        '-is_primary',
        'award__tree_sort',
    )
    # Determine Primary (if present)
    try:
        primary = contests.get(is_primary=True)
    except Contest.DoesNotExist:
        primary = None
    # MonkeyPatch qualifiers
    for contest in contests:
        if round.num == contest.award.rounds:
            if contest.award.level != contest.award.LEVEL.deferred:
                if contest.award.level == contest.award.LEVEL.qualifier:
                    threshold = contest.award.threshold
                    if threshold:
                        qualifiers = contest.contestants.filter(
                            status__gt=0,
                            entry__competitor__tot_score__gte=threshold,
                            entry__is_private=False,
                        ).distinct(
                        ).order_by(
                            'entry__group__name',
                        ).values_list(
                            'entry__group__name',
                            flat=True,
                        )
                        if qualifiers:
                            contest.detail = ", ".join(
                                qualifiers.values_list('entry__group__name', flat=True)
                            )
                        else:
                            contest.detail = "(No qualifiers)"
                else:
                    if contest.group:
                        contest.detail = str(contest.group.name)
                    else:
                        contest.detail = "(No recipient)"
            else:
                contest.detail = "(Result determined post-contest)"
        else:
            contest.detail = "(Result not yet determined)"
    panelists = round.panelists.select_related(
        'person',
    ).filter(
        kind=Panelist.KIND.official,
        category__gte=Panelist.CATEGORY.ca,
    ).order_by(
        'category',
        'person__last_name',
        'person__first_name',
    )
    is_multi = all([
        round.session.rounds.count() > 1,
    ])
    context = {
        'round': round,
        'competitors': competitors,
        'privates': privates,
        'advancers': advancers,
        'panelists': panelists,
        'contests': contests,
        'is_multi': is_multi,
        'primary': primary,
    }
    rendered = render_to_string('oss.html', context)
    file = pydf.generate_pdf(
        rendered,
        page_size='Legal',
        orientation='Portrait',
        margin_top='5mm',
        margin_bottom='5mm',
    )
    content = ContentFile(file)
    return content


@job
def create_session_oss(session):
    Competitor = apps.get_model('api.competitor')
    Contest = apps.get_model('api.contest')
    Panelist = apps.get_model('api.panelist')
    Contestant = apps.get_model('api.contestant')
    competitors = session.competitors.filter(
        status=Competitor.STATUS.finished,
        is_private=False,
    ).select_related(
        'group',
        'entry',
    ).prefetch_related(
        'entry__contestants',
        'entry__contestants__contest',
        'appearances',
        'appearances__round',
        'appearances__songs',
        'appearances__songs__chart',
        'appearances__songs__scores',
        'appearances__songs__scores__panelist',
        'appearances__songs__scores__panelist__person',
    ).order_by(
        'tot_rank',
        '-tot_points',
        '-sng_points',
        '-per_points',
        'group__name',
    )
    for competitor in competitors:
        # Monkey-patch contesting
        try:
            contestants = competitor.entry.contestants.filter(
                status=Contestant.STATUS.included,
            ).order_by('contest__num').values_list('contest__num', flat=True)
        except AttributeError:
            contestants = None
        if contestants:
            competitor.contestants = contestants
        else:
            competitor.contestants = ""
    # Eval Only
    privates = session.competitors.filter(
        status=Competitor.STATUS.finished,
        is_private=True,
    ).select_related(
        'group',
        'entry',
    ).order_by(
        'group__name',
    )
    privates = privates.values_list('group__name', flat=True)
    contests = session.contests.filter(
        status=Contest.STATUS.included,
        contestants__status__gt=0,
    ).select_related(
        'award',
        'group',
    ).distinct(
    ).order_by(
        '-is_primary',
        'award__tree_sort',
    )
    # Determine Primary (if present)
    try:
        primary = contests.get(is_primary=True)
    except Contest.DoesNotExist:
        primary = None
    # MonkeyPatch qualifiers
    for contest in contests:
        if contest.award.level != contest.award.LEVEL.deferred:
            if contest.award.level == contest.award.LEVEL.qualifier:
                threshold = contest.award.threshold
                if threshold:
                    qualifiers = contest.contestants.filter(
                        status__gt=0,
                        entry__competitor__tot_score__gte=threshold,
                        entry__is_private=False,
                    ).distinct(
                    ).order_by(
                        'entry__group__name',
                    ).values_list(
                        'entry__group__name',
                        flat=True,
                    )
                    if qualifiers:
                        contest.detail = ", ".join(
                            qualifiers.values_list('entry__group__name', flat=True)
                        )
                    else:
                        contest.detail = "(No qualifiers)"
            else:
                if contest.group:
                    contest.detail = str(contest.group.name)
                else:
                    contest.detail = "(No recipient)"
        else:
            contest.detail = "(Result determined post-contest)"
    panelists = Panelist.objects.filter(
        round__session=session,
        kind=Panelist.KIND.official,
        category__gte=Panelist.CATEGORY.ca,
    ).distinct(
        'category',
        'person__last_name',
        'person__first_name',
    ).order_by(
        'category',
        'person__last_name',
        'person__first_name',
    )
    context = {
        'session': session,
        'competitors': competitors,
        'privates': privates,
        'panelists': panelists,
        'contests': contests,
        'primary': primary,
        'is_multi': False,
    }
    rendered = render_to_string('oss.html', context)
    file = pydf.generate_pdf(
        rendered,
        page_size='Legal',
        orientation='Portrait',
        margin_top='5mm',
        margin_bottom='5mm',
    )
    content = ContentFile(file)
    return content


@job
def create_csa_report(competitor):
    Panelist = apps.get_model('api.panelist')
    Member = apps.get_model('api.member')
    Song = apps.get_model('api.song')
    panelists = Panelist.objects.filter(
        kind=Panelist.KIND.official,
        scores__song__appearance__competitor=competitor,
    ).distinct(
    ).order_by(
        'category',
        'person__last_name',
    )
    appearances = competitor.appearances.order_by(
        '-num',
    ).prefetch_related(
        'songs',
    )
    songs = Song.objects.select_related(
        'chart',
    ).filter(
        appearance__competitor=competitor,
    ).prefetch_related(
        'scores',
        'scores__panelist__person',
    ).order_by(
        '-appearance__round__num',
        'num',
    )
    context = {
        'competitor': competitor,
        'panelists': panelists,
        'appearances': appearances,
        'songs': songs,
    }
    rendered = render_to_string('csa.html', context)
    file = pydf.generate_pdf(rendered)
    content = ContentFile(file)
    return content


@job
def save_csa_report(competitor):
    content = create_csa_report(competitor)
    competitor.csa.save(
        slugify(
            '{0} csa'.format(
                competitor.group.name,
            )
        ),
        content=content,
    )
    return


@job
def create_sa_report(round):
    Panelist = apps.get_model('api.panelist')
    Competitor = apps.get_model('api.competitor')
    panelists = Panelist.objects.filter(
        kind__in=[
            Panelist.KIND.official,
            Panelist.KIND.practice,
        ],
        scores__song__appearance__round=round,
    ).select_related(
        'person',
    ).distinct(
    ).order_by(
        'category',
        'kind',
        'person__last_name',
        'person__nick_name',
        'person__first_name',
    )
    mo_count = panelists.filter(
        category=Panelist.CATEGORY.music,
        kind=Panelist.KIND.official,
    ).count()
    po_count = panelists.filter(
        category=Panelist.CATEGORY.performance,
        kind=Panelist.KIND.official,
    ).count()
    so_count = panelists.filter(
        category=Panelist.CATEGORY.singing,
        kind=Panelist.KIND.official,
    ).count()
    mp_count = panelists.filter(
        category=Panelist.CATEGORY.music,
        kind=Panelist.KIND.practice,
    ).count()
    pp_count = panelists.filter(
        category=Panelist.CATEGORY.performance,
        kind=Panelist.KIND.practice,
    ).count()
    sp_count = panelists.filter(
        category=Panelist.CATEGORY.singing,
        kind=Panelist.KIND.practice,
    ).count()
    competitors = round.session.competitors.filter(
        status=Competitor.STATUS.finished,
    ).select_related(
        'group',
    ).prefetch_related(
        'appearances',
        'appearances__songs',
        'appearances__songs__scores',
        'appearances__songs__scores__panelist',
        'appearances__songs__scores__panelist__person',
    ).order_by(
        '-tot_points',
        '-sng_points',
        '-mus_points',
        '-per_points',
        'group__name',
    )
    context = {
        'round': round,
        'panelists': panelists,
        'competitors': competitors,
        'mo_count': mo_count,
        'po_count': po_count,
        'so_count': so_count,
        'mp_count': mp_count,
        'pp_count': pp_count,
        'sp_count': sp_count,
    }
    rendered = render_to_string('sa.html', context)
    file = pydf.generate_pdf(
        rendered,
        page_size='Letter',
        orientation='Landscape',
    )
    content = ContentFile(file)
    return content


@job
def save_csa_round(round):
    Competitor = apps.get_model('api.competitor')
    competitors = round.session.competitors.filter(
        # status=Competitor.STATUS.finished,
        appearances__round=round,
        appearances__draw__isnull=True,
    ).order_by(
        'group__name',
    )
    merger = PdfFileMerger()
    for competitor in competitors:
        merger.append(competitor.csa, import_bookmarks=False)
    with tempfile.NamedTemporaryFile(mode='w+b',suffix='.pdf') as f:
        merger.write(f.name)
        round.csa.save(
            slugify(
                '{0} csa'.format(
                    round.id,
                )
            ),
            content=f,
            save=True,
        )
    return


@job
def create_pdf(template, context):
    rendered = render_to_string(template, context)
    pdf = pydf.generate_pdf(rendered)
    return pdf


@job('high')
def send_entry(template, context):
    entry = context['entry']
    officers = entry.group.officers.filter(
        status__gt=0,
        person__email__isnull=False,
    )
    if not officers:
        raise RuntimeError("No officers for {0}".format(entry.group))
    ccs = []
    assignments = entry.session.convention.assignments.filter(
        category__lt=10,
    ).exclude(person__email=None)
    tos = ["{0} <{1}>".format(officer.person.common_name, officer.person.email) for officer in officers]
    ccs = ["{0} <{1}>".format(assignment.person.common_name, assignment.person.email) for assignment in assignments]
    if entry.group.kind == entry.group.KIND.quartet:
        members = entry.group.members.filter(
            status__gt=0,
            person__email__isnull=False,
        ).exclude(
            person__officers__in=officers,
        ).distinct()
        for member in members:
            ccs.append(
                "{0} <{1}>".format(member.person.common_name, member.person.email)
            )
    rendered = render_to_string(template, context)
    subject = "[Barberscore] {0} {1} {2} Session".format(
        entry.group.name,
        entry.session.convention.name,
        entry.session.get_kind_display(),
    )
    email = EmailMessage(
        subject=subject,
        body=rendered,
        from_email='Barberscore <admin@barberscore.com>',
        to=tos,
        cc=ccs,
    )
    try:
        result = email.send()
    except Exception as e:
        raise(e)
    if result != 1:
        raise RuntimeError("Email unsuccessful {0}".format(entry))
    return


@job('high')
def send_csa(context):
    competitor = context['competitor']
    officers = competitor.group.officers.filter(
        status__gt=0,
        person__email__isnull=False,
    )
    if not officers:
        raise RuntimeError("No officers for {0}".format(competitor.group))
    tos = ["{0} <{1}>".format(officer.person.common_name, officer.person.email) for officer in officers]
    ccs = ["David Mills <proclamation56@gmail.com>"]
    if competitor.group.kind == competitor.group.KIND.quartet:
        members = competitor.group.members.filter(
            status__gt=0,
            person__email__isnull=False,
        ).exclude(
            person__officers__in=officers,
        ).distinct()
        for member in members:
            ccs.append(
                "{0} <{1}>".format(member.person.common_name, member.person.email)
            )
    rendered = render_to_string('csa.txt', context)
    subject = "[Barberscore] {0} {1} {2} Session CSA".format(
        competitor.group.name,
        competitor.session.convention.name,
        competitor.session.get_kind_display(),
    )
    email = EmailMessage(
        subject=subject,
        body=rendered,
        from_email='Barberscore <admin@barberscore.com>',
        to=tos,
        cc=ccs,
    )
    # try:
    #     result = email.send()
    # except Exception as e:
    #     raise(e)
    # if result != 1:
    #     raise RuntimeError("Email unsuccessful {0}".format(entry))
    return


@job('high')
def send_sa(context):
    round = context['round']
    panelists = round.panelists.filter(
        person__email__isnull=False,
    )
    if not panelists:
        raise RuntimeError("No officers")
    ccs = ["{0} <{1}>".format(panelist.person.common_name, panelist.person.email) for panelist in panelists]
    tos = ["David Mills <proclamation56@gmail.com>"]
    rendered = render_to_string('sa.txt', context)
    subject = "[Barberscore] {0} {1} Round SA".format(
        round.session.convention.name,
        round.session.get_kind_display(),
    )
    email = EmailMessage(
        subject=subject,
        body=rendered,
        from_email='Barberscore <admin@barberscore.com>',
        to=tos,
        cc=ccs,
    )
    # try:
    #     result = email.send()
    # except Exception as e:
    #     raise(e)
    # if result != 1:
    #     raise RuntimeError("Email unsuccessful {0}".format(entry))
    return


@job('high')
def send_session(template, context):
    session = context['session']
    Officer = apps.get_model('api.officer')
    Assignment = apps.get_model('api.assignment')
    Entry = apps.get_model('api.entry')
    if session.status > session.STATUS.closed:
        # only send to approved entries
        officers = Officer.objects.filter(
            status__gt=0,
            person__email__isnull=False,
            group__entries__session=session,
            group__entries__status=Entry.STATUS.approved,
        ).distinct()
    elif not session.is_invitational:
        # send to all active groups in the district
        if session.kind == session.KIND.quartet:
            officers = Officer.objects.filter(
                status__gt=0,
                person__email__isnull=False,
                group__status__gt=0,
                group__kind=session.kind,
                group__parent__grantors__convention=session.convention,
            ).distinct()
        else:
            officers = Officer.objects.filter(
                status__gt=0,
                person__email__isnull=False,
                group__status__gt=0,
                group__kind=session.kind,
                group__parent__parent__grantors__convention=session.convention,
            ).distinct()
    assignments = Assignment.objects.filter(
        convention=session.convention,
        category=Assignment.CATEGORY.drcj,
        status=Assignment.STATUS.active,
    ).exclude(person__email=None)
    to = ["{0} <{1}>".format(assignment.person.common_name, assignment.person.email) for assignment in assignments]
    bcc = ["{0} <{1}>".format(officer.person.common_name, officer.person.email) for officer in officers]
    rendered = render_to_string(template, context)
    subject = "[Barberscore] {0} {1} Session".format(
        session.convention.name,
        session.get_kind_display(),
    )
    email = EmailMessage(
        subject=subject,
        body=rendered,
        from_email='Barberscore <admin@barberscore.com>',
        to=to,
        bcc=bcc,
    )
    return email.send()


@job('high')
def send_session_reports(template, context):
    session = context['session']
    Assignment = apps.get_model('api.assignment')
    assignments = Assignment.objects.filter(
        convention=session.convention,
        category__lte=Assignment.CATEGORY.ca,
        status=Assignment.STATUS.active,
    ).exclude(person__email=None)
    to = ["{0} <{1}>".format(assignment.person.common_name, assignment.person.email) for assignment in assignments]
    rendered = render_to_string(template, context)
    subject = "[Barberscore] {0} {1} Session Reports".format(
        session.convention.name,
        session.get_kind_display(),
    )
    email = EmailMessage(
        subject=subject,
        body=rendered,
        from_email='Barberscore <admin@barberscore.com>',
        to=to,
    )
    return email.send()
