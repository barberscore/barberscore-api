from .base import *

ALLOWED_HOSTS = [
    'localhost',
]

LOGGING = {
    'version': 1,
    "disable_existing_loggers": True,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'loggers': {
        'apps.api': {
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
}
