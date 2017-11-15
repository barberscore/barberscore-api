# Standard Libary
import logging

# Third-Party
import docraptor

# Third-Party
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0
from auth0.v3.management.rest import Auth0Error

from django.conf import settings
from django.core.cache import cache


# Django
from django.apps import apps as api_apps
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

log = logging.getLogger(__name__)
config = api_apps.get_app_config('api')


def get_auth0():
    if cache['auth0_api_access_token']:
        access_token = cache['auth0_api_access_token']
    else:
        client = GetToken(settings.AUTH0_DOMAIN)
        token = client.client_credentials(
            settings.AUTH0_API_ID,
            settings.AUTH0_API_SECRET,
            settings.AUTH0_AUDIENCE,
        )
        cache.set(
            'auth0_api_access_token',
            token['access_token'],
            timeout=token['expires_in'],
        )
        access_token = token['access_token']
    auth0 = Auth0(
        settings.AUTH0_DOMAIN,
        access_token,
    )
    return auth0


def create_or_update_auth0_account_from_user(user):
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
    # Create or Update Auth0
    if user.auth0_id:
        response = auth0.users.update(payload)
        created = False
    else:
        response = auth0.users.create(payload)
        created = True
    return response, created


def create_pdf(payload):
    docraptor.configuration.username = settings.DOCRAPTOR_API_KEY
    client = docraptor.DocApi()
    return client.create_doc(payload)


def send_session(session, template):
    Group = config.get_model('Group')
    groups = Group.objects.filter(
        status=10,
        organization__grantors__convention=session.convention,
        kind=session.kind,
    )
    assignments = session.convention.assignments.filter(
        category__lt=10,
    ).exclude(person__email=None)
    ccs = ["{0} <{1}>".format(assignment.person.common_name, assignment.person.email) for assignment in assignments]
    for group in groups:
        try:
            contacts = group.members.filter(
                is_admin=True,
            ).exclude(person__email=None)
            if not contacts:
                log.error(
                    "No valid contacts for {0}".format(
                        group,
                    )
                )
                continue

            tos = ["{0} <{1}>".format(contact.person.common_name, contact.person.email) for contact in contacts]
            ccs = ccs
            rendered = render_to_string(template, {'session': session, 'group': group})
            subject = "[Barberscore] {0}".format(
                group.nomen,
            )
            email = EmailMessage(
                subject=subject,
                body=rendered,
                from_email='Barberscore <admin@barberscore.com>',
                to=tos,
                cc=ccs,
                bcc=[
                    'admin@barberscore.com',
                    'proclamation56@gmail.com',
                ],
            )
            result = email.send()
            if result == 1:
                log.info(
                    "{0}".format(
                        group.nomen,
                    )
                )
            else:
                log.error(
                    "{0}".format(
                        group.nomen,
                    )
                )
        except Exception as e:
            log.error(e)
            continue
