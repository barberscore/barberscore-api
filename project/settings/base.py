import os

import dj_database_url

from django.core.exceptions import ImproperlyConfigured
from django.contrib.messages import constants as message_constants


def get_env_variable(var_name):
    """Get the environment variable or return exception"""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {var_name} environment variable".\
            format(var_name=var_name)
        raise ImproperlyConfigured(error_msg)

DATABASE_URL = get_env_variable("DATABASE_URL")

DATABASES = {'default': dj_database_url.config(default=DATABASE_URL)}

PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))
PROJECT_HOME = PROJECT_ROOT

PROJECT_NAME = 'barberscore'

TIME_ZONE = 'America/Los_Angeles'

LANGUAGE_CODE = 'en-us'

USE_I18N = False

USE_L10N = True

USE_TZ = True

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, "project/static"),
)

SECRET_KEY = get_env_variable("SECRET_KEY")

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "project/templates"),
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

AUTHENTICATION_BACKENDS = (
    'noncense.backends.MobileBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_USER_MODEL = 'noncense.User'

LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

MESSAGE_TAGS = {
    message_constants.ERROR: 'danger',
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Media Server configuration
MEDIA_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIA_ROOT = 'project/media'
MEDIA_URL = '/media/'

# Static Server configuration
STATIC_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATIC_ROOT = 'static'
STATIC_URL = '/static/'

# Aliasing default settings.
DEFAULT_FILE_STORAGE = MEDIA_STORAGE
STATICFILES_STORAGE = STATIC_STORAGE


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'haystack',
    'convention',
    'noncense',
    'profile',
)


REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS': 'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'utilities.timezone.TimezoneMiddleware',
)

CORS_ORIGIN_ALLOW_ALL = True


HAYSTACK_URL = get_env_variable("BONSAI_URL")

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': HAYSTACK_URL,
        'INDEX_NAME': 'haystack',
    },
}

TWILIO_ACCOUNT_SID = get_env_variable("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = get_env_variable("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = get_env_variable("TWILIO_FROM_NUMBER")
