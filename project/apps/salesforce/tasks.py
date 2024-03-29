import django
django.setup()

# Standard Library
import logging
import time

# Third-Party
from django_rq import job, get_queue
from rq import Retry

# Django
from apps.bhs.models import Convention, Award, Chart, Group, Person
from apps.registration.models import Contest, Session, Assignment, Entry
from django.core.exceptions import ObjectDoesNotExist

log = logging.getLogger(__name__)

@job('high')
def update_or_create_convention_from_salesforce(convention):
    return Convention.objects.update_or_create_convention(convention)

@job('high')
def update_or_create_award_from_salesforce(award):
    return Award.objects.update_or_create_award(award)

@job('high')
def update_or_create_chart_from_salesforce(chart):
    return Chart.objects.update_or_create_chart(chart)

@job('high')
def update_or_create_group_from_salesforce(group):
    return Group.objects.update_or_create_group(group)

@job('high')
def update_or_create_person_from_salesforce(person):
    return Person.objects.update_or_create_person(person)

@job('high')
def update_or_create_session_from_salesforce(session):
    return Session.objects.update_or_create_session(session)

@job('high')
def update_or_create_contest_from_salesforce(contest):
    queue = get_queue('high')

    #
    # Query Session to see if session_id record exists
    # 

    if Session.objects.filter(pk=contest['session_id']).count():
        return Contest.objects.update_or_create_contest(contest)
    else:
        queue.enqueue(update_or_create_contest_from_salesforce, args=(contest), 
            retry=Retry(max=10, 
                interval=[60, 120, 180, 240, 300, 360, 420, 480, 540, 600]))

@job('high')
def update_or_create_assignment_from_salesforce(assignment):
    return Assignment.objects.update_or_create_assignment(assignment)

@job('high')
def update_or_create_entry_from_salesforce(entry):
    return Entry.objects.update_or_create_entry(entry)

@job('high')
def update_contest_entry_from_salesforce(entry):
    queue = get_queue('high')

    #
    # Query Entry to see if entry_id record exists
    # 

    if Entry.objects.filter(pk=entry['entry_id']).count():
        return Entry.objects.update_contestentry_status(entry)
    else:
        queue.enqueue(update_contest_entry_from_salesforce, args=(entry), 
            retry=Retry(max=10, 
                interval=[60, 120, 180, 240, 300, 360, 420, 480, 540, 600]))

@job('high')
def update_group_chart_from_salesforce(chart):
	return Group.objects.update_group_chart(chart)


# Delete Jobs

@job('high')
def delete_convention(uuid):
    return Convention.objects.filter(id=uuid).delete()

@job('high')
def delete_award(uuid):
    return Award.objects.filter(id=uuid).delete()

@job('high')
def delete_chart(uuid):
    return Chart.objects.filter(id=uuid).delete()

@job('high')
def delete_group(uuid):
    return Group.objects.filter(id=uuid).delete()

@job('high')
def delete_person(uuid):
    return Person.objects.filter(id=uuid).delete()

@job('high')
def delete_session(uuid):
    return Session.objects.filter(id=uuid).delete()

@job('high')
def delete_contest(uuid):
    return Contest.objects.filter(id=uuid).delete()

@job('high')
def delete_assignment(uuid):
    return Assignment.objects.filter(id=uuid).delete()

@job('high')
def delete_entry(uuid):
    return Entry.objects.filter(id=uuid).delete()

@job('high')
def delete_repertory(chart):
    return Group.objects.update_group_chart(chart)

@job('high')
def delete_entry_contest(entry):
    return Entry.objects.update_contestentry_status(entry)
