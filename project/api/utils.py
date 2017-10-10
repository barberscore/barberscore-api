# Standard Libary
import csv
import logging
import sys
from urllib.parse import urljoin

# Third-Party
import requests
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0
from cloudinary.uploader import upload
from openpyxl import Workbook

# Django
from django.apps import apps as api_apps
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone

config = api_apps.get_app_config('api')
from bhs.models import Structure

log = logging.getLogger(__name__)


def export_active_quartets():
    with open('active_quartets.csv', 'w') as f:
        output = []
        fieldnames = [
            'id',
            'name',
            'bhs_id',
            'district',
        ]
        quartets = Structure.objects.filter(
            kind='quartet',
            status__name='active'
        )
        for quartet in quartets:
            pk = str(quartet.id)
            try:
                name = quartet.name.strip()
            except AttributeError:
                name = '(UNKNOWN)'
            bhs_id = quartet.bhs_id
            district = str(quartet.parent)
            row = {
                'id': pk,
                'name': name,
                'bhs_id': bhs_id,
                'district': district,
            }
            output.append(row)
        writer = csv.DictWriter(
            f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for row in output:
            writer.writerow(row)


def do_org_sort(root):
    i = 1
    root.org_sort = i
    root.save()
    for child in root.children.order_by('kind', 'name'):
        i += 1
        child.org_sort = i
        child.save()
        for grandchild in child.children.filter(kind=21).order_by('kind', 'name'):
            i += 1
            grandchild.org_sort = i
            grandchild.save()


def update_officers():
    now = timezone.now()
    officers = Member.objects.filter(end_date__gt=now)
    for officer in officers:
        officer.status = Officer.STATUS.active
        officer.save()
        # log.info(officer)
    # now = timezone.now()
    # officers = Member.objects.filter(end_date__lte=now)
    # for officer in officers:
        # officer.status = Officer.STATUS.inactive
        # officer.save()
        # log.info(officer)


def update_members():
    now = timezone.now()
    members = Member.objects.filter(end_date__lte=now)
    for member in members:
        member.status = Member.STATUS.inactive
        member.save()
        # log.info(member)
    members = Member.objects.filter(end_date__gt=now)
    for member in members:
        member.status = Member.STATUS.active
        member.save()
        # log.info(member)


def get_auth0_token():
    client = GetToken(settings.AUTH0_DOMAIN)
    token = client.client_credentials(
        settings.AUTH0_API_ID,
        settings.AUTH0_API_SECRET,
        settings.AUTH0_AUDIENCE,
    )
    return token['access_token']


def get_requests_token():
    url = 'https://barberscore-dev.auth0.com/oauth/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': settings.AUTH0_API_ID,
        'client_secret': settings.AUTH0_API_SECRET,
        'audience': settings.AUTH0_AUDIENCE,
    }
    response = requests.post(url, data=data)
    return response


def get_auth0_me(token):
    url = urljoin("https://{0}".format(settings.AUTH0_DOMAIN), 'userinfo')
    headers = {
        'Authorization': 'Bearer {0}'.format(token)
    }
    response = requests.get(url, headers=headers)
    return response


def update_auth0_id(user):
    token = get_auth0_token()
    auth0 = Auth0(
        settings.AUTH0_DOMAIN,
        token,
    )
    result = auth0.users.list(
        search_engine='v2',
        q='email:"{0}"'.format(user.email),
    )
    if result['length'] != 1:
        return log.error("Error {0}".format(user))
    auth0_id = result['users'][0]['user_id']
    user.auth0_id = auth0_id
    user.save()
    return log.info("Updated {0}".format(user))


def get_requests_token():
    url = 'https://barberscore-dev.auth0.com/oauth/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': settings.AUTH0_API_ID,
        'client_secret': settings.AUTH0_API_SECRET,
        'audience': settings.AUTH0_AUDIENCE,
    }
    response = requests.post(url, data=data)
    return response


def impersonate(user):
    token = get_auth0_token()
    impersonator_id = 'email|599e62507cd3126297fa63bc'.partition('|')[2]
    url = "https://{0}/users/{1}/impersonate".format(
        settings.AUTH0_DOMAIN,
        user.auth0_id,
    )
    headers = {
        'Authorization': 'Bearer {0}'.format(token),
    }
    data = {
        'protocol': 'oauth2',
        'impersonator_id': impersonator_id,
        'client_id': settings.AUTH0_CLIENT_ID,
        'additionalParameters': {
            'response_type': 'code',
            'callback_url': 'http://localhost:4200/login',
            'scope': 'openid profile',
        },
    }
    response = requests.post(url, data=data, headers=headers)
    return response


