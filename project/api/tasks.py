import logging
from django.apps import apps as api_apps
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django_rq import job

import docraptor
from django.conf import settings

log = logging.getLogger(__name__)
config = api_apps.get_app_config('api')


@job
def create_pdf(payload):
    docraptor.configuration.username = settings.DOCRAPTOR_API_KEY
    client = docraptor.DocApi()
    return client.create_doc(payload)


@job
def send_entry(context, template):
    entry = context['entry']
    contacts = entry.group.members.filter(
        is_admin=True,
    ).exclude(person__email=None)
    if not contacts:
        log.error("No valid contacts for {0}".format(entry))
        return
    assignments = entry.session.convention.assignments.filter(
        category__lt=10,
    ).exclude(person__email=None)
    tos = ["{0} <{1}>".format(contact.person.common_name, contact.person.email) for contact in contacts]
    ccs = ["{0} <{1}>".format(assignment.person.common_name, assignment.person.email) for assignment in assignments]
    rendered = render_to_string(template, context)
    subject = "[Barberscore] {0}".format(entry.nomen)
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
    try:
        result = email.send()
    except Exception as e:
        log.error("{0} {1}".format(e, entry))
        raise(e)
    if result != 1:
        log.error("{0} {1}".format(e, entry))
        raise RuntimeError("Email unsuccessful {0}".format(entry))
    return


@job
def send_session(context, template):
    session = context['session']
    Group = config.get_model('Group')
    Member = config.get_model('Member')
    Assignment = config.get_model('Assignment')
    contacts = Member.objects.filter(
        is_admin=True,
        group__status=Group.STATUS.active,
        group__organization__grantors__convention=session.convention,
        group__kind=session.kind,
    ).exclude(person__email=None)
    assignments = Assignment.objects.filter(
        convention=session.convention,
        category=Assignment.CATEGORY.drcj,
        status=Assignment.STATUS.active,
    ).exclude(person__email=None)
    to = ["{0} <{1}>".format(assignment.person.common_name, assignment.person.email) for assignment in assignments]
    bcc = ["{0} <{1}>".format(contact.person.common_name, contact.person.email) for contact in contacts]
    bcc.extend([
        'Barberscore Admin <admin@barberscore.com>',
        'David Mills <proclamation56@gmail.com>',
    ])
    rendered = render_to_string(template, context)
    subject = "[Barberscore] {0}".format(session.nomen)
    email = EmailMessage(
        subject=subject,
        body=rendered,
        from_email='Barberscore <admin@barberscore.com>',
        to=to,
        bcc=bcc,
    )
    return email.send()
