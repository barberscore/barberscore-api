from django.conf import settings

from twilio.rest import TwilioRestClient

from random import randint
import logging
log = logging.getLogger('apps.noncense')


def get_nonce():
    return randint(1001, 9999)


def sendcode(mobile):
    '''Sends an SMS over twilio with the included payload'''
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_from = settings.TWILIO_FROM_NUMBER
    client = TwilioRestClient(account_sid, auth_token)
    nonce = get_nonce()
    twilio_response = client.sms.messages.create(
        to=mobile,
        from_=twilio_from,
        body=nonce,
    )
    log.debug("{0}".format(nonce))
    return twilio_response.to, twilio_response.body
