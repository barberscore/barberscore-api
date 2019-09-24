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


@job('low')
def update_person_from_membercenter(resource):
    Person = apps.get_model('bhs.person')
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
        return serialized.save()
    raise ValueError(serialized.errors)


@job('low')
def update_group_from_membercenter(resource):
    Group = apps.get_model('bhs.group')
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
        owners = [x['id'] for x in resource['relationships']['owners']['data']]
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



@job('low')
def update_group_from_source(group):
    source, _, pk = group.source_id.partition("|")
    # Only supports Member Center currently
    if source != 'bhs':
        return ValueError("Not BHS")
    endpoint, _, token = settings.MEMBERCENTER_URL.partition('@')
    url = "{0}/bhs/group/{1}".format(endpoint, pk)
    headers = {
        'Authorization': 'Token {0}'.format(token)
    }
    response = requests.get(
        url,
        headers=headers,
    )
    if not response.ok:
        raise RuntimeError("Bad Response")
    resource = response.json()['data']
    data = resource['attributes']
    serialized = GroupSerializer(group, data=data)
    if serialized.is_valid():
        owners = [x['id'] for x in resource['relationships']['owners']['data']]
        return serialized.save(owners=owners)
    raise ValueError(serialized.errors)


from collections import defaultdict
from django.db.models.signals import *


class DisableSignals(object):
    def __init__(self, disabled_signals=None):
        self.stashed_signals = defaultdict(list)
        self.disabled_signals = disabled_signals or [
            pre_init, post_init,
            pre_save, post_save,
            pre_delete, post_delete,
            pre_migrate, post_migrate,
        ]

    def __enter__(self):
        for signal in self.disabled_signals:
            self.disconnect(signal)

    def __exit__(self, exc_type, exc_val, exc_tb):
        for signal in list(self.stashed_signals):
            self.reconnect(signal)

    def disconnect(self, signal):
        self.stashed_signals[signal] = signal.receivers
        signal.receivers = []

    def reconnect(self, signal):
        signal.receivers = self.stashed_signals.get(signal, [])
        del self.stashed_signals[signal]

