# Standard Libary
import logging

# Third-Party
import docraptor

# Django
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.template.loader import get_template

# Local
from .models import (
    Assignment,
    Entry,
    Round,
    Session,
)

log = logging.getLogger(__name__)
docraptor.configuration.username = settings.DOCRAPTOR_API_KEY
# docraptor.configuration.debug = True
doc_api = docraptor.DocApi()


def print_oss(message):
    id = message.content.get('id')
    session = Session.objects.get(id=id)
    entries = session.entries.filter(
        rank__gt=20,
    ).exclude(
        rank=None,
    ).order_by(
        '-total_points',
        '-sng_points',
        '-mus_points',
        '-prs_points',
    )
    assignments = session.assignments.order_by(
        'category',
        'kind',
        'slot',
    )
    foo = get_template('oss.html')
    template = foo.render(context={
        'session': session,
        'entries': entries,
        'assignments': assignments,
    })
    try:
        create_response = doc_api.create_doc({
            "test": True,
            "document_content": template,
            "name": "oss-{0}.pdf".format(id),
            "document_type": "pdf",
        })
        f = ContentFile(create_response)
        session.scoresheet_pdf.save(
            "{0}.pdf".format(id),
            f
        )
        session.save()
        log.info("PDF created and saved to instance")
    except docraptor.rest.ApiException as error:
        log.exception(error)
        log.exception(error.message)
        log.exception(error.code)
        log.exception(error.response_body)
    return


def print_csa(message):
    id = message.content.get('id')
    entry = Entry.objects.get(id=id)
    contestants = entry.contestants.all()
    appearances = entry.appearances.order_by(
        'round__kind',
    )
    assignments = entry.session.assignments.exclude(
        category=Assignment.CATEGORY.admin,
    ).order_by(
        'category',
        'kind',
        'slot',
    )
    foo = get_template('csa.html')
    template = foo.render(context={
        'entry': entry,
        'appearances': appearances,
        'assignments': assignments,
        'contestants': contestants,
    })
    try:
        create_response = doc_api.create_doc({
            "test": True,
            "document_content": template,
            "name": "csa-{0}.pdf".format(id),
            "document_type": "pdf",
        })
        f = ContentFile(create_response)
        entry.csa_pdf.save(
            "{0}.pdf".format(id),
            f
        )
        entry.save()
        log.info("PDF created and saved to instance")
    except docraptor.rest.ApiException as error:
        log.error(error)
        log.error(error.message)
        log.error(error.response_body)
    return


def print_ann(message):
    id = message.content.get('id')
    round = Round.objects.get(id=id)
    nxt = round.num + 1
    contests = round.session.contests.all()
    try:
        next_round = round.session.rounds.get(
            num=nxt,
        )
    except Round.DoesNotExist:
        next_round = None
    if next_round:
        advancing = next_round.appearances.order_by('num')
    else:
        advancing = None
    medalists = round.session.entries.filter(
        rank__lte=5,
    ).order_by('rank')
    foo = get_template('ann.html')
    template = foo.render(context={
        'round': round,
        'advancing': advancing,
        'contests': contests,
        'medalists': medalists,
    })
    try:
        create_response = doc_api.create_doc({
            "test": True,
            "document_content": template,
            "name": "ann-{0}.pdf".format(id),
            "document_type": "pdf",
        })
        f = ContentFile(create_response)
        round.ann_pdf.save(
            "{0}.pdf".format(id),
            f
        )
        round.save()
        log.info("PDF created and saved to instance")
    except docraptor.rest.ApiException as error:
        log.exception(error)
        log.exception(error.message)
        log.exception(error.code)
        log.exception(error.response_body)
    return


def send_email(message):
    to = message.content.get('to')
    subject = message.content.get('subject')
    body = message.content.get('body')
    response = send_mail(
        subject,
        body,
        'Nashville Beta Test <admin@barberscore.com>',
        to,
        fail_silently=False,
    )
    return response
