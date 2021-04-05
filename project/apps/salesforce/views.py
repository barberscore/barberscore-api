
# Standard Library
import logging

# Third-Party
from django_fsm import TransitionNotAllowed
from pprint import pprint

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings

from .models import SfConvention, SfAward, SfChart, SfGroup, SfPerson
from .models import SfSession, SfContest, SfAssignment, SfEntry

from .tasks import update_or_create_convention_from_salesforce
from .tasks import update_or_create_award_from_salesforce
from .tasks import update_or_create_chart_from_salesforce
from .tasks import update_or_create_group_from_salesforce
from .tasks import update_or_create_person_from_salesforce
from .tasks import update_or_create_session_from_salesforce
from .tasks import update_or_create_contest_from_salesforce
from .tasks import update_or_create_assignment_from_salesforce
from .tasks import update_or_create_entry_from_salesforce

import untangle

@csrf_exempt
def data_import(request, **kwargs):
    # Ensure POST request
    if request.method == 'POST':
        # Parse XML
        obj = untangle.parse(request.body.decode('utf-8')).soapenv_Envelope.soapenv_Body.notifications

        # Ensure OrganizaitonID
        if obj.OrganizationId.cdata is not None and obj.OrganizationId.cdata in settings.SALESFORCE_ORGANIZATIONS:
            for elem in obj.Notification:

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

                # registration_entry
                elif "bhs_Entry" in elem.sObject['xsi:type']:
                    __entry(elem.sObject)

                # group_charts --- No BS model exists
                # registration_entry_contests --- no BS model exists 

            return HttpResponse(str(len(obj.Notification)) + ' Notifications Imported')
        else:
            return HttpResponse('OrganizationId not validated')
    else:
        return HttpResponse('This should fail!')

def __convention(data):
    print(data.sf_BS_Kind__c.cdata)
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
