# Standard Libary
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


# Core
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
DATE_FORMAT = 'c'
TIME_FORMAT = 'c'
DATETIME_FORMAT = 'c'

# Database
DATABASE_URL = get_env_variable("DATABASE_URL")
BHS_DATABASE_URL = get_env_variable("BHS_DATABASE_URL")
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600),
    'bhs_db': dj_database_url.parse(BHS_DATABASE_URL, conn_max_age=0)
}
DATABASE_ROUTERS = [
    'routers.BHSRouter',
]

# Authentication
AUTH_USER_MODEL = "api.User"
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
USERNAME_FIELD = 'email'
REQUIRED_FIELDS = []
LOGIN_URL = 'admin:login'
LOGIN_REDIRECT_URL = 'admin:index'
LOGOUT_REDIRECT_URL = 'admin:login'

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
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

# CORS
CORS_ORIGIN_ALLOW_ALL = True

# Rest Framework (JSONAPI)
REST_FRAMEWORK = {
    'PAGE_SIZE': 20,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework_json_api.pagination.PageNumberPagination',
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser'
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework_json_api.renderers.JSONRenderer',
        'rest_framework.renderers.JSONRenderer',
        'api.renderers.NoHTMLFormBrowsableAPIRenderer',
        'rest_framework.renderers.AdminRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

# JSONAPI
JSON_API_FORMAT_KEYS = 'dasherize'
JSON_API_FORMAT_TYPES = 'dasherize'
JSON_API_PLURALIZE_TYPES = False
APPEND_TRAILING_SLASH = False

# WhiteNoise
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATIC_URL = '/static/'

# Cloudinary
MEDIA_URL = '/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Applications
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'corsheaders',
    'cloudinary_storage',
    'cloudinary',
    'django_fsm',
    'django_fsm_log',
    'timezone_field',
    'rest_framework',
    'django_filters',
    'dry_rest_permissions',
    'api',
    'bhs',
]
