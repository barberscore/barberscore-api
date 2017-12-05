# Local
# Third-Party
from cryptography import x509
from cryptography.hazmat.backends import default_backend

from .base import *

# Core
DEBUG = True

# Databases
# BHS_DATABASE_URL = get_env_variable("BHS_DATABASE_URL")
# DATABASES['bhs_db'] = dj_database_url.parse(BHS_DATABASE_URL, conn_max_age=0)
# DATABASES['bhs_db']['OPTIONS'] = {'ssl': {'ca': 'rds-combined-ca-bundle.pem'}}
# DATABASE_ROUTERS = [
#     'routers.BHSRouter',
# ]
# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Debug Toolbar
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

# Auth0
AUTH0_CLIENT_ID = get_env_variable("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = get_env_variable("AUTH0_CLIENT_SECRET")
AUTH0_DOMAIN = get_env_variable("AUTH0_DOMAIN")

AUTH0_API_ID = get_env_variable("AUTH0_API_ID")
AUTH0_API_SECRET = get_env_variable("AUTH0_API_SECRET")
AUTH0_AUDIENCE = get_env_variable("AUTH0_AUDIENCE")

# JWT Settings
with open('barberscore-dev.pem', 'rb') as f:
    pem_data = f.read()
cert = x509.load_pem_x509_certificate(pem_data, default_backend())
jwt_public_key = cert.public_key()


def jwt_get_username_from_payload_handler(payload):
    return payload.get('email')


JWT_AUTH = {
    'JWT_AUDIENCE': AUTH0_CLIENT_ID,
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': jwt_get_username_from_payload_handler,
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_PUBLIC_KEY': jwt_public_key,
    'JWT_ALGORITHM': 'RS256',
}

# Cloudinary
CLOUDINARY_URL = get_env_variable("CLOUDINARY_URL")

# Redis
RQ_QUEUES = {
    'default': {
        'URL': get_env_variable("REDIS_URL"),
        'DEFAULT_TIMEOUT': 360,
        'ASYNC': True,
    },
}
RQ_SHOW_ADMIN_LINK = True

# Logging
LOGGING = {
    'version': 1,
    "disable_existing_loggers": False,
    'loggers': {
        'api': {
            'level': 'DEBUG',
            'handlers': [
                'console',
            ],
        },
        'importer': {
            'level': 'DEBUG',
            'handlers': [
                'console',
            ],
        },
        'updater': {
            'level': 'DEBUG',
            'handlers': [
                'console',
            ],
        },
        'console': {
            'level': 'DEBUG',
            'handlers': [
                'console',
            ],
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
}

INSTALLED_APPS += [
    'debug_toolbar',
]
