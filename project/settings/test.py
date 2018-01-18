# Local
from .base import *

# Heroku
ALLOWED_HOSTS = [
    'testserver',
]

DATABASES['default']['TEST'] = {
    'NAME': DATABASES['default']['NAME'],
}

# Redis
RQ_QUEUES = {
    'default': {
        'URL': get_env_variable("REDIS_URL"),
        'DEFAULT_TIMEOUT': 360,
        'ASYNC': False,
    },
}
RQ_SHOW_ADMIN_LINK = True

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
