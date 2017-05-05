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

DEBUG = True

INTERNAL_IPS = [
    '127.0.0.1',
]

# CORS Settings
CORS_ORIGIN_WHITELIST = [
    'localhost:4200'
]

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Debug Toolbar
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

# Logging
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
        'app': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}

INSTALLED_APPS += [
    'debug_toolbar',
]
