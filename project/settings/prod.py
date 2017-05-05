# Local
from .base import *


# JWT Settings
def jwt_get_username_from_payload_handler(payload):
    return payload.get('email')

JWT_AUTH = {
    # 'JWT_SECRET_KEY': AUTH0_CLIENT_SECRET,
    'JWT_AUDIENCE': AUTH0_CLIENT_ID,
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': jwt_get_username_from_payload_handler,
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_PUBLIC_KEY': jwt_public_key,
    'JWT_ALGORITHM': 'RS256',
}


# Heroku Settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

# CORS Settings
CORS_ORIGIN_WHITELIST = [
    '{0}.com'.format(PROJECT_NAME),
    '{0}.auth0.com'.format(PROJECT_NAME),
]

#  Bugsnag
BUGSNAG = {
    "api_key": get_env_variable("BUGSNAG_API_KEY"),
    "project_root": PROJECT_ROOT,
}
MIDDLEWARE = [
    'bugsnag.django.middleware.BugsnagMiddleware',
] + MIDDLEWARE

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = get_env_variable("SENDGRID_USERNAME")
EMAIL_HOST_PASSWORD = get_env_variable("SENDGRID_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'root': {
        'level': get_env_variable('DJANGO_LOG_LEVEL'),
        'handlers': ['bugsnag'],
    },

    'handlers': {
        'bugsnag': {
            'level': get_env_variable('DJANGO_LOG_LEVEL'),
            'class': 'bugsnag.handlers.BugsnagHandler',
        },
    }
}

INSTALLED_APPS += [
    'django_s3_storage',
]
