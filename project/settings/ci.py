# Local
from .base import *


# JWT Settings
def jwt_get_username_from_payload_handler(payload):
    return payload.get('email')

JWT_AUTH = {
    # 'JWT_SECRET_KEY': AUTH0_CLIENT_SECRET,
    'JWT_AUDIENCE': AUTH0_CLIENT_ID,
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': jwt_get_username_from_payload_handler,
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_PUBLIC_KEY': jwt_public_key,
    'JWT_ALGORITHM': 'RS256',
}


# Static Server Config
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATIC_URL = 'static/'
STATICFILES_STORAGE = STATIC_STORAGE

# Media (aka File Upload) Server Config
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIA_URL = 'media/'
DEFAULT_FILE_STORAGE = MEDIA_STORAGE

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
