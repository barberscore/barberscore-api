# Standard Library
import os

# Third-Party
import dj_database_url

# Django
from django.core.exceptions import ImproperlyConfigured
from django.contrib import admin


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

SERVER_EMAIL = 'admin@barberscore.com'
ADMINS = [('Alex Rubin', 'alex@barberscore.com')]
TASK_USER_ID = "auth0|6149b95c273488006af78263"

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
USERNAME_FIELD = 'email'
REQUIRED_FIELDS = [
    'name',
    'id',
]
LOGIN_URL = 'admin:login'
LOGIN_REDIRECT_URL = 'admin:index'
LOGOUT_REDIRECT_URL = 'admin:login'
JWT_AUTH = {
    'AUTH0_DOMAIN': get_env_variable("AUTH0_DOMAIN"),
    'AUTH0_CLIENT_ID': get_env_variable("AUTH0_CLIENT_ID"),
    'AUTH0_CLIENT_SECRET': get_env_variable("AUTH0_CLIENT_SECRET"),
    'AUTH0_AUDIENCE': get_env_variable("AUTH0_AUDIENCE"),
    'JWT_AUDIENCE': get_env_variable("AUTH0_CLIENT_ID"),
}

# BHS MemberCenter
MEMBERCENTER_URL = get_env_variable("MEMBERCENTER_URL")

CONVENTION_OWNERS = [
    'steve@armstrongconsulting.ca',
    'proclamation56@gmail.com',
    'mottley81@gmail.com',
    'randy.rensi@ieee.org',
    'alex@barbershopchorus.com',
]

# SALESFORCE_ORGANIZATIONS
SALESFORCE_ORGANIZATION_ID = get_env_variable("SALESFORCE_ORGANIZATION_ID")

DISTRICT_DEFAULT_LOGOS = {
    110: 'media/global/logos/barbershop-harmony-society.jpg', # BHS
    200: 'media/global/logos/cardinal-district.jpg', # CAR
    205: 'media/global/logos/central-states-district.jpg', # CSD
    210: 'media/global/logos/dixie-district.jpg', # DIX
    215: 'media/global/logos/evergreen-district.jpg', # EVG
    220: 'media/global/logos/far-western-district.jpg', # FWD
    225: 'media/global/logos/illinois-district.jpg', # ILL
    230: 'media/global/logos/johnny-appleseed-district.jpg', # JAD
    235: 'media/global/logos/land-o-lakes-district.jpg', # LOL
    240: 'media/global/logos/mid-atlantic-district.jpg', # MAD
    345: 'media/global/logos/northeastern-district.jpg', # NED
    350: 'media/global/logos/carolinas-district.jpg', # NSC
    355: 'media/global/logos/ontario-district.jpg', # ONT
    360: 'media/global/logos/pioneer-district.jpg', # PIO
    365: 'media/global/logos/rocky-mountain-district.jpg', # RMD
    370: 'media/global/logos/seneca-land-district.jpg', # SLD
    375: 'media/global/logos/sunshine-district.jpg', # SUN
    380: 'media/global/logos/southwestern-district.jpg', # SWD

    430: 'media/global/logos/barbershop-harmony-society.jpg', # HI
    700: 'media/global/logos/barbershop-harmony-society.jpg', # HI - Area 1
    705: 'media/global/logos/barbershop-harmony-society.jpg', # HI - Area 2
    710: 'media/global/logos/barbershop-harmony-society.jpg', # HI - Area 3
    715: 'media/global/logos/barbershop-harmony-society.jpg', # HI - Area 4
    720: 'media/global/logos/barbershop-harmony-society.jpg', # HI - Area 5
    725: 'media/global/logos/barbershop-harmony-society.jpg', # HI - Area 6

    510: 'media/global/logos/barbershop-harmony-society.jpg', # BABS
    515: 'media/global/logos/barbershop-harmony-society.jpg', # BHA
    750: 'media/global/logos/barbershop-harmony-society.jpg', # BHA - VR
    755: 'media/global/logos/barbershop-harmony-society.jpg', # BHA - WR
    760: 'media/global/logos/barbershop-harmony-society.jpg', # BHA - CR
    765: 'media/global/logos/barbershop-harmony-society.jpg', # BHA - ER
    770: 'media/global/logos/barbershop-harmony-society.jpg', # BHA - SR
    775: 'media/global/logos/barbershop-harmony-society.jpg', # BHA - TR

    520: 'media/global/logos/barbershop-harmony-society.jpg', # BHNZ
    800: 'media/global/logos/barbershop-harmony-society.jpg', # BHNZ - NR
    805: 'media/global/logos/barbershop-harmony-society.jpg', # BHNZ - CR
    810: 'media/global/logos/barbershop-harmony-society.jpg', # BHNZ - SR

    525: 'media/global/logos/barbershop-harmony-society.jpg', # BinG
    540: 'media/global/logos/barbershop-harmony-society.jpg', # HH
    550: 'media/global/logos/barbershop-harmony-society.jpg', # IABS
    560: 'media/global/logos/barbershop-harmony-society.jpg', # LABBS
    565: 'media/global/logos/barbershop-harmony-society.jpg', # BIBA
}

