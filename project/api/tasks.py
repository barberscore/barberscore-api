import logging
from django.apps import apps as api_apps
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django_rq import job


log = logging.getLogger(__name__)
config = api_apps.get_app_config('api')


@job
def echo_back(foo):
    return foo


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


@job
def send_session(context, template):
    session = context['session']
    Group = config.get_model('Group')
    Assignment = config.get_model('Assignment')
    groups = Group.objects.filter(
        status=Group.STATUS.active,
        organization__grantors__session=session,
        kind=session.kind,
    )
    assignments = session.convention.assignments.filter(
        category__lt=Assignment.STATUS.active,
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
