# Standard Libary
import logging
import time
from django.core.files.base import ContentFile
# Third-Party
import pydf
from auth0.v3.authentication import GetToken
from auth0.v3.exceptions import Auth0Error
from auth0.v3.management import Auth0
from django_rq import job
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

# Django
from django.apps import apps
from django.conf import settings
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.core.validators import validate_email

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


def get_accounts():
    auth0 = get_auth0()
    output = []
    more = True
    i = 0
    t = 0
    while more:
        print(i, t)
        try:
            results = auth0.users.list(
                fields=[
                    'user_id',
                ],
                per_page=100,
                page=i,
            )
        except Auth0Error as e:
            t += 1
            if t <= 5:
                time.sleep(t ** 2)
                continue
            else:
                raise e
        try:
            users = results['users']
        except KeyError as e:
            t += 1
            if t <= 5:
                time.sleep(t ** 2)
                continue
            else:
                raise e
        for user in users:
            payload = {
                'username': user['user_id'],
            }
            output.append(payload)
        more = bool(results['users'])
        i += 1
        t = 0
    return output


@job
def activate_user(user):
    Person = apps.get_model('api.person')
    auth0 = get_auth0()
    account = auth0.users.get(user.username)
    person = Person.objects.get(email=account['email'])
    user.person = person
    user.save()
    return user


@job
def delete_account(user):
    auth0 = get_auth0()
    # Delete Auth0
    auth0.users.delete(user.username)
    return


@job
def update_account(user):
    auth0 = get_auth0()
    name = user.person.__str__()
    email = user.person.email.lower()
    payload = {
        'email': email,
        'email_verified': True,
        'user_metadata': {
            'name': name,
        }
    }
    account = auth0.users.update(user.username, payload)
    return account


@job
def create_account(email, name):
    auth0 = get_auth0()
    email = email.lower()
    random = get_random_string()
    payload = {
        'email': email,
        'email_verified': True,
        'password': random,
        'user_metadata': {
            'name': name,
        }
    }
    account = auth0.users.create(payload)
    return account


@job
def create_account_from_person(person):
    # TODO Not sure we're keeping this
    auth0 = get_auth0()
    email = person.email.lower()
    name = person.__str__()
    random = get_random_string()
    payload = {
        'connection': 'Default',
        'email': email,
        'email_verified': True,
        'password': random,
        'user_metadata': {
            'name': name,
        }
    }
    account = auth0.users.create(payload)
    return account


@job
def update_account_from_person(person):
    # TODO Not sure we're keeping this
    auth0 = get_auth0()
    name = person.__str__()
    email = person.email.lower()
    payload = {
        'email': email,
        'email_verified': True,
        'user_metadata': {
            'name': name,
        }
    }
    account = auth0.users.update(person.user.username, payload)
    return account


# @job
# def update_or_create_account_from_user(user, blocked):
#     # Get the auth0 client
#     auth0 = get_auth0()
#     # Instantiate the created variable
#     created = True
#     # Try to get existing
#     if user.username.startswith('auth0'):
#         try:
#             # Flip the bit if you can find an account
#             account = auth0.users.get(user.username)
#             created = False
#         except Auth0Error as e:
#             # If you can't find the account legit then proceed
#             if not e.status_code == 404:
#                 # If there's a standard error, raise it.
#                 raise(e)
#     # Build payload
#     payload = {
#         "connection": "BHS",
#         "user_id": user.,
#         "email": user.email,
#         "email_verified": True,
#         "password": random,
#         "user_metadata": {
#             "name": user.__str__(),
#         },
#     }
#     if created:
#         # Create primary with payload if new
#         auth0.users.create(payload)
#         user.save()
#         # Now create secondary account
#         random = get_random_string()
#         secondary_payload = {
#             "connection": "Default",
#             "email": user.email,
#             "password": random,
#             "email_verified": True,
#         }
#         secondary_account = auth0.users.create(secondary_payload)
#         secondary_id = secondary_account['user_id']
#         secondary_body = {
#             'provider': 'auth0',
#             'user_id': secondary_id,
#         }
#         auth0.users.link_user_account(
#             account_id,
#             secondary_body,
#         )
#     else:
#         # Only update if there are diffs
#         try:
#             dirty = any([
#                 account['email'] != user.email,
#                 account['user_metadata']['name'] != user.name,
#                 account['app_metadata']['barberscore_id'] != str(user.id),
#                 # account['blocked'] != blocked,
#             ])
#         except KeyError:
#             dirty = True
#         if dirty:
#             account = auth0.users.update(user.account_id, payload)
#     return account, created


