import django
django.setup()

# Standard Library
import logging
import time

# Third-Party
from django_rq import job, get_queue

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
def update_or_create_contest_from_salesforce(contest, max_retries=10):
    queue = get_queue('high')

    # print('Search for SessionID + ' + contest['session_id'])

    #
    # Query Session to see if session_id record exists
    # 

    if max_retries > 0:
        if Session.objects.filter(pk=contest['session_id']).count():
            return Contest.objects.update_or_create_contest(contest)
        else:
            time.sleep(60)
            queue.enqueue(update_or_create_contest_from_salesforce, args=(contest, (max_retries - 1)))
    else:
        raise ObjectDoesNotExist("Session ID not found: " + contest['session_id'])

@job('high')
def update_or_create_assignment_from_salesforce(assignment):
    return Assignment.objects.update_or_create_assignment(assignment)

@job('high')
def update_or_create_entry_from_salesforce(entry):
    return Entry.objects.update_or_create_entry(entry)

@job('high')
def update_contest_entry_from_salesforce(entry, max_retries=10):
    queue = get_queue('high')

    print('Search for EntryID + ' + entry['entry_id'])

    #
    # Query Entry to see if entry_id record exists
    # 

    print("max_retries: " + max_retries)

    if max_retries > 0:
        print("reached")
        if Entry.objects.filter(pk=entry['entry_id']).count():
            print("reached")
            return Entry.objects.update_contestentry_status(entry)
        else:
            print("sleep")
            time.sleep(60)
            queue.enqueue(update_contest_entry_from_salesforce, args=(entry, (max_retries - 1)))
    else:
        print("entry ID not found")
        raise ObjectDoesNotExist("Entry ID not found: " + entry['entry_id'])


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
