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

# deletion = {
#     'bhs_Convention': delete_convention,
#     'bhs_Award': delete_award,
#     'bhs_Chart': delete_chart,
#     'Account': delete_group,
#     'Contact': delete_person,
#     'bhs_Session': delete_session,
#     'bhs_Contest': delete_contest,
#     'bhs_Assignment': delete_assignment,
#     'bhs_Entry': delete_entry
# }

# @job('high')
# def remove_record_from_salesforce(type, uuid, data):

#     if type in deletion:
#         deletion[type](uuid)

#     # group_charts
#     elif type == "bhs_Repertory":
#         chart = {
#             'group_id': data.sf_Object_Key__c.cdata,
#             'chart_id': data.sf_Foreign_Key__c.cdata,
#             'deleted': "true"
#         }
#         return Group.objects.update_group_chart(chart)

#     # registration_entry_contests
#     elif type == "bhs_Entry_Contest_Xref":
#         entry = {
#             'entry_id': data.sf_Object_Key__c.cdata,
#             'contest_id': data.sf_Foreign_Key__c.cdata,
#             'deleted': "true"
#         }
#         return Entry.objects.update_contestentry_status(entry)

#     else:
#         print("Type not configured for deletion: " + type)
#         return
