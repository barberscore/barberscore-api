
# Local
from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.rq import RqIntegration

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
# DATABASES['bhs_db'] = dj_database_url.parse(
#     get_env_variable("BHS_DATABASE_URL"),
#     conn_max_age=600,
# )
# DATABASE_ROUTERS = [
#     'routers.BHSRouter',
# ]

# Email
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = get_env_variable("SENDGRID_API_KEY")
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_HOST_USER = 'apikey'
# EMAIL_HOST_PASSWORD = get_env_variable("SENDGRID_API_KEY")
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

# Sentry
sentry_sdk.init(
    dsn=get_env_variable("SENTRY_DSN"),
    integrations=[
        DjangoIntegration(),
        RqIntegration(),
    ],
    send_default_pii=True,
    release=get_env_variable("HEROKU_RELEASE_VERSION")
)

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
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
}
