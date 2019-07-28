
# Local
from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.rq import RqIntegration

# Core
ALLOWED_HOSTS = [
    '.barberscore.com',
    '.herokuapp.com',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
SECURE_SSL_REDIRECT = True


# Sentry
sentry_sdk.init(
    dsn=get_env_variable("SENTRY_DSN"),
    integrations=[
        DjangoIntegration(),
        RqIntegration(),
    ],
    send_default_pii=True,
    environment=get_env_variable("HEROKU_APP_NAME"),
)

# Email
EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
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
