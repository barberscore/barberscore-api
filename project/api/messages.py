# Standard Libary
import logging

# Django
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

log = logging.getLogger(__name__)


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
