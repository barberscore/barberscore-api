
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

# Django
from django.apps import apps
from django.conf import settings
from django.core.cache import cache
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.core.validators import ValidationError
from django.core.validators import validate_email
from django.db.models import Count
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.utils.timezone import localdate

log = logging.getLogger(__name__)

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
    auth0 = get_auth0()
    username = person.user.username
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
