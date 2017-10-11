# Standard Libary
import logging

# Third-Party
import docraptor

# Django
from django.apps import apps as api_apps
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

log = logging.getLogger(__name__)
config = api_apps.get_app_config('api')


def create_pdf(payload):
    docraptor.configuration.username = settings.DOCRAPTOR_API_KEY
    client = docraptor.DocApi()
    return client.create_doc(payload)


def send_entry(entry, template):
    contacts = entry.group.members.filter(
        is_admin=True,
    ).exclude(person__email=None)
    if not contacts:
        log.error(
            "No valid contacts for {0}".format(
                entry,
            )
        )
        return

    assignments = entry.session.convention.assignments.filter(
        category__lt=10,
    ).exclude(person__email=None)
    tos = ["{0} <{1}>".format(contact.person.common_name, contact.person.email) for contact in contacts]
    ccs = ["{0} <{1}>".format(assignment.person.common_name, assignment.person.email) for assignment in assignments]
    rendered = render_to_string(template, {'entry': entry})
    subject = "[Barberscore] {0}".format(
        entry.nomen,
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
                entry.nomen,
            )
        )
    else:
        log.error(
            "{0}".format(
                entry.nomen,
            )
        )


def send_session(session, template):
    Group = config.get_model('Group')
    groups = Group.objects.filter(
        status=10,
        organization__grantors__session=session,
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
