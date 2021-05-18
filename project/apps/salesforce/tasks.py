import django
django.setup()

# Standard Library
import logging

# Third-Party
from django_rq import job

# Django
from apps.bhs.models import Convention, Award, Chart, Group, Person
from apps.registration.models import Contest, Session, Assignment, Entry

log = logging.getLogger(__name__)

@job('high')
def update_or_create_convention_from_salesforce(convention):
    return Convention.objects.update_or_create(pk=convention['id'], defaults=convention)

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
    return Contest.objects.update_or_create_contest(contest)

@job('high')
def update_or_create_assignment_from_salesforce(assignment):
    return Assignment.objects.update_or_create_assignment(assignment)

@job('high')
def update_or_create_entry_from_salesforce(entry):
    return Entry.objects.update_or_create_entry(entry)

@job('high')
def update_contest_entry_from_salesforce(entry):
	return Entry.objects.update_contestentry_status(entry)

@job('high')
def update_group_chart_from_salesforce(chart):
	return Group.objects.update_group_chart(chart)

@job('high')
def remove_record_from_salesforce(type, uuid):
    # convention
    if type == "bhs_Convention":
        return Convention.objects.filter(id=uuid).delete()

    # award
    elif type == "bhs_Award":
        return Award.objects.filter(id=uuid).delete()

    # chart
    elif type == "bhs_Chart":
        return Chart.objects.filter(id=uuid).delete()

    # group
    elif type == "Account":
        return Group.objects.filter(id=uuid).delete()

    # person
    elif type == "Contact":
        return Person.objects.filter(id=uuid).delete()

    # registration_session (should be already configured)
    elif type == "bhs_Session":
        return Session.objects.filter(id=uuid).delete()

    # registration_contest
    elif type == "bhs_Contest":
        return Contest.objects.filter(id=uuid).delete()

    # registration_assignment
    elif type == "bhs_Assignment":
        return Assignment.objects.filter(id=uuid).delete()

    # registration_entry
    elif type == "bhs_Entry":
        return Entry.objects.filter(id=uuid).delete()

    # # group_charts
    # elif type == "bhs_Repertory":
    #     return Group.objects.filter(id=uuid).delete()

    # # registration_entry_contests
    # elif type == "bhs_Entry_Contest":
    #     print("Type not configured for deletion: " + type)

    else:
        print("Type not configured for deletion: " + type)

    return