def send_link(user):
    token = get_auth0_token()
    impersonator_id = 'email|599e62507cd3126297fa63bc'.partition('|')[2]
    url = "https://{0}/users/{1}/impersonate".format(
        settings.AUTH0_DOMAIN,
        user.auth0_id,
    )
    headers = {
        'Authorization': 'Bearer {0}'.format(token),
    }
    data = {
        'protocol': 'oauth2',
        'impersonator_id': impersonator_id,
        'client_id': settings.AUTH0_CLIENT_ID,
        'additionalParameters': {
            'response_type': 'code',
            'callback_url': 'http://localhost:4200/login',
            'scope': 'openid profile',
        },
    }
    response = requests.post(url, data=data, headers=headers)
    return response
# def create_account(person):
#     if not person.email:
#         raise RuntimeError("No email")
#     user = User.objects.create_user(
#         person.email,
#     )
#     password = User.objects.make_random_password()
#     payload = {
#         "connection": "Default",
#         "email": person.email,
#         "password": password,
#         "user_metadata": {
#             "name": person.name
#         },
#         "app_metadata": {
#             "bhs_id": person.bhs_id,
#             "person_id": str(person.id),
#         }
#     }
#     auth0 = Auth0(
#         settings.AUTH0_DOMAIN,
#         settings.AUTH0_TOKEN,
#     )
#     response = auth0.users.create(payload)
#     sub_id = response['user_id']
#     payload2 = {
#         "result_url": "http://localhost:4200",
#         "user_id": sub_id,
#     }
#     response2 = auth0.tickets.create_pswd_change(payload2)
#     return response2['ticket']


# def export_bbscores(session):
#     output = []
#     fieldnames = [
#         'oa',
#         'contestant_id',
#         'group_name',
#         'group_type',
#         'song_number',
#         'song_title',
#     ]
#     entries = session.entries.order_by('entity__name')
#     for entry in entries:
#         try:
#             oa = entry.appearances.get(round__num=1).num
#         except Appearance.DoesNotExist:
#             continue
#         group_name = entry.entity.name
#         group_type = entry.entity.get_kind_display()
#         if group_type == 'Quartet':
#             contestant_id = entry.entity.bhs_id
#         elif group_type == 'Chorus':
#             contestant_id = entry.entity.code
#         else:
#             raise RuntimeError("Improper Entity Type")
#         i = 1
#         for repertory in entry.entity.repertories.order_by('chart__title'):
#             song_number = i
#             song_title = repertory.chart.title
#             i += 1
#             row = {
#                 'oa': oa,
#                 'contestant_id': contestant_id,
#                 'group_name': group_name,
#                 'group_type': group_type,
#                 'song_number': song_number,
#                 'song_title': song_title,
#             }
#             output.append(row)
#     writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, extrasaction='ignore')
#     writer.writeheader()
#     for row in output:
#         writer.writerow(row)
#     return


