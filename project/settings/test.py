# Local
from .base import *


# Heroku Settings
ALLOWED_HOSTS = [
    'testserver',
]
DATABASES['default']['TEST'] = {
    'NAME': DATABASES['default']['NAME'],
}

#  Docraptor
DOCRAPTOR_API_KEY = None

# Cloudinary
CLOUDINARY_URL = None

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
