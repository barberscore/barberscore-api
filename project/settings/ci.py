# Local
from .base import *

# Static Server Config
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATIC_URL = '/static/'
STATICFILES_STORAGE = STATIC_STORAGE

# Media (aka File Upload) Server Config
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = MEDIA_STORAGE

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
