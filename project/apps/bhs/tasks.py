import requests

from django_rq import job
from django.apps import apps
from django.conf import settings
#
from .serializers import PersonSerializer
from .serializers import GroupSerializer
from rest_framework_json_api.parsers import JSONParser
from django.contrib.auth import get_user_model
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

# @job('low')
def update_person_from_source(person):
    User = get_user_model()
    source_type, _, source_pk = person.source_id.partition("|")
    if source_type != 'bhs':
        return
    response = requests.get('http://localhost:8000/bhs/person/{0}'.format(source_pk))
    human = response.json()
    parsed = JSONParser().parse_attributes(human['data'])
    serialized = PersonSerializer(person, data=parsed)
    if serialized.is_valid():
        usernames = parsed['usernames']
        owners = User.objects.filter(email__in=usernames).values_list('id', flat=True)
        return serialized.save(owners=owners)
    return serialized.errors

def update_group_from_source(group):
    User = get_user_model()
    source_type, _, source_pk = group.source_id.partition("|")
    if source_type != 'bhs':
        return
    response = requests.get('http://localhost:8000/bhs/group/{0}'.format(source_pk))
    human = response.json()
    parsed = JSONParser().parse_attributes(human['data'])
    serialized = GroupSerializer(group, data=parsed)
    if serialized.is_valid():
        usernames = parsed['usernames']
        owners = User.objects.filter(email__in=usernames).values_list('id', flat=True)
        return serialized.save(owners=owners)
    return serialized.errors
