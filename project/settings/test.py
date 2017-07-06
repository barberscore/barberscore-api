# Local
from .base import *

# Heroku
ALLOWED_HOSTS = [
    'testserver',
]
DATABASES['default']['TEST'] = {
    'NAME': DATABASES['default']['NAME'],
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#  Docraptor
DOCRAPTOR_API_KEY = get_env_variable("DOCRAPTOR_API_KEY")
