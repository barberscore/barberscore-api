# Local
from .base import *

# Heroku
ALLOWED_HOSTS = [
    'testserver',
    'localhost',
]

# Redis
RQ_QUEUES['default']['ASYNC'] = False
RQ_QUEUES['high']['ASYNC'] = False

# Algolia
ALGOLIA['INDEX_SUFFIX'] = 'test'
ALGOLIA['AUTO_INDEXING'] = False

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
