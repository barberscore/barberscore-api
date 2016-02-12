import os
import dj_database_url

from django.core.exceptions import ImproperlyConfigured


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
ADMINS = (
    (get_env_variable("FULL_NAME"), get_env_variable("USER_EMAIL")),
)
SERVER_EMAIL = get_env_variable('SERVER_EMAIL')


# Database
DATABASE_URL = get_env_variable("DATABASE_URL")
DATABASES = {'default': dj_database_url.config(default=DATABASE_URL)}

# Auth
AUTH_USER_MODEL = "api.User"
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

# Middleware
MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'django.middleware.transaction.TransactionMiddleware',
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
)

# Phonenumber support
PHONENUMBER_DEFAULT_REGION = 'US'
PHONENUMBER_DEFAULT_FORMAT = 'NATIONAL'

# Rest Framework (JSONAPI)
REST_FRAMEWORK = {
    # DJA settings
    'PAGE_SIZE': 200,
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework_json_api.pagination.PageNumberPagination',
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
        # 'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        # 'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework_filters.backends.DjangoFilterBackend',
    ],
}

# Plus supplementary settings:
JSON_API_FORMAT_KEYS = 'dasherize'
# JSON_API_FORMAT_RELATION_KEYS = 'dasherize'
# JSON_API_PLURALIZE_RELATION_TYPE = False
APPEND_TRAILING_SLASH = False

#  CORS Headers
CORS_ORIGIN_ALLOW_ALL = False

# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200',
        'INDEX_NAME': 'haystack',
    },
}

# Grappelli
GRAPPELLI_ADMIN_TITLE = 'Barberscore Admin'
GRAPPELLI_AUTOCOMPLETE_LIMIT = 20
# GRAPPELLI_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Applications
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'grappelli.dashboard',
    'super_inlines.grappelli_integration',
    'grappelli',
    'super_inlines',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'fsm_admin',
    'django_fsm',
    # 'django_fsm_log',
    'haystack',
    'easy_pdf',
    'timezone_field',
    'corsheaders',
    'mptt',
    'rest_framework',
    'apps.api',
)
