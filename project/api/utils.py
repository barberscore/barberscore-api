# Standard Libary
import csv
import logging

# Third-Party
from auth0.v3.management import Auth0
import requests


# Django
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import (
    timezone,
)

from django.apps import apps as api_apps

config = api_apps.get_app_config('api')
# Local
# from .models import (
#     Award,
#     Chart,
#     Contestant,
#     Convention,
#     Entity,
#     Entry,
#     Office,
#     Officer,
#     Member,
#     Person,
#     Session,
#     User,
# )

log = logging.getLogger(__name__)


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
    url = 'https://barberscore.auth0.com/oauth/token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': settings.AUTH0_API_ID,
        'client_secret': settings.AUTH0_API_SECRET,
        'audience': settings.AUTH0_AUDIENCE,
    }
    response = requests.post(url, payload)
    json = response.json()
    return json['access_token']


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


def export_bbscores(session):
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
        entries = session.entries.order_by('entity__name')
        for entry in entries:
            try:
                oa = entry.appearances.get(round__num=1).num
            except Appearance.DoesNotExist:
                continue
            group_name = entry.entity.name
            group_type = entry.entity.get_kind_display()
            if group_type == 'Quartet':
                contestant_id = entry.entity.bhs_id
            elif group_type == 'Chorus':
                contestant_id = entry.entity.code
            else:
                raise RuntimeError("Improper Entity Type")
            i = 1
            for repertory in entry.entity.repertories.order_by('chart__title'):
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
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for row in output:
            writer.writerow(row)


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
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
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
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
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
            'is_district_representative',
            'rounds',
            'threshold',
            'minimum',
            'advance',
            'entity',
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
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
