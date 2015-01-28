import os
import dj_database_url

from django.core.exceptions import ImproperlyConfigured
from django.contrib.messages import constants as message_constants


def get_env_variable(var_name):
    """Get the environment variable or return exception"""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {var_name} env var".format(var_name=var_name)
        raise ImproperlyConfigured(error_msg)

if get_env_variable("DJANGO_DEBUG") == 'True':
    DEBUG = True
else:
    DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Globals
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PROJECT_NAME = 'barberscore'
USE_TZ = True
TIME_ZONE = get_env_variable("TZ")
LANGUAGE_CODE = 'en-us'
USE_I18N = False
USE_L10N = True
USE_TZ = True
SECRET_KEY = get_env_variable("SECRET_KEY")
ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'
PHONENUMBER_DEFAULT_REGION = 'US'
PHONENUMBER_DEFAULT_FORMAT = 'NATIONAL'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'
DOMAIN = get_env_variable("DOMAIN")
STATICFILES_DIRS = ()

# Database
DATABASE_URL = get_env_variable("DATABASE_URL")
DATABASES = {'default': dj_database_url.config(default=DATABASE_URL)}

# Auth
AUTH_USER_MODEL = 'noncense.User'
AUTHENTICATION_BACKENDS = (
    'noncense.backends.MobileBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Middleware
MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

# Templating
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    # "website.context.mixpanel_public_key",
)

# TODO RUNSERVER WITH CSS!!!

# AWS S3  Settings
# This was hellaciously confusing to set up.  I'm subclassing storages in
# 'apps/dinadesa/backends.py' and doing a lot of renaming below for clarity.
# `Static` means public-read, static resources like CSS, Images, etc.
# `Media` means private, user or admin-uploaded resources that have ACL
# by default (most notably, photos).

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Configure AWS variables
# Access credentials (global)
AWS_ACCESS_KEY_ID = get_env_variable("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env_variable("AWS_SECRET_ACCESS_KEY")
AWS_PRELOAD_METADATA = True

# Static Server Config
AWS_STATIC_BUCKET_NAME = get_env_variable("AWS_STATIC_BUCKET_NAME")
STATIC_ROOT = '/static/'
if DEBUG:
    STATIC_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    STATIC_URL = '/static/'
else:
    STATIC_STORAGE = 'utils.backends.StaticS3BotoStorage'
    STATIC_URL = 'https://{0}.s3-us-west-1.amazonaws.com/'.format(
        AWS_STATIC_BUCKET_NAME,
    )

# Media (aka File Upload) Server Config
AWS_MEDIA_BUCKET_NAME = get_env_variable("AWS_MEDIA_BUCKET_NAME")
MEDIA_ROOT = '/Users/dbinetti/Repos/barberscore/project/media'
if DEBUG:
    MEDIA_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_URL = '/media/'
else:
    MEDIA_STORAGE = 'utils.backends.MediaS3BotoStorage'
    MEDIA_URL = 'https://{0}.s3-us-west-1.amazonaws.com/'.format(
        AWS_MEDIA_BUCKET_NAME,
    )

# Aliasing Django Defaults
DEFAULT_FILE_STORAGE = MEDIA_STORAGE
STATICFILES_STORAGE = STATIC_STORAGE

# Bootstrap overwrite
MESSAGE_TAGS = {
    message_constants.ERROR: 'danger',
}

# Twilio for Noncense
TWILIO_ACCOUNT_SID = get_env_variable("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = get_env_variable("TWILIO_AUTH_TOKEN")

# Rest Framework
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ]
}

# Ajax Selects
AJAX_LOOKUP_CHANNELS = {
    'singer': {'model': 'api.singer', 'search_field': 'name'},
    'chorus': {'model': 'api.chorus', 'search_field': 'name'},
    'quartet': {'model': 'api.quartet', 'search_field': 'name'},
}


# Applications
INSTALLED_APPS = (
    'utils',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'timezone_field',
    'ajax_select',
    'corsheaders',
    'noncense',
    'rest_framework',
    'apps.api',
    'apps.website',
)

CORS_ORIGIN_ALLOW_ALL = True