def create_bbscores(session):
    Entry = config.get_model('Entry')
    with open('bbscores.csv', 'w') as f:
        output = []
        fieldnames = [
            'oa',
            'contestant_id',
            'group_name',
            'group_type',
            'song_number',
            'song_title',
        ]
        entries = session.entries.filter(
            status=Entry.STATUS.approved,
        ).order_by('draw')
        for entry in entries:
            oa = entry.draw
            group_name = entry.group.name
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
                song_title = repertory.chart.title
                i += 1
                row = {
                    'oa': oa,
                    'contestant_id': contestant_id,
                    'group_name': group_name,
                    'group_type': group_type,
                    'song_number': song_number,
                    'song_title': song_title,
                }
                output.append(row)
        writer = csv.DictWriter(
            f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for row in output:
            writer.writerow(row)


def create_bbscores_excel(session):
    Entry = config.get_model('Entry')
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
        status=Entry.STATUS.approved,
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

    wb.save('bbscores.xlsx')


def create_drcj_report(session):
    Entry = config.get_model('Entry')
    Group = config.get_model('Group')
    with open('drcj_report.csv', 'w') as f:
        output = []
        fieldnames = [
            'oa',
            'group_name',
            'representing',
            'evaluation',
            'private',
            'bhs_id',
            'group_exp_date',
            'repertory_count',
            'particpant_count',
            'expiring_count',
            'directors',
            'awards',
            'persons',
            'chapters',
        ]
        entries = session.entries.filter(
            status=Entry.STATUS.approved,
        ).order_by('draw')
        for entry in entries:
            oa = entry.draw
            group_name = entry.group.name
            representing = entry.group.organization.name
            evaluation = entry.is_evaluation
            private = entry.is_private
            bhs_id = entry.group.bhs_id
            repertory_count = entry.group.repertories.filter(
                status__gt=0,
            ).count()
            group_exp_date = None
            repertory_count = entry.group.repertories.filter(
                status__gt=0,
            ).count()
            participants = entry.participants.all()
            participant_count = participants.count()
            expiring_count = participants.filter(
                member__valid_through__lte=session.convention.close_date,
            ).count()
            directors = entry.directors
            awards_list = []
            for contestant in entry.contestants.all().order_by('contest__award__name'):
                awards_list.append(contestant.contest.award.name)
            awards = "\n".join(filter(None, awards_list))
            persons_list = []
            chapters_list = []
            if entry.group.kind == entry.group.KIND.quartet:
                participants = entry.participants.all().order_by('member__part')
                for participant in participants:
                    persons_list.append(
                        participant.member.get_part_display(),
                    )
                    persons_list.append(
                        participant.member.person.nomen,
                    )
                    persons_list.append(
                        participant.member.person.email,
                    )
                    persons_list.append(
                        participant.member.person.phone,
                    )
                    if entry.group.kind == Group.KIND.chorus:
                        chapters = None
                        continue
                    person_chapter_list = []
                    for member in participant.member.person.members.filter(
                        status=10,
                        group__kind=Group.KIND.chorus,
                    ).distinct('group'):
                        person_chapter_list.append(
                            member.group.name,
                        )
                    chapters_list.extend(
                        person_chapter_list
                    )
                    list(set(chapters_list))
            chapters = "\n".join(filter(None, chapters_list))
            persons = "\n".join(filter(None, persons_list))
            row = {
                'oa': oa,
                'group_name': group_name,
                'representing': representing,
                'evaluation': evaluation,
                'private': private,
                'bhs_id': bhs_id,
                'group_exp_date': group_exp_date,
                'repertory_count': repertory_count,
                'particpant_count': participant_count,
                'expiring_count': expiring_count,
                'directors': directors,
                'awards': awards,
                'persons': persons,
                'chapters': chapters,
            }
            output.append(row)
        writer = csv.DictWriter(
            f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for row in output:
            writer.writerow(row)


def create_drcj_report_excel(session):
    Entry = config.get_model('Entry')
    Group = config.get_model('Group')
    Participant = config.get_model('Participant')
    wb = Workbook()
    ws = wb.active
    fieldnames = [
        'oa',
        'group_name',
        'representing',
        'evaluation',
        'private',
        'bhs_id',
        'group_exp_date',
        'repertory_count',
        'particpant_count',
        'expiring_count',
        'tenor',
        'lead',
        'baritone',
        'bass',
        'directors',
        'awards',
        'chapters',
    ]
    ws.append(fieldnames)
    entries = session.entries.filter(
        status=Entry.STATUS.approved,
    ).order_by('draw')
    for entry in entries:
        oa = entry.draw
        group_name = entry.group.name
        representing = entry.group.organization.name
        evaluation = entry.is_evaluation
        private = entry.is_private
        bhs_id = entry.group.bhs_id
        repertory_count = entry.group.repertories.filter(
            status__gt=0,
        ).count()
        group_exp_date = None
        repertory_count = entry.group.repertories.filter(
            status__gt=0,
        ).count()
        participants = entry.participants.all()
        participant_count = participants.count()
        expiring_count = participants.filter(
            member__valid_through__lte=session.convention.close_date,
        ).count()
        directors = entry.directors
        awards_list = []
        for contestant in entry.contestants.all().order_by('contest__award__name'):
            awards_list.append(contestant.contest.award.name)
        awards = "\n".join(filter(None, awards_list))
        parts = {}
        part = 1
        while part <= 4:
            try:
                participant = entry.participants.get(
                    part=part,
                )
            except Participant.DoesNotExist:
                parts[part] = None
                part += 1
                continue
            except Participant.MultipleObjectsReturned:
                parts[part] = None
                part += 1
                continue
            participant_list = []
            participant_list.append(
                participant.member.person.nomen,
            )
            participant_list.append(
                participant.member.person.email,
            )
            participant_list.append(
                participant.member.person.phone,
            )
            participant_detail = "\n".join(filter(None, participant_list))
            parts[part] = participant_detail
            part += 1
        chapters_list = []
        if entry.group.kind == entry.group.KIND.quartet:
            participants = entry.participants.all()
            for participant in participants:
                person_chapter_list = []
                for member in participant.member.person.members.filter(
                    status=10,
                    group__kind=Group.KIND.chorus,
                ).distinct('group'):
                    person_chapter_list.append(
                        member.group.name,
                    )
                chapters_list.extend(
                    person_chapter_list
                )
            dedupe = list(set(chapters_list))
            chapters = "\n".join(filter(None, dedupe))
        else:
            chapters = None
        row = [
            oa,
            group_name,
            representing,
            evaluation,
            private,
            bhs_id,
            group_exp_date,
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
    wb.save('drcj_report.xlsx')


def create_admin_emails_csv(session):
    Entry = config.get_model('Entry')
    with open('admin_emails.csv', 'w') as f:
        output = []
        fieldnames = [
            'group',
            'person',
            'email',
        ]
        entries = session.entries.filter(
            status=Entry.STATUS.approved,
        ).order_by('draw')
        for entry in entries:
            admins = entry.group.members.filter(
                is_admin=True,
            )
            for admin in admins:
                group = entry.group.nomen
                person = admin.person.nomen
                email = admin.person.email
                row = {
                    'group': group,
                    'person': person,
                    'email': email,
                }
                output.append(row)
        writer = csv.DictWriter(
            f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for row in output:
            writer.writerow(row)


def create_admin_emails_excel(session):
    Entry = config.get_model('Entry')
    wb = Workbook()
    ws = wb.active
    fieldnames = [
        'group',
        'admin',
        'email',
    ]
    ws.append(fieldnames)
    entries = session.entries.filter(
        status=Entry.STATUS.approved,
    ).order_by('draw')
    for entry in entries:
        admins = entry.group.members.filter(
            is_admin=True,
        )
        for admin in admins:
            group = entry.group.nomen.encode('utf-8').strip()
            person = admin.person.nomen.encode('utf-8').strip()
            email = admin.person.email.encode('utf-8').strip()
            row = [
                group,
                person,
                email,
            ]
            ws.append(row)
    wb.save('admin_emails.xlsx')


def export_charts():
    output = []
    fieldnames = [
        'id',
        'title',
        'arrangers',
        'composers',
        'lyricists',
    ]
    charts = Chart.objects.all()
    for chart in charts:
        row = {
            'id': chart.id.hex,
            'title': chart.title,
            'arrangers': chart.arrangers,
            'composers': chart.composers,
            'lyricists': chart.lyricists,
        }
        output.append(row)
    writer = csv.DictWriter(
        sys.stdout, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    for row in output:
        writer.writerow(row)
    return


def export_db_chapters():
    with open('chapters.csv', 'wb') as f:
        chapters = Entity.objects.filter(
            kind=Entity.KIND.chorus,
        ).exclude(
            parent=None,
        ).values()
        fieldnames = [
            'id',
            'nomen',
            'name',
            'status',
            'kind',
            'age',
            'is_novice',
            'short_name',
            'long_name',
            'code',
            'start_date',
            'end_date',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            'notes',
            'bhs_id',
            'parent_id',
            'parent',
        ]
        writer = csv.DictWriter(
            f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for chapter in chapters:
            parent = Entity.objects.get(
                id=str(chapter['parent_id']),
            )
            chapter['parent'] = parent.name
            try:
                writer.writerow(chapter)
            except UnicodeEncodeError:
                clean = {}
                for k, v in chapter.items():
                    try:
                        clean[k] = v.encode('ascii', 'replace')
                    except AttributeError:
                        clean[k] = v
                writer.writerow(clean)


def export_db_offices():
    with open('offices.csv', 'wb') as f:
        offices = Office.objects.all(
        ).values()
        fieldnames = [
            'id',
            'nomen',
            'name',
            'status',
            'kind',
            'short_name',
            'long_name',
        ]
        writer = csv.DictWriter(
            f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for office in offices:
            try:
                writer.writerow(office)
            except UnicodeEncodeError:
                clean = {}
                for k, v in office.items():
                    try:
                        clean[k] = v.encode('ascii', 'replace')
                    except AttributeError:
                        clean[k] = v
                writer.writerow(clean)


def export_db_awards():
    with open('awards.csv', 'wb') as f:
        awards = Award.objects.all(
        ).values()
        fieldnames = [
            'id',
            'nomen',
            'name',
            'status',
            'kind',
            'season',
            'size',
            'scope',
            'is_primary',
            'is_improved',
            'is_novice',
            'is_manual',
            'is_multi',
            'is_rep_qualifies',
            'rounds',
            'threshold',
            'minimum',
            'advance',
            'entity',
        ]
        writer = csv.DictWriter(
            f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for office in offices:
            try:
                writer.writerow(office)
            except UnicodeEncodeError:
                clean = {}
                for k, v in office.items():
                    try:
                        clean[k] = v.encode('ascii', 'replace')
                    except AttributeError:
                        clean[k] = v
                writer.writerow(clean)
