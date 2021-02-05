import django
django.setup()

# Standard Library
import logging

# Third-Party
from django_rq import job

# Django
from apps.registration.models import Contest
from apps.registration.models import Session

log = logging.getLogger(__name__)

@job('high')
def update_or_create_contest_from_salesforce(contest):
    return Contest.objects.update_or_create_contest(contest)

@job('high')
def update_or_create_session_from_salesforce(session):
    return Session.objects.update_or_create_session(session)

@job('high')
def import_group(group):
    return 'add/update group'

@job('high')
def import_member(member):
    return 'add/update member'

@job('high')
def import_register_group(group):
    return 'register group for event'

@job('high')
def import_session(session):
    return 'register group for event'