# @job
# def link_secondary_account_from_user(user):
#     # Get the auth0 client
#     auth0 = get_auth0()
#     # Create random initial password
#     random = get_random_string()
#     # Create the payload
#     secondary_payload = {
#         "connection": "Default",
#         "email": user.email,
#         "password": random,
#         "email_verified": True,
#     }
#     secondary_account = auth0.users.create(secondary_payload)
#     secondary_id = secondary_account['user_id']
#     secondary_body = {
#         'provider': 'auth0',
#         'user_id': secondary_id,
#     }
#     response = auth0.users.link_user_account(
#         user.account_id,
#         secondary_body,
#     )
#     return response


@job
def create_account_from_human(human):
    validate_email(human.email)
    # Get the auth0 client
    auth0 = get_auth0()
    # Build payload
    name = human.__str__()
    random = get_random_string()
    payload = {
        "user_id": human.id,
        "connection": "Default",
        "email": human.email,
        "password": random,
        "email_verified": True,
        "user_metadata": {
            "name": name
        },
    }
    account = auth0.users.create(payload)
    return account

@job
def unlink_user_account(user):
    client = get_auth0()
    user_id = user.username.partition('|')[2]
    client.users.unlink_user_account(
        user.account_id,
        'auth0',
        user_id,
    )
    return

@job
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
        'Director(s)',
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
        participant_count = entry.mos
        members = entry.group.members.filter(
            status__gt=0,
        )
        expiring_count = members.filter(
            person__current_through__lte=session.convention.close_date,
        ).count()
        directors = entry.directors
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
            directors,
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
        expiration = member.person.current_through
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
        'panelist',
        'song__num',
    )
    panelists = Panelist.objects.filter(
        kind=Panelist.KIND.official,
        scores__song__appearance=appearance,
    ).order_by(
        'category',
        'person__last_name',
        'scores__song__num',
    )
    context = {
        'appearance': appearance,
        'songs': songs,
        'scores': scores,
        'panelists': panelists,
    }
    rendered = render_to_string('variance.html', context)
    file = pydf.generate_pdf(rendered)
    content = ContentFile(file)
    return content


@job
def create_ors_report(round):
    competitors = round.session.competitors.order_by(
        'rank',
        'tot_points'
    )
    panelists = round.panelists.filter(
        kind=round.panelists.model.KIND.official,
    ).order_by(
        'category',
    )
    contests = round.session.contests.filter(
        status__gt=0,
    ).order_by(
        '-award__is_primary',
        'award__name',
    )
    context = {
        'round': round,
        'competitors': competitors,
        'panelists': panelists,
        'contests': contests,
    }
    rendered = render_to_string('ors.html', context)
    file = pydf.generate_pdf(rendered)
    content = ContentFile(file)
    return content


@job
def create_oss_report(session):
    Panelist = apps.get_model('api.panelist')
    competitors = session.competitors.order_by(
        'rank',
        'tot_points'
    )
    rounds = session.rounds.all()
    panelists = Panelist.objects.filter(
        kind=Panelist.KIND.official,
        round__in=rounds,
    ).order_by(
        'category',
    )
    contests = session.contests.filter(
        status__gt=0,
    ).order_by(
        '-award__is_primary',
        'award__name',
    )
    context = {
        'session': session,
        'competitors': competitors,
        'panelists': panelists,
        'contests': contests,
    }
    rendered = render_to_string('oss.html', context)
    file = pydf.generate_pdf(rendered)
    content = ContentFile(file)
    return content


@job
def create_csa_report(competitor):
    Panelist = apps.get_model('api.panelist')
    panelists = Panelist.objects.filter(
        kind=Panelist.KIND.official,
        scores__song__appearance__competitor=competitor,
    ).distinct(
    ).order_by(
        'category',
        'person__last_name',
    )
    appearances = competitor.appearances.order_by(
        'round__num',
    )
    # contests = session.contests.filter(
    #     status__gt=0,
    # ).order_by(
    #     '-award__is_primary',
    #     'award__name',
    # )
    context = {
        'competitor': competitor,
        'panelists': panelists,
        'appearances': appearances,
    }
    rendered = render_to_string('csa.html', context)
    file = pydf.generate_pdf(rendered)
    content = ContentFile(file)
    return content


@job
def create_sa_report(session):
    Person = apps.get_model('api.person')
    persons = Person.objects.filter(
        panelists__round__session=session,
    ).distinct(
    ).order_by(
        'panelists__category',
        'panelists__kind',
        'last_name',
        'first_name',
    )
    competitors = session.competitors.order_by('rank')
    context = {
        'session': session,
        'persons': persons,
        'competitors': competitors,
    }
    rendered = render_to_string('sa.html', context)
    file = pydf.generate_pdf(rendered)
    content = ContentFile(file)
    return content


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


@job
def update_bhs_member(member):
    Join = apps.get_model('bhs.join')
    Member = apps.get_model('api.member')
    joins = Join.objects.filter(
        subscription__human__id=member.person.mc_pk,
        structure__id=member.group.mc_pk,
    ).order_by('modified')
    for join in joins:
        result = Member.objects.update_from_join(join)
    return result
