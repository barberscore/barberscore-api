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
MIIDFTCCAf2gAwIBAgIJfzzFZRilvkumMA0GCSqGSIb3DQEBCwUAMCgxJjAkBgNV
BAMTHWJhcmJlcnNjb3JlLXN0YWdpbmcuYXV0aDAuY29tMB4XDTE4MDIwOTE4Mjkx
NloXDTMxMTAxOTE4MjkxNlowKDEmMCQGA1UEAxMdYmFyYmVyc2NvcmUtc3RhZ2lu
Zy5hdXRoMC5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDtF92O
vLtUd5G2ktJqJgnm1JCTouhJk8ejg0eEFDEpUoSfumhQt0mVArWlMqwyYcxRrYdT
4A8XT/bGOamQWBVpqsnvEfwprnrIIIkARChGByz5/grITnMon7E/WGEV98vYjxsu
vYl9gyX40ILRUR7yMbhdBa4VRAiR4vzBKvla4lwItq4H/WLVtN/qJSlckwlaoxFJ
IAMdNm0DCBAhODtWVXFWPO3srJIpXY7qxKI+0ooS3zBVXcyvf/h5Y7dzci62Yz7G
SO3AEcCuI89YWJ3yqRZbiYdErF3sxqjkXb87NvuYk6l2P9oU0ereVrNlL+8M4yCs
BbBswmpiuYGFeb7rAgMBAAGjQjBAMA8GA1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYE
FPorKieaJWitgA7lItY6l2GbF6CiMA4GA1UdDwEB/wQEAwIChDANBgkqhkiG9w0B
AQsFAAOCAQEAYKoV40DDrlJGNzYFGUTQ8Nn01xiPuNCaw+bFETX6zrOyYRwP/NdY
Mpq3Xfp5b5985weHpzRQxlNGZJTKbYAjlMVarrWnZwXH9HojzAZH0D4S0OSZdTlJ
W4a+/tjijD/ZlbWQPrKH0X+PhCHNUClJRQknmqesmHVvjAND8O16hcZv3fj/dfhN
ZSeTSMJG/9S4eL4ASotDHXW5dva7z9HW1N4BihXX22biUdRnYaLS/wzhctd476jc
I5FM/wVN8vCL5qUc4oMqx77106u+8kUuIH7aRmaIZejBjAksX033B5dwM6P2HDJx
qgZCixEcgsbeBKEx/WFcpgJwJV2egCTaDw==
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
