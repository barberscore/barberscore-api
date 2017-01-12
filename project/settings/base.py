# Standard Libary
import datetime
import os
import jwt
import base64
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


DEBUG = get_env_variable("DEBUG")

# Globals
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PROJECT_NAME = get_env_variable('PROJECT_NAME')
TIME_ZONE = get_env_variable("TZ")
USE_TZ = True
LANGUAGE_CODE = 'en-us'
USE_I18N = False
USE_L10N = True
SECRET_KEY = get_env_variable("SECRET_KEY")
ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'
DOMAIN = get_env_variable("DOMAIN")
STATICFILES_DIRS = ()
STATIC_URL = '/static/'
SERVER_EMAIL = get_env_variable('SERVER_EMAIL')


# Database
DATABASE_URL = get_env_variable("DATABASE_URL")
DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL)
}

# Auth
AUTH_USER_MODEL = "app.User"
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
USERNAME_FIELD = 'username'
REQUIRED_FIELDS = [
]


# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
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
            'debug': DEBUG,
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

# Phonenumber support
PHONENUMBER_DEFAULT_REGION = 'US'
PHONENUMBER_DEFAULT_FORMAT = 'NATIONAL'

# Rest Framework (JSONAPI)
REST_FRAMEWORK = {
    # DJA settings
    'PAGE_SIZE': 100,
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    # And other DRF settings
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'dry_rest_permissions.generics.DRYPermissions',
    ],
}

# Plus supplementary settings:
JSON_API_FORMAT_KEYS = 'dasherize'
# JSON_API_FORMAT_RELATION_KEYS = 'dasherize'
# JSON_API_PLURALIZE_RELATION_TYPE = False
APPEND_TRAILING_SLASH = False

# JWT Settings
AUTH0_CLIENT_SECRET = get_env_variable("AUTH0_CLIENT_SECRET")
AUTH0_CLIENT_ID = get_env_variable("AUTH0_CLIENT_ID")
AUTH0_DOMAIN = get_env_variable("AUTH0_DOMAIN")


def jwt_get_username_from_payload_handler(payload):
    return payload.get('email')


def jwt_decode(token):
    return jwt.decode(
        token,
        # AUTH0_CLIENT_SECRET,
        base64.b64decode(
            AUTH0_CLIENT_SECRET.replace("_", "/").replace("-", "+")
        ),
        audience=AUTH0_CLIENT_ID,
    )

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_DECODE_HANDLER': jwt_decode,
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': jwt_get_username_from_payload_handler,
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}

#  CORS Headers
CORS_ORIGIN_ALLOW_ALL = False

#  Docraptor
DOCRAPTOR_API_KEY = get_env_variable("DOCRAPTOR_API_KEY")

# Applications
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'corsheaders',
    'fsm_admin',
    'django_fsm',
    # 'django_fsm_log',
    'timezone_field',
    'mptt',
    'rest_framework',
    'dry_rest_permissions',
    'app',
)
