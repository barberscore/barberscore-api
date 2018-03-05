# Local
# Third-Party
from cryptography import x509
from cryptography.hazmat.backends import default_backend

from .base import *

# Core
DEBUG = True
ALLOWED_HOSTS = [
    'localhost',
]

# BHS Database
BHS_DATABASE_URL = get_env_variable("BHS_DATABASE_URL")
DATABASES['bhs_db'] = dj_database_url.parse(BHS_DATABASE_URL, conn_max_age=0)
DATABASES['bhs_db']['OPTIONS'] = {
    'ssl': {'ca': 'rds-combined-ca-bundle.pem'}}
DATABASE_ROUTERS = [
    'routers.BHSRouter',
]

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

# Auth0
AUTH0_CLIENT_ID = get_env_variable("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = get_env_variable("AUTH0_CLIENT_SECRET")
AUTH0_DOMAIN = get_env_variable("AUTH0_DOMAIN")

AUTH0_API_ID = get_env_variable("AUTH0_API_ID")
AUTH0_API_SECRET = get_env_variable("AUTH0_API_SECRET")
AUTH0_AUDIENCE = get_env_variable("AUTH0_AUDIENCE")

# JWT Settings
pem_data = b"""
-----BEGIN CERTIFICATE-----
MIIDDTCCAfWgAwIBAgIJPuLUYhcdfwcOMA0GCSqGSIb3DQEBCwUAMCQxIjAgBgNV
BAMTGWJhcmJlcnNjb3JlLWRldi5hdXRoMC5jb20wHhcNMTgwMjA5MTgyOTA2WhcN
MzExMDE5MTgyOTA2WjAkMSIwIAYDVQQDExliYXJiZXJzY29yZS1kZXYuYXV0aDAu
Y29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3FTGBVil9QjWlfCk
L8G9VY4b8UEZhkRi4C9R6+3TiLLjsGe11bk4uydEoYOqnGl5QCcG1LfVDiStjrHs
6PNdj18TTi8EBbIicCPmcCILqglEwuyexogo2u3d2R6Qwu0STu0xCbXMwrraWKaZ
68MLLG7+Jp/znPcOMNi392qLEZKTSv8GXQzYa+/rFNhpHpqiGA3FzmvH/1jQgWpO
1PF9kWXoKUkktlaN8hpQtVrThpQFF5IirXj/A6XhYQVEQEFwYM3kLLvXUeW1QJB3
/T+PDdLYiShwrNRtnzo/axrPa0EpMffIEtEaFG/95fnyO+qdOunHck50s2kTYIb6
vcEBbQIDAQABo0IwQDAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBSi3RnXKUbR
62i31WJbbAzGJWw9xDAOBgNVHQ8BAf8EBAMCAoQwDQYJKoZIhvcNAQELBQADggEB
ACU3ZIPShubA4dSo9JyJzLXnvY+N32XDiVwyF4zMNbz7Jr5tgW5CXzcDvTSH7KkW
nzP3+qBULVY224daSfsWdwz/9ZK+5OGMkYCSpiS+1lAH4gDIctwJbn/82idqWZWN
BKWRf27qh/dVFLAlNu69BIw5XUjMjhDN1v6ABYRb2Ht0pAesSw+A3lHJvFmdEhf2
XcopG+t8nnohFDPAeHKzEHnHOF1YIMKkFbc0UBC3jrS/P+sX1V6sm3znQ2ZE0aBi
a/ZlOmOZFZRUUChffFULBp3I82+NsZH6duXP5R2/c2ZxBSrtpeaeSNNerpwyr2iH
2PpfXUn1tsVm6EGPQPgrHcA=
-----END CERTIFICATE-----
""".strip()
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

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Redis
RQ_QUEUES['default']['ASYNC'] = False
RQ_QUEUES['high']['ASYNC'] = False

# Algolia
ALGOLIA['INDEX_SUFFIX'] = 'dev'

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
    'debug_toolbar',
]
