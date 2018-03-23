# Standard Libary
# Debug Toolbar
from .base import *

HOST_NAME = 'http://localhost:8000'
DEBUG = True
ALLOWED_HOSTS = [
    'localhost',
]
INTERNAL_IPS = [
    '127.0.0.1',
]


EMAIL_PORT = 1025

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE

MIDDLEWARE += [
    'querycount.middleware.QueryCountMiddleware',
]


DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]


# Auth0 - COPIED until i can mock
AUTH0_CLIENT_ID = get_env_variable("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = get_env_variable("AUTH0_CLIENT_SECRET")
AUTH0_CLIENT_DOMAIN = get_env_variable("AUTH0_CLIENT_DOMAIN")
AUTH0_API_ID = get_env_variable("AUTH0_API_ID")
AUTH0_API_SECRET = get_env_variable("AUTH0_API_SECRET")
AUTH0_API_DOMAIN = get_env_variable("AUTH0_API_DOMAIN")



def jwt_get_username_from_payload_handler(payload):
    """Switch to email as JWT username payload."""
    return payload.get('email')

from cryptography import x509
from cryptography.hazmat.backends import default_backend

pem_data = get_env_variable("AUTH0_CERTIFICATE")
pem_data = pem_data.encode()

cert = x509.load_pem_x509_certificate(pem_data, default_backend())
jwt_public_key = cert.public_key()

JWT_AUTH = {
    'JWT_AUDIENCE': AUTH0_CLIENT_ID,
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': jwt_get_username_from_payload_handler,
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_PUBLIC_KEY': jwt_public_key,
    'JWT_ALGORITHM': 'RS256',
}

RQ_QUEUES['default']['ASYNC'] = False
RQ_QUEUES['high']['ASYNC'] = False

# Algolia
ALGOLIA = {
    'APPLICATION_ID': get_env_variable("ALGOLIASEARCH_APPLICATION_ID"),
    'API_KEY': get_env_variable("ALGOLIASEARCH_API_KEY"),
    'ALGOLIASEARCH_AUTO_INDEXING': False,
    'INDEX_SUFFIX': 'dev',
}
# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'api': {
            'handlers': [
                'console',
            ],
            'level': 'DEBUG',
        },
        'importer': {
            'handlers': [
                'console',
                'logfile',
            ],
            'level': 'DEBUG',
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
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'dev.log'),
            'maxBytes': 5000000,
            'backupCount': 10,
            'formatter': 'standard',
        },
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
}

INSTALLED_APPS += [
    'algoliasearch_django',
    'debug_toolbar',
    'whitenoise.runserver_nostatic',
]
