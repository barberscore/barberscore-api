import requests

from django_rq import job
from django.apps import apps
from django.conf import settings
#
from .serializers import PersonSerializer
from .serializers import GroupSerializer
from rest_framework_json_api.parsers import JSONParser
from django.contrib.auth import get_user_model



# Standard Library
import logging

# Third-Party
from django_rq import job
from auth0.v3.authentication import GetToken
from auth0.v3.exceptions import Auth0Error
from auth0.v3.management import Auth0
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils.crypto import get_random_string

from rest_framework_jwt.settings import api_settings
from django.forms.models import model_to_dict


log = logging.getLogger(__name__)

def get_membercenter_token():
    """
    Retrieve membercenter access_token.

    This also uses the cache so we're not re-instantiating for every update.
    """
    membercenter_api_access_token = cache.get('membercenter_api_access_token')
    if not membercenter_api_access_token:
        client = GetToken(api_settings.AUTH0_DOMAIN)
        response = client.client_credentials(
            api_settings.AUTH0_CLIENT_ID,
            api_settings.AUTH0_CLIENT_SECRET,
            api_settings.AUTH0_AUDIENCE,
        )
        cache.set(
            'membercenter_api_access_token',
            response['access_token'],
            timeout=response['expires_in'],
        )
        membercenter_api_access_token = response['access_token']
    return membercenter_api_access_token


def get_membercenter_response(source):
    source_type, _, source_pk = source.source_id.partition("|")
    if source_type != 'bhs':
        return ValueError("Source must be BHS")
    endpoint, _, token = settings.MEMBERCENTER_URL.partition('@')
    url = "{0}/bhs/{1}/{2}".format(
        endpoint,
        source._meta.model_name,
        source_pk,
    )
    headers = {
        'Authorization': 'Token {0}'.format(token)
    }
    response = requests.get(
        url,
        headers=headers,
    )
    return response

# @job('low')
def update_person_from_source(person):
    User = get_user_model()
    response = get_membercenter_response(person)
    human = response.json()
    parsed = JSONParser().parse_attributes(human['data'])
    serialized = PersonSerializer(person, data=parsed)
    if serialized.is_valid():
        usernames = parsed['usernames']
        owners = User.objects.filter(email__in=usernames).values_list('id', flat=True)
        return serialized.save(owners=owners)
    return serialized.errors

@job('low')
def update_person_from_membercenter(resource):
    Person = apps.get_model('bhs.person')
    User = get_user_model()
    source_id = "bhs|{0}".format(resource['id'])
    data = resource['attributes']
    data['source_id'] = source_id
    try:
        person = Person.objects.get(
            source_id=source_id,
        )
        serialized = PersonSerializer(person, data=data)
    except Person.DoesNotExist:
        serialized = PersonSerializer(data=data)
    if serialized.is_valid():
        usernames = data['usernames']
        owners = User.objects.filter(email__in=usernames).values_list('id', flat=True)
        return serialized.save(owners=owners)
    raise ValueError(serialized.errors)

@job('low')
def update_group_from_membercenter(resource):
    Group = apps.get_model('bhs.group')
    User = get_user_model()
    source_id = "bhs|{0}".format(resource['id'])
    data = resource['attributes']
    data['source_id'] = source_id
    try:
        group = Group.objects.get(
            source_id=source_id,
        )
        serialized = GroupSerializer(group, data=data)
    except Group.DoesNotExist:
        serialized = GroupSerializer(data=data)
    if serialized.is_valid():
        usernames = data['usernames']
        owners = User.objects.filter(email__in=usernames).values_list('id', flat=True)
        return serialized.save(owners=owners)
    raise ValueError(serialized.errors)

# def get_or_create_account_from_email(email):
#     auth0 = get_auth0()
#     results = auth0.users_by_email.search_users_by_email(email)
#     if results:
#         account = results[0]
#         created = False
#     else:
#         password = get_random_string()
#         payload = {
#             'connection': 'Default',
#             'email': email,
#             'email_verified': True,
#             'password': password,
#         }
#         account = auth0.users.create(payload)
#         created = True
#     return account, created


# @job('low')
# def update_account_from_user(user):
#     auth0 = get_auth0()
#     payload = model_to_dict(
#         user,
#         fields=[
#             'email',
#             'name',
#             'first_name',
#             'last_name',
#             'app_metadata',
#             'user_metadata',
#         ]
#     )
#     # Re-write payload to conform to Auth0
#     if user.image_url:
#         payload['picture'] = user.image_url
#     payload['given_name'] = payload.pop('first_name')
#     payload['family_name'] = payload.pop('last_name')
#     return auth0.users.update(user.username, payload)


# @job('low')
# def delete_account_from_user(user):
#     auth0 = get_auth0()
#     return auth0.users.delete(user.username)

# @job('low')
# def add_account_roles_from_user_pk_set(user, role, pk_set):
#     auth0 = get_auth0()
#     roles_raw = role.objects.filter(id__in=pk_set)
#     roles = [str(i.rolename) for i in roles_raw]
#     return auth0.users.add_roles(user.username, roles)

# @job('low')
# def remove_account_roles_from_user_pk_set(user, role, pk_set):
#     auth0 = get_auth0()
#     roles_raw = role.objects.filter(id__in=pk_set)
#     roles = [str(i.rolename) for i in roles_raw]
#     return auth0.users.remove_roles(user.username, roles)












# @job('low')
# def create_or_update_group_from_structure(structure):
#     Group = apps.get_model('bhs.group')
#     return Group.objects.update_or_create_from_structure(structure)


# @job('low')
# def create_or_update_person_from_human(human):
#     Person = apps.get_model('bhs.person')
#     return Person.objects.update_or_create_from_human(human)


# @job('low')
# def create_or_update_officer_from_role(role):
#     Officer = apps.get_model('bhs.officer')
#     return Officer.objects.update_or_create_from_role(role)

