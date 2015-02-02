import os
import dj_database_url

from django.core.exceptions import ImproperlyConfigured
from django.contrib.messages import constants as message_constants


def get_env_variable(var_name):
    """Get the environment variable or return exception"""
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
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'
DOMAIN = get_env_variable("DOMAIN")
STATICFILES_DIRS = ()
ADMINS = (
    (get_env_variable("FULL_NAME"), get_env_variable("USER_EMAIL"))
)
SERVER_EMAIL = get_env_variable('SERVER_EMAIL')


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
    'django.middleware.transaction.TransactionMiddleware',
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

# Bootstrap overwrite
MESSAGE_TAGS = {
    message_constants.ERROR: 'danger',
}

# Twilio for Noncense
TWILIO_ACCOUNT_SID = get_env_variable("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = get_env_variable("TWILIO_AUTH_TOKEN")

# Phonenumber support
PHONENUMBER_DEFAULT_REGION = 'US'
PHONENUMBER_DEFAULT_FORMAT = 'NATIONAL'

# Rest Framework
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ]
}

#  CORS Headers
CORS_ORIGIN_ALLOW_ALL = True

# Easy Select2
SELECT2_USE_BUNDLED_JQUERY = False

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
    'django_object_actions',
    'easy_select2',
    'corsheaders',
    'watson',
    'noncense',
    'rest_framework',
    'apps.api',
    'apps.website',
)
