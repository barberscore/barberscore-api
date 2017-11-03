# Local
from .base import *

# Heroku
ALLOWED_HOSTS = [
    'testserver',
]

DATABASES['default']['TEST'] = {
    'NAME': DATABASES['default']['NAME'],
}

RQ_QUEUES['default']['ASYNC'] = False


# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
