# Local
from .base import *

# Heroku
ALLOWED_HOSTS = [
    'testserver',
    'localhost',
]

# Overwrite database settings
DATABASES.pop('bhs_db', None)
DATABASE_ROUTERS = []

# Staticfiles
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Email
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
