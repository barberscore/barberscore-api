# Standard Libary
import os

# Third-Party
from cryptography import x509
from cryptography.hazmat.backends import default_backend
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
DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL)
}

# Authentication
AUTH_USER_MODEL = "app.User"
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
USERNAME_FIELD = 'email'
REQUIRED_FIELDS = []
LOGIN_URL = 'admin:login'
LOGIN_REDIRECT_URL = 'admin:app_list'
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
    'PAGE_SIZE': 10,
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
        'app.renderers.NoHTMLFormBrowsableAPIRenderer',
        'rest_framework.renderers.AdminRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ],
}

# WhiteNoise
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATIC_URL = '/static/'

# JSONAPI
JSON_API_FORMAT_KEYS = 'dasherize'
APPEND_TRAILING_SLASH = False

#  Docraptor
DOCRAPTOR_API_KEY = get_env_variable("DOCRAPTOR_API_KEY")

# Cloudinary
CLOUDINARY_URL = get_env_variable("CLOUDINARY_URL")

# Auth0
AUTH0_CLIENT_ID = get_env_variable("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = get_env_variable("AUTH0_CLIENT_SECRET")
AUTH0_DOMAIN = get_env_variable("AUTH0_DOMAIN")

AUTH0_API_ID = get_env_variable("AUTH0_API_ID")
AUTH0_API_SECRET = get_env_variable("AUTH0_API_SECRET")
AUTH0_AUDIENCE = get_env_variable("AUTH0_AUDIENCE")

AUTH0_PUBLIC_KEY = get_env_variable("AUTH0_PUBLIC_KEY")

# JWT Settings
pem_data = open(AUTH0_PUBLIC_KEY, 'rb').read()
cert = x509.load_pem_x509_certificate(pem_data, default_backend())
jwt_public_key = cert.public_key()


def jwt_get_username_from_payload_handler(payload):
    return payload.get('email')


JWT_AUTH = {
    'JWT_AUDIENCE': AUTH0_CLIENT_ID,
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': jwt_get_username_from_payload_handler,
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_PUBLIC_KEY': jwt_public_key,
    'JWT_ALGORITHM': 'RS256',
}

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
    'django_fsm',
    'timezone_field',
    'rest_framework',
    'django_filters',
    'dry_rest_permissions',
    'app',
]
