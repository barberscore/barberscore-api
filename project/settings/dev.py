# Local
from .base import *

ALLOWED_HOSTS = [
    'localhost',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

# Static Server Config
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATIC_URL = '/static/'

# Media (aka File Upload) Server Config
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIA_URL = '/media/'

# Aliasing Django Defaults
DEFAULT_FILE_STORAGE = MEDIA_STORAGE
STATICFILES_STORAGE = STATIC_STORAGE

# CORS Settings
CORS_ORIGIN_WHITELIST = (
    'localhost:4200',
)

# Test Settings
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--nologcapture',
    '--with-coverage',
    '--cover-package=app',
]

# Email
DEFAULT_FROM_EMAIL = 'admin@{0}.com'.format(PROJECT_NAME)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Debug Toolbar
DEBUG_TOOLBAR_PATCH_SETTINGS = False
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
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

INSTALLED_APPS += (
    'debug_toolbar',
    'django_nose',
)
