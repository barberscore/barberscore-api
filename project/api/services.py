# Standard Libary
import logging

# Third-Party

# Third-Party
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

from django.conf import settings
from django.core.cache import cache


# Django
from django.apps import apps as api_apps

log = logging.getLogger(__name__)
config = api_apps.get_app_config('api')


def get_auth0():
    auth0_api_access_token = cache.get('auth0_api_access_token')
    if not auth0_api_access_token:
        client = GetToken(settings.AUTH0_DOMAIN)
        response = client.client_credentials(
            settings.AUTH0_API_ID,
            settings.AUTH0_API_SECRET,
            settings.AUTH0_AUDIENCE,
        )
        cache.set(
            'auth0_api_access_token',
            response['access_token'],
            timeout=response['expires_in'],
        )
        auth0_api_access_token = response['access_token']
    auth0 = Auth0(
        settings.AUTH0_DOMAIN,
        auth0_api_access_token,
    )
    return auth0


def create_auth0_account_from_user(user):
    auth0 = get_auth0()
    # Build payload
    payload = {
        "connection": "email",
        "email": user.email,
        "email_verified": True,
        "user_metadata": {
            "name": user.name
        },
        "app_metadata": {
            "barberscore_id": str(user.id),
        }
    }
    # Create Auth0 Account
    response = auth0.users.create(payload)
    return response


def update_auth0_account_from_user(user):
    auth0 = get_auth0()
    # Build payload
    payload = {
        "connection": "email",
        "email": user.email,
        "email_verified": True,
        "user_metadata": {
            "name": user.name
        },
        "app_metadata": {
            "barberscore_id": str(user.id),
        }
    }
    # Update Auth0 Account
    response = auth0.users.update(user.auth0_id, payload)
    return response


def delete_auth0_account_from_user(user):
    auth0 = get_auth0()
    # Delete Auth0
    if user.auth0_id:
        response = auth0.users.delete(user.auth0_id)
    return response


# def get_requests_token():
#     url = 'https://barberscore-dev.auth0.com/oauth/token'
#     data = {
#         'grant_type': 'client_credentials',
#         'client_id': settings.AUTH0_API_ID,
#         'client_secret': settings.AUTH0_API_SECRET,
#         'audience': settings.AUTH0_AUDIENCE,
#     }
#     response = requests.post(url, data=data)
#     return response


# def get_auth0_me(token):
#     url = urljoin("https://{0}".format(settings.AUTH0_DOMAIN), 'userinfo')
#     headers = {
#         'Authorization': 'Bearer {0}'.format(token)
#     }
#     response = requests.get(url, headers=headers)
#     return response


# def update_auth0_id(user):
#     token = get_auth0_token()
#     auth0 = Auth0(
#         settings.AUTH0_DOMAIN,
#         token,
#     )
#     result = auth0.users.list(
#         search_engine='v2',
#         q='email:"{0}"'.format(user.email),
#     )
#     if result['length'] != 1:
#         return log.error("Error {0}".format(user))
#     auth0_id = result['users'][0]['user_id']
#     user.auth0_id = auth0_id
#     user.save()
#     return log.info("Updated {0}".format(user))


# def impersonate(user):
#     token = get_auth0_token()
#     impersonator_id = 'email|599e62507cd3126297fa63bc'.partition('|')[2]
#     url = "https://{0}/users/{1}/impersonate".format(
#         settings.AUTH0_DOMAIN,
#         user.auth0_id,
#     )
#     headers = {
#         'Authorization': 'Bearer {0}'.format(token),
#     }
#     data = {
#         'protocol': 'oauth2',
#         'impersonator_id': impersonator_id,
#         'client_id': settings.AUTH0_CLIENT_ID,
#         'additionalParameters': {
#             'response_type': 'code',
#             'callback_url': 'http://localhost:4200/login',
#             'scope': 'openid profile',
#         },
#     }
#     response = requests.post(url, data=data, headers=headers)
#     return response


# def send_link(user):
#     token = get_auth0_token()
#     impersonator_id = 'email|599e62507cd3126297fa63bc'.partition('|')[2]
#     url = "https://{0}/users/{1}/impersonate".format(
#         settings.AUTH0_DOMAIN,
#         user.auth0_id,
#     )
#     headers = {
#         'Authorization': 'Bearer {0}'.format(token),
#     }
#     data = {
#         'protocol': 'oauth2',
#         'impersonator_id': impersonator_id,
#         'client_id': settings.AUTH0_CLIENT_ID,
#         'additionalParameters': {
#             'response_type': 'code',
#             'callback_url': 'http://localhost:4200/login',
#             'scope': 'openid profile',
#         },
#     }
#     response = requests.post(url, data=data, headers=headers)
#     return response
