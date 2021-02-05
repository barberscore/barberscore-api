
# Standard Library
import logging

# Third-Party
from django_fsm import TransitionNotAllowed
from pprint import pprint

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings

from .models import SfSession

from .tasks import update_or_create_session_from_salesforce
from .tasks import update_or_create_contest_from_salesforce

import untangle

@csrf_exempt
def data_import(request, **kwargs):
    # pprint(vars(request))

    # Ensure POST request
    if request.method == 'POST':
        # Parse XML
        obj = untangle.parse(request.body.decode('utf-8')).soapenv_Envelope.soapenv_Body.notifications

        # Ensure OrganizaitonID
        if obj.OrganizationId.cdata is not None and obj.OrganizationId.cdata in settings.SALESFORCE_ORGANIZATIONS:
            for elem in obj.Notification:
                if "Session" in elem.sObject['xsi:type']:
                    __session(elem)

            return HttpResponse(str(len(obj.Notification)) + ' Notifications Imported')
        else:
            return HttpResponse('OrganizationId not validated')
    else:
        return HttpResponse('This should fail!')

def __session(notification):
    session = SfSession.parse_sf_notification(notification.sObject)
    update_or_create_session_from_salesforce.delay(session)
    print('====Import Queued====')