SESSION_OWNERS = CONVENTION_OWNERS

if os.environ['EMAIL_ADMINS_ONLY']:
    EMAIL_ADMINS_ONLY = get_env_variable("EMAIL_ADMINS_ONLY")
else:
    EMAIL_ADMINS_ONLY = True
EMAIL_ADMINS = [
    'Steve Armstrong <steve@armstrongconsulting.ca>',
    'David Mills <proclamation56@gmail.com>',
    'Mike Ott <mottley81@gmail.com>',
    'Randy Rensi <randy.rensi@ieee.org>',
    'Alex Rubin <alex@webgraph.com>'
]

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

if get_env_variable('USE_HTTPS'):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True

# Templating
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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
                "ssl_cert_reqs": None,
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
    'PAGE_SIZE':
        100,
    'EXCEPTION_HANDLER':
        'rest_framework_json_api.exceptions.exception_handler',
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework_json_api.pagination.JsonApiPageNumberPagination',
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser'
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework_json_api.renderers.JSONRenderer',
        'apps.registration.renderers.BrowsableAPIRendererWithoutForms',
        # 'rest_framework.renderers.BrowsableAPIRenderer',
        # 'rest_framework.renderers.JSONRenderer',
        # 'rest_framework.renderers.AdminRenderer',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'dry_rest_permissions.generics.DRYPermissions',
    ],
    'DEFAULT_METADATA_CLASS':
        'rest_framework_json_api.metadata.JSONAPIMetadata',
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework_json_api.filters.QueryParameterValidationFilter',
        'rest_framework_json_api.filters.OrderingFilter',
        'rest_framework_json_api.django_filters.DjangoFilterBackend',
        'django_filters.rest_framework.DjangoFilterBackend',
        # 'rest_framework.filters.SearchFilter',
    ],
    # 'SEARCH_PARAM': 'filter[search]',
    'ORDERING_PARAM': 'sort',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework_json_api.renderers.JSONRenderer',
    ],
    'TEST_REQUEST_DEFAULT_FORMAT':
        'vnd.api+json',
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
# JSON_API_FORMAT_FIELD_NAMES = 'dasherize'
# JSON_API_FORMAT_TYPES = 'dasherize'
JSON_API_PLURALIZE_TYPES = False
JSON_API_UNIFORM_EXECEPTIONS = True

# Phone Number
PHONENUMBER_DB_FORMAT = 'E164'
PHONENUMBER_DEFAULT_REGION = 'US'

ADMIN_ORDERING = {
    "organizations": [
        'Organization',
        'District',
        'Division'
    ],
}

# Creating a sort function
def get_app_list(self, request):
    app_dict = self._build_app_dict(request)
    for app_name in app_dict:
        if app_name in ADMIN_ORDERING:
            app = app_dict[app_name]
            app['models'].sort(key=lambda x: ADMIN_ORDERING[app_name].index(x['object_name']))
            yield app
        else:
            yield app_dict[app_name]

admin.AdminSite.get_app_list = get_app_list

# Sync Production Database admin feature
# Only visible in non-production environments when BARBERSCORE_PROD_DATABASE is set
_original_each_context = admin.AdminSite.each_context

def _patched_each_context(self, request):
    ctx = _original_each_context(self, request)
    _is_prod = DJANGO_SETTINGS_MODULE == 'settings.prod'
    _has_source = bool(os.environ.get('BARBERSCORE_PROD_DATABASE'))
    ctx['show_sync_db_button'] = (not _is_prod) and _has_source
    return ctx

admin.AdminSite.each_context = _patched_each_context

from django.urls import path as _admin_path

_original_get_urls = admin.AdminSite.get_urls

def _patched_get_urls(self):
    self.index_template = 'admin/custom_index.html'
    from views import sync_prod_db_confirm
    from views import sync_prod_db_execute
    custom_urls = [
        _admin_path('sync-db/', self.admin_view(sync_prod_db_confirm), name='sync_prod_db'),
        _admin_path('sync-db/execute/', self.admin_view(sync_prod_db_execute), name='sync_prod_db_execute'),
    ]
    return custom_urls + _original_get_urls(self)

admin.AdminSite.get_urls = _patched_get_urls

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
    'django_object_actions',
    'fsm_admin',
    'phonenumber_field',
    'reversion',
    'rest_framework_jwt',
    'prettyjson',
    'corsheaders',
    'apps.bhs',
    'apps.registration',
    'apps.adjudication',
    'apps.salesforce',
    'apps.organizations',
]
