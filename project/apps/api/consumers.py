import logging
import docraptor
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.template.loader import get_template
from .models import (
    Performer,
    Session,
)

log = logging.getLogger(__name__)
docraptor.configuration.username = "YOUR_API_KEY_HERE"
# docraptor.configuration.debug = True
doc_api = docraptor.DocApi()


def print_oss(message):
    id = message.content.get('id')
    session = Session.objects.get(id=id)
    performers = session.performers.order_by(
        '-total_points',
        '-sng_points',
        '-mus_points',
        '-prs_points',
    )
    judges = session.judges.all()
    foo = get_template('oss.html')
    template = foo.render(context={
        'session': session,
        'performers': performers,
        'judges': judges,
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
    performer = Performer.objects.get(id=id)
    contestants = performer.contestants.all()
    performances = performer.performances.order_by(
        'round__kind',
    )
    judges = performer.session.judges.all()
    foo = get_template('csa.html')
    template = foo.render(context={
        'performer': performer,
        'performances': performances,
        'judges': judges,
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
        performer.csa_pdf.save(
            "{0}.pdf".format(id),
            f
        )
        performer.save()
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
