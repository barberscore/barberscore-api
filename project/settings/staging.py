# Standard Libary
import sys

# Third-Party
from cryptography import x509
from cryptography.hazmat.backends import default_backend

# Local
from .base import *

# Heroku
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
ALLOWED_HOSTS = [
    '.barberscore.com',
    '.herokuapp.com',
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
MIIDFTCCAf2gAwIBAgIJP0AZhh3zdMQyMA0GCSqGSIb3DQEBCwUAMCgxJjAkBgNV
BAMTHWJhcmJlcnNjb3JlLXN0YWdpbmcuYXV0aDAuY29tMB4XDTE3MDUwOTIyMTIz
OFoXDTMxMDExNjIyMTIzOFowKDEmMCQGA1UEAxMdYmFyYmVyc2NvcmUtc3RhZ2lu
Zy5hdXRoMC5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC/8aYp
FPDifYndcdQ0Cpq7CXQMNCF9KsPfLlw3tDlb8614ssq5qPSIx+w/0UMe8ACjjclQ
5Fc4zwJzPMjOHBxDDWdVS6fgfBYG1v3ixQLQhIfnSBpf3q+hntYvpDJ3gp2BwPO+
2EKmDcCNOqAadoGDb4soJqLj3Qv0JFam7B9BruBcAqFDlW8n7ahEA0awBUmeVJdJ
sWo4eJ2bCqxcwbcxVHjXbtxvuyy81RUZmFjuzrgf2fBMdvEbpgpzBmg4lAXw6Q+Q
OKfz34RuHFb7Ky7rJ27heJKNpwKhsQS0WWiKog5TILav44PtiS0BXIxO3jVDuAgv
HBErCq0P6/bI2ZetAgMBAAGjQjBAMA8GA1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYE
FDUR2C1OdJ/0S/An4U1/XWw90k7LMA4GA1UdDwEB/wQEAwIChDANBgkqhkiG9w0B
AQsFAAOCAQEAsBmk5CQ0XJ7Vu1+ssUSLm4bfEvlAeF9Almfyjmw/3QoVQ8KkEtW/
ogIoV3nep+l4Btp3g5WfwzXam84En6K9IdgqUuuBv8bvJclN3om9JePkY9/RRbqQ
/N1L1OoLEJDfUSfV+x0vj2+nqETENbh2UxUbNJQjVBFZW1xYFe6O/db4FgrtVAwz
buyER6G1UeOf/ZU/KyXqTZGTm06AbzPkmDz9XGjpLP1zHIyxQK5/PKykJHGCIIjW
itR73fixB4kEPBRziDeVC/bwvi//JxT1AZJ+MVyrfrFqpE+5Oe0gOQtf025e0uJm
A8U0cA+HFirdAYvKXb1JCFCfubvjHa/ixA==
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

# Bugsnag
BUGSNAG = {
    'api_key': get_env_variable("BUGSNAG_API_KEY"),
    'notify_release_stages': [
        'production', 'staging',
    ],
    'release_stage': 'staging',
}
MIDDLEWARE = ['bugsnag.django.middleware.BugsnagMiddleware'] + MIDDLEWARE

# Cloudinary
CLOUDINARY_URL = get_env_variable("CLOUDINARY_URL")

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'api': {
            'handlers': [
                'console',
                'bugsnag',
            ],
            'level': 'INFO',
        },
        'importer': {
            'handlers': [
                'console',
                'bugsnag',
            ],
            'level': 'INFO',
        },
        'updater': {
            'handlers': [
                'console',
                'bugsnag',
            ],
            'level': 'INFO',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
        'bugsnag': {
            'level': 'ERROR',
            'class': 'bugsnag.handlers.BugsnagHandler',
        },
    },
}
