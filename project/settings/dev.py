# Standard Libary
# Debug Toolbar
from .base import *

# Django
DEBUG = True
HOST_NAME = 'http://localhost:8000'
ALLOWED_HOSTS = [
    'localhost',
]
INTERNAL_IPS = [
    '127.0.0.1',
]

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

# RQ Overwrite
RQ_QUEUES['default']['ASYNC'] = True
RQ_QUEUES['high']['ASYNC'] = True

# Algolia Overwrite
ALGOLIA['AUTO_INDEXING'] = False
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
                'logfile',
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
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'dev.log'),
            'maxBytes': 5000000,
            'backupCount': 10,
            'formatter': 'standard',
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
