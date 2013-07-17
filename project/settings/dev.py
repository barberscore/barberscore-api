from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG


INSTALLED_APPS += (
    'debug_toolbar',
    'django_extensions',
    'django_nose',
)

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}


# CACHES = {
#     'default': {
#         'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
#         'LOCATION': 'localhost:11211',
#         'TIMEOUT': 500,
#         'BINARY': True,
#         'OPTIONS': {  # Maps to pylibmc "behaviors"
#             'tcp_nodelay': True,
#             'ketama': True
#         }
#     }
# }

NONCENSE_SERVER = {
    'default': {
        # 'BACKEND': '',
        'URL': 'http://localhost:7000/',
        'CONSUMER_ID': get_env_variable("NONCENSE_CONSUMER_ID"),
        'CONSUMER_SECRET': get_env_variable("NONCENSE_CONSUMER_SECRET"),
    }
}


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://localhost:9200/',
        'INDEX_NAME': 'haystack',
    },
}

MEDIA_ROOT = PROJECT_ROOT.ancestor(2).child("localstorage").child("media")
MEDIA_URL = '/media/'

STATIC_ROOT = PROJECT_ROOT.ancestor(2).child("localstorage").child("static")
STATIC_URL = '/static/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

BROKER_URL = "amqp://guest:guest@localhost:5672//"
CELERY_RESULT_BACKEND = "amqp"
