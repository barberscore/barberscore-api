# Local
from .base import *

# Heroku
ALLOWED_HOSTS = [
    'testserver',
    'localhost',
]

# Static Files
CLOUDINARY_URL = get_env_variable("CLOUDINARY_URL")
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Email
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
