from .basic import *
import sys
HOST_NAME = 'https://api.staging.barberscore.com'
ALLOWED_HOSTS = [
    '.barberscore.com',
    '.herokuapp.com',
]

# JWT Settings
def jwt_get_username_from_payload_handler(payload):
    """Switch to email as JWT username payload."""
    return payload.get('email')

from cryptography import x509
from cryptography.hazmat.backends import default_backend

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

JWT_AUTH = {
    'JWT_AUDIENCE': AUTH0_CLIENT_ID,
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': jwt_get_username_from_payload_handler,
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_PUBLIC_KEY': jwt_public_key,
    'JWT_ALGORITHM': 'RS256',
}


# Heroku
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
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
            'stream': sys.stdout,
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
    },
}
