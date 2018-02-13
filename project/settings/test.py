# Local
from .base import *

# Heroku
ALLOWED_HOSTS = [
    'testserver',
]

# Redis
RQ_QUEUES['default']['ASYNC'] = False

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
