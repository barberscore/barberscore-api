# Local
from .base import *

DEBUG = True
ALLOWED_HOSTS = [
    'localhost',
]
INTERNAL_IPS = [
    '127.0.0.1',
]

#  Membercenter API
BHS_URL = get_env_variable("BHS_URL")

# Mailhog
EMAIL_PORT = 1025

# Debug Toolbar
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE
MIDDLEWARE += [
    'querycount.middleware.QueryCountMiddleware',
]
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

# Async settings
RQ_QUEUES['default']['ASYNC'] = True
RQ_QUEUES['high']['ASYNC'] = True
RQ_QUEUES['low']['ASYNC'] = True

# Algolia Overwrite
ALGOLIA['INDEX_SUFFIX'] = 'dev'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'api': {
            'handlers': [
                'console',
            ],
            'level': 'DEBUG',
        },
        'importer': {
            'handlers': [
                'console',
            ],
            'level': 'DEBUG',
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
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
}

INSTALLED_APPS += [
    'debug_toolbar',
    'whitenoise.runserver_nostatic',
]
