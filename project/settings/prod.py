
# Local
from .base import *

# Core
DEBUG = False
HOST_NAME = 'https://api.barberscore.com'
ALLOWED_HOSTS = [
    '.barberscore.com',
    '.herokuapp.com',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
SECURE_SSL_REDIRECT = True

# Database
DATABASES['bhs_db'] = dj_database_url.parse(
    get_env_variable("BHS_DATABASE_URL"),
    conn_max_age=600,
)
DATABASE_ROUTERS = [
    'routers.BHSRouter',
]

# Email
# EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
# SENDGRID_SANDBOX_MODE_IN_DEBUG = False
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = get_env_variable("SENDGRID_API_KEY")
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Sentry
RAVEN_CONFIG = {
    'environment': 'production',
    'dsn': get_env_variable("SENTRY_DSN"),
    'release': get_env_variable("HEROKU_SLUG_DESCRIPTION"),
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'django': {
            'handlers': [
                'console',
            ],
            'level': 'INFO',
        },
        'api': {
            'handlers': [
                'console',
            ],
            'level': 'INFO',
        },
        'importer': {
            'handlers': [
                'console',
            ],
            'level': 'INFO',
        },
        'updater': {
            'handlers': [
                'console',
            ],
            'level': 'INFO',
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': [
                'console'
            ],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': [
                'console'
            ],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': [
                'console'
            ],
            'propagate': False,
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
    },
}

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat',
]
