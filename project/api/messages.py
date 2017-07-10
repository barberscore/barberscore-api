# Standard Libary
import logging

# Django
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

log = logging.getLogger(__name__)


def send_entry(entry, template, context):
    officers = entry.entity.officers.filter(
        office__is_group_manager=True,
    )
    assignments = entry.session.convention.assignments.filter(
        category__lt=10,
    )
    recipients = ["{0} <{1}>".format(officer.person.common_name, officer.person.email) for officer in officers]
    contacts = ["{0} <{1}>".format(assignment.person.common_name, assignment.person.email) for assignment in assignments]
    rendered = render_to_string(template, context)
    subject = "{0} {1} for {2}".format(
        entry.session.nomen,
        context['details'],
        entry.entity.name,
    )
    email = EmailMessage(
        subject=subject,
        body=rendered,
        from_email='Barberscore <admin@barberscore.com>',
        to=recipients,
        cc=contacts,
    )
    result = email.send()
    if result == 1:
        log.info(
            "Sent {0} for {1}".format(
                context['details'],
                entry,
            )
        )
    else:
        log.error(
            "FAILED {0} for {1}".format(
                context['details'],
                entry,
            )
        )
