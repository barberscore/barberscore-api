# Standard Libary
import logging

# Third-Party
import docraptor
# Third-Party
from auth0.v3.management import Auth0
from auth0.v3.management.rest import Auth0Error

from django.conf import settings
from api.utils import get_auth0_token


# Django
from django.apps import apps as api_apps
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

log = logging.getLogger(__name__)
config = api_apps.get_app_config('api')


def get_auth0():
    token = get_auth0_token()
    return Auth0(
        settings.AUTH0_DOMAIN,
        token,
    )


def get_auth0_users(auth0):
    lst = []
    more = True
    i = 0
    t = 0
    while more:
        results = auth0.users.list(
            fields=[
                'user_id',
                'email',
                'app_metadata',
                'user_metadata',
            ],
            per_page=100,
            page=i,
        )
        try:
            payload = [result for result in results['users']]
        except KeyError:
            t += 1
            if t > 3:
                break
            else:
                continue
        lst.extend(payload)
        more = bool(results['users'])
        i += 1
        t = 0
    return lst


def generate_payload(user):
    if user.person.email != user.email:
        user.email = user.person.email
        user.save()
    email = user.email

    name = user.name
    barberscore_id = str(user.id)
    payload = {
        "connection": "email",
        "email": email,
        "email_verified": True,
        "user_metadata": {
            "name": name
        },
        "app_metadata": {
            "barberscore_id": barberscore_id,
        }
    }
    return payload


def update_auth0_from_user(user):
    user.email = user.person.email
    user.name = user.person.nomen
    user.save()
    # Get the Auth0 instance
    auth0 = get_auth0()
    payload = {
        'email': user.email,
        'user_metadata': {
            'name': user.name,
        },
        'app_metadata': {
            'barberscore_id': str(user.id),
        },
    }
    account = auth0.users.update(user.auth0_id, payload)
    log.info("UPDATED: {0}".format(account['user_id']))
    return


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
