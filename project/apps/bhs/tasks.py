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
        owners = []
        for username in usernames:
            defaults = {
                'name': data['name'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
            }
            user, _ = User.objects.update_or_create(
                email=data['email'],
                defaults=defaults,
            )
            owners.append(user.id)
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
        owners = User.objects.filter(username__in=usernames).values_list('id', flat=True)
        return serialized.save(owners=owners)
    raise ValueError(serialized.errors)


@job('low')
def update_group_owners_from_membercenter(resource):
    Group = apps.get_model('bhs.group')
    Person = apps.get_model('bhs.person')
    User = get_user_model()
    group_source_id = "bhs|{0}".format(resource['relationships']['group']['data']['id'])
    person_source_id = "bhs|{0}".format(resource['relationships']['person']['data']['id'])
    group = Group.objects.get(
        source_id=group_source_id,
    )
    person = Person.objects.get(
        source_id=person_source_id,
    )
    if person.email:
        defaults = {
            'name': person.name,
            'first_name': person.first_name,
            'last_name': person.last_name,
        }
        user, _ = User.objects.update_or_create(
            email=person.email,
            defaults=defaults,
        )
        if resource['attributes']['status'] > 0:
            return group.owners.add(user)
        return group.owners.remove(user)
    return
