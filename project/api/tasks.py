# Standard Libary
import csv
import logging
import time
from io import BytesIO

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
def save_round_oss(round):
    content = round.get_oss()
    round.oss.save(
        slugify(
            '{0} oss'.format(
                round,
            )
        ),
        content=content,
    )
    return


@job
def save_csa_report(competitor):
    content = competitor.get_csa()
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
def save_csa_round(round):
    content = round.get_csa()
    round.csa.save(
        slugify(
            '{0} csa'.format(
                round,
            )
        ),
        content=content,
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
    try:
        result = email.send()
    except Exception as e:
        raise(e)
    if result != 1:
        raise RuntimeError("Email unsuccessful {0}".format(entry))
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
    try:
        result = email.send()
    except Exception as e:
        raise(e)
    if result != 1:
        raise RuntimeError("Email unsuccessful {0}".format(entry))
    return

