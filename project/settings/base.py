# Standard Library
import os

# Third-Party
import dj_database_url

# Django
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    """Get the environment variable or return exception."""
    try:
        var = os.environ[var_name]
        # Replace unix strings with Python Booleans
        if var == 'True':
            var = True
        if var == 'False':
            var = False
    except KeyError:
        error_msg = "Set the {var_name} env var".format(var_name=var_name)
        raise ImproperlyConfigured(error_msg)
    return var


# Common
DJANGO_SETTINGS_MODULE = get_env_variable("DJANGO_SETTINGS_MODULE")
DEBUG = False
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
SECRET_KEY = get_env_variable("SECRET_KEY")
DEFAULT_FROM_EMAIL = "admin@barberscore.com"
ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'
USE_I18N = False
USE_L10N = False
APPEND_SLASH = False

# Datetime
TIME_ZONE = 'US/Pacific'
USE_TZ = True
DATE_FORMAT = 'Y-m-d'
TIME_FORMAT = 'H:i:s'
DATETIME_FORMAT = 'Y-m-d H:i:s'

# Authentication
AUTH_USER_MODEL = "rest_framework_jwt.User"
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django.contrib.auth.backends.RemoteUserBackend',
]
USERNAME_FIELD = 'username'
REQUIRED_FIELDS = [
    'name',
    'email',
]
LOGIN_URL = 'admin:login'
LOGIN_REDIRECT_URL = 'admin:index'
LOGOUT_REDIRECT_URL = 'admin:login'
JWT_AUTH = {
    'AUTH0_CLIENT_ID': get_env_variable("BARBERSCORE_CLIENT_ID"),
    'AUTH0_CLIENT_SECRET': get_env_variable("BARBERSCORE_CLIENT_SECRET"),
    'AUTH0_DOMAIN': get_env_variable("AUTH0_DOMAIN"),
    'AUTH0_AUDIENCE': get_env_variable("AUTH0_AUDIENCE"),
}

# File Management
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Templating
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
            ],
        }
    },
]

# Database
DATABASES = {
    'default': dj_database_url.parse(
        get_env_variable("DATABASE_URL"),
        conn_max_age=600,
    ),
}

# CORS Configuration
CORS_ORIGIN_ALLOW_ALL = True

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

# Sessions
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# RQ
RQ_QUEUES = {
    'default': {
        'USE_REDIS_CACHE': 'default',
        'ASYNC': True,
    },
    'high': {
        'USE_REDIS_CACHE': 'default',
        'ASYNC': True,
    },
    'low': {
        'USE_REDIS_CACHE': 'default',
        'ASYNC': True,
    },
}
RQ_SHOW_ADMIN_LINK = True

# Algolia
ALGOLIA = {
    'APPLICATION_ID': get_env_variable("ALGOLIASEARCH_APPLICATION_ID"),
    'API_KEY': get_env_variable("ALGOLIASEARCH_API_KEY"),
    'AUTO_INDEXING': False,
}

# Cloudinary
CLOUDINARY_URL = get_env_variable("CLOUDINARY_URL")
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Rest Framework (JSONAPI)
REST_FRAMEWORK = {
    'PAGE_SIZE': 100,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework_json_api.pagination.JsonApiPageNumberPagination',
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser'
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework_json_api.renderers.JSONRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.AdminRenderer',
    ],
    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ],
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'vnd.api+json',
    # 'DEFAULT_THROTTLE_CLASSES': (
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle'
    # ),
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '100/day',
    #     'user': '1000/day'
    # }
}

# JSONAPI
JSON_API_FORMAT_FIELD_NAMES = 'dasherize'
JSON_API_FORMAT_TYPES = 'dasherize'
JSON_API_PLURALIZE_TYPES = False

# Phone Number
PHONENUMBER_DB_FORMAT = 'E164'
PHONENUMBER_DEFAULT_REGION = 'US'

# Applications
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'algoliasearch_django',
    'cloudinary_storage',
    'cloudinary',
    'rest_framework',
    'django_filters',
    'dry_rest_permissions',
    'django_rq',
    'django_fsm',
    'django_fsm_log',
    'fsm_admin',
    'phonenumber_field',
    'reversion',
    'rest_framework_jwt',
    'prettyjson',
    'corsheaders',
    'apps.bhs',
    'apps.smanager',
    'apps.rmanager',
    'apps.keller',
]
