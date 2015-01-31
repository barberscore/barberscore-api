from .base import *

import sys

# AWS S3  Settings
# This was hellaciously confusing to set up.
# `Static` means public-read, static resources like CSS, Images, etc.
# `Media` means private, user or admin-uploaded resources that have ACL


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Configure AWS variables
# Access credentials (global)
AWS_ACCESS_KEY_ID = get_env_variable("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env_variable("AWS_SECRET_ACCESS_KEY")
AWS_PRELOAD_METADATA = True

# Static Server Config
AWS_STATIC_BUCKET_NAME = "{0}-static".format(PROJECT_NAME)
STATIC_STORAGE = 'utils.backends.StaticS3BotoStorage'
STATIC_URL = 'https://{0}.s3-us-west-1.amazonaws.com/'.format(
    AWS_STATIC_BUCKET_NAME,
)

# Media (aka File Upload) Server Config
AWS_MEDIA_BUCKET_NAME = "{0}-files".format(PROJECT_NAME)
MEDIA_STORAGE = 'utils.backends.MediaS3BotoStorage'
MEDIA_URL = 'https://{0}.s3-us-west-1.amazonaws.com/'.format(
    AWS_MEDIA_BUCKET_NAME,
)

# Aliasing Django Defaults
DEFAULT_FILE_STORAGE = MEDIA_STORAGE
STATICFILES_STORAGE = STATIC_STORAGE


EMAIL_BACKEND = 'adjrill.mail.backends.djrill.DjrillBackend'
MANDRILL_API_KEY = get_env_variable("MANDRILL_APIKEY")

BUGSNAG = {
    "api_key": get_env_variable("BUGSNAG_API_KEY"),
    "project_root": PROJECT_ROOT,
}

MIDDLEWARE_CLASSES += (
    "bugsnag.django.middleware.BugsnagMiddleware",
)

ALLOWED_HOSTS = [
    get_env_variable("HEROKU_HOST"),
    '.barberscore.com',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'ERROR',
        'handlers': ['bugsnag'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
    },
    'loggers': {
        'api': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
        'noncense': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
        'utils': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
    'handlers': {
        'bugsnag': {
            'level': 'ERROR',
            'class': 'bugsnag.handlers.BugsnagHandler',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout,
        },
    },
}

INSTALLED_APPS += (
    'djrill',
)
