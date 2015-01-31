from .base import *

import sys

EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'
MANDRILL_API_KEY = get_env_variable("MANDRILL_APIKEY")

BUGSNAG = {
    "api_key": get_env_variable("BUGSNAG_API_KEY"),
    "project_root": PROJECT_ROOT,
}

MIDDLEWARE_CLASSES += (
    "bugsnag.django.middleware.BugsnagMiddleware",
)

ALLOWED_HOSTS = [
    get_env_variable("HEROKU_HOST"),
    '.barberscore.com',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'ERROR',
        'handlers': ['bugsnag'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
    },
    'loggers': {
        'api': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
        'noncense': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
        'utils': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
    'handlers': {
        'bugsnag': {
            'level': 'ERROR',
            'class': 'bugsnag.handlers.BugsnagHandler',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout,
        },
    },
}
