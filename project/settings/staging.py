
# Local
from .base import *

# Core
HOST_NAME = 'https://api.staging.barberscore.com'
ALLOWED_HOSTS = [
    '.barberscore.com',
    '.herokuapp.com',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
SECURE_SSL_REDIRECT = True

# Database
DATABASES['bhs_db'] = dj_database_url.parse(
    get_env_variable("BHS_DATABASE_URL"),
    conn_max_age=600,
)
DATABASE_ROUTERS = [
    'routers.BHSRouter',
]

# Email
EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'api': {
            'handlers': [
                'console',
            ],
            'level': 'INFO',
        },
        'importer': {
            'handlers': [
                'console',
            ],
            'level': 'INFO',
        },
        'updater': {
            'handlers': [
                'console',
            ],
            'level': 'INFO',
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': [
                'console'
            ],
            'propagate': False,
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
}
