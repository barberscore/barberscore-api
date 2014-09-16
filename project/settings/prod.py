from .base import *

if get_env_variable("DJANGO_DEBUG") == 'True':
    DEBUG = True
else:
    DEBUG = False
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS += (
    'storages',
    'djrill',
    'raven.contrib.django.raven_compat',
)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# AWS S3  Settings
# This was hellaciously confusing to set up.  I'm subclassing storages in
# 'apps/barberscore/backends.py' and doing a lot of renaming below for clarity.
# `Static` means public-read, static resources like CSS, Images, etc.
# `Media` means private, user or admin-uploaded resources that have ACL
# by default (most notably, photos).

# Configure AWS variables
# Access credentials (global)
AWS_ACCESS_KEY_ID = get_env_variable("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env_variable("AWS_SECRET_ACCESS_KEY")
AWS_PRELOAD_METADATA = True
AWS_MEDIA_BUCKET_NAME = 'barberscore-files'
AWS_STATIC_BUCKET_NAME = 'barberscore-static'
AWS_MEDIA_FULL_URL = 'https://{0}.s3-us-west-1.amazonaws.com/'.format(AWS_MEDIA_BUCKET_NAME)


# Django Media Server configuration
MEDIA_STORAGE = 'utilities.backends.MediaS3BotoStorage'
MEDIA_ROOT = '/media/'
MEDIA_URL = 'https://s3-us-west-1.amazonaws.com/{0}/'.format(
    AWS_MEDIA_BUCKET_NAME,
)

# Django Static Server configuration
STATIC_STORAGE = 'utilities.backends.StaticS3BotoStorage'
STATIC_ROOT = '/static/'
STATIC_URL = 'https://s3-us-west-1.amazonaws.com/{0}/'.format(
    AWS_STATIC_BUCKET_NAME,
)

# Aliasing default settings.
DEFAULT_FILE_STORAGE = MEDIA_STORAGE
STATICFILES_STORAGE = STATIC_STORAGE
AWS_STORAGE_BUCKET_NAME = AWS_MEDIA_BUCKET_NAME
AWS_STORAGE_FULL_URL = AWS_MEDIA_FULL_URL

ADMIN_MEDIA_PREFIX = '{0}{1}'.format(STATIC_URL, 'admin/')

# /AWS S3

ALLOWED_HOSTS = [
    get_env_variable("HEROKU_HOST"),
    '.barberscore.com',
    '.barberscore.com',
    'heroku.barberscore.com.',
    'heroku.barberscore.com.',
]

EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'
# MANDRILL_API_KEY = get_env_variable("MANDRILL_APIKEY")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
