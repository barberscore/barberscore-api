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

# BHS Database
BHS_DATABASE_URL = get_env_variable("BHS_DATABASE_URL")
DATABASES['bhs_db'] = dj_database_url.parse(BHS_DATABASE_URL, conn_max_age=0)
DATABASES['bhs_db']['OPTIONS'] = {
    'ssl': {'ca': '/app/rds-combined-ca-bundle.pem'}}
DATABASE_ROUTERS = [
    'routers.BHSRouter',
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
MIIC8jCCAdqgAwIBAgIJABLVuzjwy/ZnMA0GCSqGSIb3DQEBBQUAMCAxHjAcBgNV
BAMTFWJhcmJlcnNjb3JlLmF1dGgwLmNvbTAeFw0xNjAyMDIyMDQzMjlaFw0yOTEw
MTEyMDQzMjlaMCAxHjAcBgNVBAMTFWJhcmJlcnNjb3JlLmF1dGgwLmNvbTCCASIw
DQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBANBRssHuPBDasaOVaHIZ+Ab3lsMv
mzlJENgMl2QbXBIueR1//7nDDg86y/BpxkLvweUaHBaIXIgep4vNaR1oKNtM3u/i
umxE3TGHib2amWJ6KhfKj9mx5Tr5i0N1eOTdRAZse5cE5sXLndfsVa8bnPquzCs9
FI1JuD1YS3xcya1TGahgGcdlvCrJ8fpoqZOYDfQNpU76ZzbgtextlQx0Lj+7ENNh
oj2IMWBQHn4ziBBn0L8RXNo2aSbd/XL7K6+yWWrXlpznmeD6FTQk3ci07hVax8JG
cZ+y75nKR7yCKMDsewF/gHPlmuJNDbl7EnyoYjPDwF+bLiZihXr+K13pk1UCAwEA
AaMvMC0wDAYDVR0TBAUwAwEB/zAdBgNVHQ4EFgQU+TcpRN0CGkreBQ1QC8dSKwqI
BJMwDQYJKoZIhvcNAQEFBQADggEBAFCeNW2uY1MxAJhT+Dln9V7fOqM6YCu0dpST
YvaDzKFqLnrFUmVieY482E561l6L18InVP3OURv13LPPqAAA/d7tY5aWZg9oQrfg
Kl4DMK9F0WE6zKWLVYP/VvkofT8TIak9QdhDVmvLceoqEUkVjtr8L9mPGT+bW3Uw
5SAOtfiniuBdxatYUTAmxcPXNa7+6FBcQzFbBgSCYLdie7VrGZZsACd8h42EXM0v
JqkZzu/oXza4VrgXKLQ91ly64RLvpaS++OQjxdhb7iBP2TSmOiwqO700PNhEUuZC
yYe1Toa8+xB3MDBPvRLfY0tuRbghAjHSY8aM1rPcFs54WOpjnZk=
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
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_HOST_USER = get_env_variable("SENDGRID_USERNAME")
# EMAIL_HOST_PASSWORD = get_env_variable("SENDGRID_PASSWORD")
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = get_env_variable("SENDGRID_API_KEY")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# EMAIL_SUBJECT_PREFIX = "[Barberscore] "
# EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
# SENDGRID_API_KEY = get_env_variable("SENDGRID_API_KEY")

# Bugsnag
BUGSNAG = {
    'api_key': get_env_variable("BUGSNAG_API_KEY"),
    'notify_release_stages': [
        'production', 'staging',
    ],
    'release_stage': 'production',
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
