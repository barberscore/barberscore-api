import sys

# Local
from .base import *

# Third-Party
from cryptography import x509
from cryptography.hazmat.backends import default_backend

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

AUTH0_PUBLIC_KEY = get_env_variable("AUTH0_PUBLIC_KEY")

# JWT Settings
pem_data = AUTH0_PUBLIC_KEY.encode()
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
EMAIL_HOST_USER = get_env_variable("SENDGRID_USERNAME")
EMAIL_HOST_PASSWORD = get_env_variable("SENDGRID_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = "[Barberscore] "

#  Docraptor
DOCRAPTOR_API_KEY = get_env_variable("DOCRAPTOR_API_KEY")

# Cloudinary
CLOUDINARY_URL = get_env_variable("CLOUDINARY_URL")

# Bugsnag
BUGSNAG_API_KEY = get_env_variable("BUGSNAG_API_KEY")
BUGSNAG_RELEASE_STAGE = get_env_variable("BUGSNAG_RELEASE_STAGE")
MIDDLEWARE = ['bugsnag.django.middleware.BugsnagMiddleware'] + MIDDLEWARE


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'api': {
            'handlers': [
                'console',
            ],
            'level': 'ERROR',
        },
        'importer': {
            'handlers': [
                'console',
            ],
            'level': 'ERROR',
        },
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
    },
}
