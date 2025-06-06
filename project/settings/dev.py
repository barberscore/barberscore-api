# Local
from .base import *

DEBUG = True
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0'
]
INTERNAL_IPS = [
    '127.0.0.1',
]

# Mailhog
EMAIL_PORT = 1026
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
# EMAIL_HOST_USER = 'd7409e08d76811'
# EMAIL_HOST_PASSWORD = 'ef085d636ac702'
# EMAIL_PORT = '2525'


# Debug Toolbar
'''MIDDLEWARE = [
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
]'''

# Async settings
# if DEBUG:
#     RQ_QUEUES['default']['ASYNC'] = False
#     RQ_QUEUES['high']['ASYNC'] = False
#     RQ_QUEUES['low']['ASYNC'] = False
# else:
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
    # 'debug_toolbar',
    'whitenoise.runserver_nostatic',
]

# Caches
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": get_env_variable("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 20,
            },
        }
    },
}
