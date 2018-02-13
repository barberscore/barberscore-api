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

# Cloudinary
CLOUDINARY_URL = None
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
