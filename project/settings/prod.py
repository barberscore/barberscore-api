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


# Heroku Settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

# AWS Global Settings
AWS_ACCESS_KEY_ID = get_env_variable("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env_variable("AWS_SECRET_ACCESS_KEY")
AWS_PRELOAD_METADATA = True
AWS_REGION = get_env_variable("AWS_DEFAULT_REGION")

# AWS S3 Static Settings (public-read, static resources like CSS, Images, etc.)
AWS_S3_KEY_PREFIX_STATIC = "static"
AWS_S3_BUCKET_NAME_STATIC = "{0}".format(PROJECT_NAME)
AWS_S3_MAX_AGE_SECONDS_STATIC = 60 * 60 * 24 * 365  # 1 year
STATIC_STORAGE = 'django_s3_storage.storage.StaticS3Storage'
STATICFILES_STORAGE = STATIC_STORAGE

# AWS S3 Media Settings (user or admin-uploaded content)
AWS_S3_KEY_PREFIX = "files"
AWS_S3_BUCKET_NAME = "{0}".format(PROJECT_NAME)
AWS_S3_MAX_AGE_SECONDS = 60 * 60  # 1 hour
MEDIA_STORAGE = 'django_s3_storage.storage.S3Storage'
DEFAULT_FILE_STORAGE = MEDIA_STORAGE

# CORS Settings
CORS_ORIGIN_WHITELIST = [
    '{0}.com'.format(PROJECT_NAME),
    '{0}.s3.amazonaws.com'.format(PROJECT_NAME),
    '{0}.auth0.com'.format(PROJECT_NAME),
]

#  Bugsnag
BUGSNAG = {
    "api_key": get_env_variable("BUGSNAG_API_KEY"),
    "project_root": PROJECT_ROOT,
}
MIDDLEWARE = [
    'bugsnag.django.middleware.BugsnagMiddleware',
] + MIDDLEWARE

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = get_env_variable("SENDGRID_USERNAME")
EMAIL_HOST_PASSWORD = get_env_variable("SENDGRID_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'root': {
        'level': get_env_variable('DJANGO_LOG_LEVEL'),
        'handlers': ['bugsnag'],
    },

    'handlers': {
        'bugsnag': {
            'level': get_env_variable('DJANGO_LOG_LEVEL'),
            'class': 'bugsnag.handlers.BugsnagHandler',
        },
    }
}

INSTALLED_APPS += [
    'django_s3_storage',
]
