from django.conf import settings

from twilio.rest import TwilioRestClient

from random import randint


def get_nonce():
    return randint(1001, 9999)


def sendcode(mobile, nonce):
    '''Sends an SMS over twilio with the included payload'''
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_from = settings.TWILIO_FROM_NUMBER
    client = TwilioRestClient(account_sid, auth_token)
    twilio_response = client.sms.messages.create(
        to=mobile,
        from_=twilio_from,
        body=nonce,
    )
    return twilio_response

# def test_twilio_sms(mobile, body):
#     '''Sends an SMS over twilio with the included payload'''
#     account_sid = 'ACb1b9bca9ccef183757e6ebdb64d063c3'
#     auth_token = '41bd31f387ba44b7bfd7cf4965ce06f7'
#     twilio_from = settings.TWILIO_FROM_NUMBER
#     client = TwilioRestClient(account_sid, auth_token)
#     message = client.sms.messages.create(
#         to=mobile,
#         from_=twilio_from,
#         body=body,
#     )
#     return message
