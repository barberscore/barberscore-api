# Local
from .base import *


# Heroku Settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
ALLOWED_HOSTS = [
    '.barberscore.com',
    '.herokuapp.com',
]
DATABASES['default']['TEST'] = {
    'NAME': DATABASES['default']['name'],
}


# Email
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = get_env_variable("SENDGRID_USERNAME")
EMAIL_HOST_PASSWORD = get_env_variable("SENDGRID_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = "[Barberscore] "

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
}
