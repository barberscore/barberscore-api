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
pem_data = b"""
-----BEGIN CERTIFICATE-----
MIIC+jCCAeKgAwIBAgIJbuZM6FlzJ6TDMA0GCSqGSIb3DQEBBQUAMCQxIjAgBgNV
BAMTGWJhcmJlcnNjb3JlLWRldi5hdXRoMC5jb20wHhcNMTYxMDI2MjAzNDE0WhcN
MzAwNzA1MjAzNDE0WjAkMSIwIAYDVQQDExliYXJiZXJzY29yZS1kZXYuYXV0aDAu
Y29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArktLSct+7BT6SDLJ
k6P7esPEk2rWTd6+S97gB8oZ9I4WTiGx7jsPgoYn9pUltnHF2r0N1WuOM8UCUMfk
b/lwHcpBGsNx2cxsvr0oVsgKEynJNn0ynRCR2EH7b/iYrtOtMyE1CXtMMgT9vMhS
e/mE8VxsTvgev1nQmR8lq/jXZvLY068/BbicWsrJ11/7toSiJEMH3yEwzlK7ZRDj
Oorp0sp3//ZCZeP4ep9SwK/dNthUgAe1yfQokKQCnW5aMYYZgMG4RDIKND28PGMe
7QmesTbSzoXTPDZBMLJC0o/CSZlQrPzg5SmfyGO0sl+ZnWt9PBeCYjLgtBbKDOH9
o8gNTQIDAQABoy8wLTAMBgNVHRMEBTADAQH/MB0GA1UdDgQWBBS9m0sa23+rX1a1
3/2+h9f2UTlrzDANBgkqhkiG9w0BAQUFAAOCAQEALsbWOoKVb4hEFl7akai9bqRK
DMxXf6ZBu7tQMFVDE3xr5Rzc11aeyUCWA9oIrv07JNHQI1OPrXHSKdd+UDAiO2N1
pTIfrOjySNxBoTkr0IJWp+SQjiNr+vvbJGSgThvebHmxNVIQ+WQosVmWHobuZ+tF
LXyoMAxse01/vNGW3LqsMWG32icIQ4Xra2wKmXag/oQGlu4NASRuEhtP8Lp47v1D
m+rablf5MmFd3dtErVU9a3cqeGUEIjYhTK18slv55LOEdMPklRgkDUlvCIxd3RA1
yZw/f9vAojVPQmXNY95Kzg14aqhiRGSeNhG6BRMnDvzm3/rx4UezNmLxT6F1cg==
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

# Cloudinary
CLOUDINARY_URL = get_env_variable("CLOUDINARY_URL")

# Redis
RQ_QUEUES['default']['ASYNC'] = False

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
