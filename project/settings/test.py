# Local
from .base import *

# Heroku
ALLOWED_HOSTS = [
    'testserver',
    'localhost',
]

# Email
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
