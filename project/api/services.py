from django.conf import settings
import docraptor

def create_pdf(payload):
    docraptor.configuration.username = settings.DOCRAPTOR_API_KEY
    client = docraptor.DocApi()
    return client.create_doc(payload)
