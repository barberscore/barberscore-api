import logging
import docraptor
from django.core.files.base import ContentFile
from django.template.loader import get_template
from .models import (
    Session,
)

log = logging.getLogger(__name__)
docraptor.configuration.username = "YOUR_API_KEY_HERE"
# docraptor.configuration.debug = True
doc_api = docraptor.DocApi()


def test_rap(message):
    session = Session.objects.get(id=message.content.get('pk'))
    foo = get_template('rap.html')
    template = foo.render(context={'session': session})
    try:
        create_response = doc_api.create_doc({
            "test": True,
            "document_content": template,
            "name": "{0}.pdf".format(message.content.get('pk')),
            "document_type": "pdf",
        })
        f = ContentFile(create_response)
        print type(f)
        session.scoresheet_pdf.save(
            "{0}.pdf".format(message.content.get('pk')),
            f
        )
        session.save()
        log.info("success")
    except docraptor.rest.ApiException as error:
        log.exception(error)
        log.exception(error.message)
        log.exception(error.code)
        log.exception(error.response_body)
    return
