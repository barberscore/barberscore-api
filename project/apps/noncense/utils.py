from django.conf import settings

from random import randint
from twilio.rest import TwilioRestClient

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def sendcode(mobile=None):
    ''' receives the request, and responds with nonce or error '''
    nonce = randint(1001, 9999)
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_from = settings.TWILIO_FROM_NUMBER
    client = TwilioRestClient(account_sid, auth_token)
    message = client.sms.messages.create(to=mobile, from_=twilio_from, body="%s" % (nonce))
    twilio_response = dict(mobile=message.to, nonce=message.body, twilio_sid=message.sid)
    return twilio_response
