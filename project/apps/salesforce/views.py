
# Standard Library
import logging

# Third-Party
from django_fsm import TransitionNotAllowed
from pprint import pprint

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings

from .models import SfConvention, SfAward, SfChart, SfGroup, SfPerson, SfGroupChart
from .models import SfSession, SfContest, SfAssignment, SfEntry, SfEntryContest

from .tasks import update_or_create_convention_from_salesforce
from .tasks import update_or_create_award_from_salesforce
from .tasks import update_or_create_chart_from_salesforce
from .tasks import update_or_create_group_from_salesforce
from .tasks import update_or_create_person_from_salesforce
from .tasks import update_or_create_session_from_salesforce
from .tasks import update_or_create_contest_from_salesforce
from .tasks import update_or_create_assignment_from_salesforce
from .tasks import update_or_create_entry_from_salesforce
from .tasks import update_contest_entry_from_salesforce
from .tasks import update_group_chart_from_salesforce
from .tasks import delete_convention
from .tasks import delete_award
from .tasks import delete_chart
from .tasks import delete_group
from .tasks import delete_person
from .tasks import delete_session
from .tasks import delete_contest
from .tasks import delete_assignment
from .tasks import delete_entry
from .tasks import delete_repertory
from .tasks import delete_entry_contest

import untangle

from apps.registration.models import Contest, Session, Assignment, Entry


@csrf_exempt
def data_import(request, **kwargs):
    # Ensure POST request
    if request.method == 'POST':
        # Parse XML
        obj = untangle.parse(request.body.decode('utf-8')).soapenv_Envelope.soapenv_Body.notifications

        # Ensure OrganizaitonID
        if obj.OrganizationId.cdata is not None and obj.OrganizationId.cdata in settings.SALESFORCE_ORGANIZATIONS:
            processed = 0

            for elem in obj.Notification:

                processed += 1

                # convention
                if "bhs_Convention" in elem.sObject['xsi:type']:
                    __convention(elem.sObject)

                # award
                elif "bhs_Award" in elem.sObject['xsi:type']:
                    __award(elem.sObject)

                # chart
                elif "bhs_Chart" in elem.sObject['xsi:type']:
                    __chart(elem.sObject)

                # group
                elif "Account" in elem.sObject['xsi:type']:
                    __group(elem.sObject)

                # person
                elif "Contact" in elem.sObject['xsi:type']:
                    __person(elem.sObject)

                # registration_session (should be already configured)
                elif "bhs_Session" in elem.sObject['xsi:type']:
                    __session(elem.sObject)

                # registration_contest
                elif "bhs_Contest" in elem.sObject['xsi:type']:
                    __contest(elem.sObject)

                # registration_assignment
                elif "bhs_Assignment" in elem.sObject['xsi:type']:
                    __assignment(elem.sObject)

                # registration_entry_contests
                elif "bhs_Entry_Contest" in elem.sObject['xsi:type']:
                    __entry_contest(elem.sObject)

                # registration_entry
                elif "bhs_Entry" in elem.sObject['xsi:type']:
                    __entry(elem.sObject)

                # group_charts
                elif "bhs_Repertory" in elem.sObject['xsi:type']:
                    __group_chart(elem.sObject)

                # Delete entries
                elif "bhs_Barberscore_Delete" in elem.sObject['xsi:type']:
                    __delete_entry(elem.sObject)

                else:
                    # THis means it wasn't an approved type
                    processed -= 1

                # group_charts --- No BS model exists

            print(str(processed) + ' Notifications Imported')
            return render(request, 'response.xml', { 'status': 'true' }, content_type='application/xml')
        else:
            print('OrganizationId not validated')
            return render(request, 'response.xml', { 'status': 'false' }, content_type='application/xml')
    else:
        print('This should fail!')
        return render(request, 'response.xml', { 'status': 'false' }, content_type='application/xml')

def __convention(data):
    convention = SfConvention.parse_sf_notification(data)
    update_or_create_convention_from_salesforce.delay(convention)
    print('====Convention Import Queued====')

def __award(data):
    award = SfAward.parse_sf_notification(data)
    update_or_create_award_from_salesforce.delay(award)
    print('====Award Import Queued====')

def __chart(data):
    chart = SfChart.parse_sf_notification(data)
    update_or_create_chart_from_salesforce.delay(chart)
    print('====Chart Import Queued====')

def __group(data):
    group = SfGroup.parse_sf_notification(data)
    update_or_create_group_from_salesforce.delay(group)
    print('====Group Import Queued====')

def __person(data):
    person = SfPerson.parse_sf_notification(data)
    update_or_create_person_from_salesforce.delay(person)
    print('====Person Import Queued====')

def __session(data):
    session = SfSession.parse_sf_notification(data)
    update_or_create_session_from_salesforce.delay(session)
    print('====Session Import Queued====')

def __contest(data):
    contest = SfContest.parse_sf_notification(data)
    update_or_create_contest_from_salesforce.delay(contest)
    print('====Contest Import Queued====')

def __assignment(data):
    assignment = SfAssignment.parse_sf_notification(data)
    update_or_create_assignment_from_salesforce.delay(assignment)
    print('====Assignment Import Queued====')

def __entry(data):
    entry = SfEntry.parse_sf_notification(data)
    update_or_create_entry_from_salesforce.delay(entry)
    print('====Entry Import Queued====')

def __entry_contest(data):
    entry = SfEntryContest.parse_sf_notification(data)
    update_contest_entry_from_salesforce.delay(entry)
    print('====Entry Contests Import Queued====')

def __group_chart(data):
    chart = SfGroupChart.parse_sf_notification(data)
    update_group_chart_from_salesforce.delay(chart)
    print('====Group Chart Import Queued====')

deletion = {
    'bhs_Convention': delete_convention,
    'bhs_Award': delete_award,
    'bhs_Chart': delete_chart,
    'Account': delete_group,
    'Contact': delete_person,
    'bhs_Session': delete_session,
    'bhs_Contest': delete_contest,
    'bhs_Assignment': delete_assignment,
    'bhs_Entry': delete_entry
}

def __delete_entry(data):
    uuid = data.sf_Object_Key__c.cdata
    recordType = data.sf_Object_Name__c.cdata

    if recordType in deletion:
        deletion[recordType].delay(uuid)

    # group_charts
    elif recordType == "bhs_Repertory":
        chart = {
            'group_id': data.sf_Object_Key__c.cdata,
            'chart_id': data.sf_Foreign_Key__c.cdata,
            'deleted': "true"
        }
        delete_repertory.delay(chart)

    # registration_entry_contests
    elif recordType == "bhs_Entry_Contest_Xref":
        entry = {
            'entry_id': data.sf_Object_Key__c.cdata,
            'contest_id': data.sf_Foreign_Key__c.cdata,
            'deleted': "true"
        }
        delete_entry_contest.delay(entry)


    # remove_record_from_salesforce.delay(recordType, uuid, data)
    print('====Delete Entries Queued====')
