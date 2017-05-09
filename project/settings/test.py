# Local
from .base import *


# Heroku Settings
ALLOWED_HOSTS = [
    'testserver',
]
DATABASES['default']['TEST'] = {
    'NAME': DATABASES['default']['NAME'],
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
