from .base import *

DEBUG = bool(get_env_variable("DJANGO_DEBUG"))
TEMPLATE_DEBUG = DEBUG

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

AWS_ACCESS_KEY_ID = get_env_variable("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env_variable("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = get_env_variable("AWS_STORAGE_BUCKET_NAME")

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

INSTALLED_APPS += (
    'storages',
    'raven.contrib.django.raven_compat',
)

RAVEN_CONFIG = {
    'dsn': get_env_variable("SENTRY_DSN"),
}

STATIC_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/static/'
MEDIA_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/media/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'


ALLOWED_HOSTS = [get_env_variable("HEROKU_HOST")]

EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = get_env_variable("MANDRILL_USERNAME")
EMAIL_HOST_PASSWORD = get_env_variable("MANDRILL_APIKEY")
EMAIL_SUBJECT_PREFIX = '[Barberscore] '

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}

# os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '')
# os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
# os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

MEMCACHE_SERVERS = get_env_variable('MEMCACHIER_SERVERS')
MEMCACHE_USERNAME = get_env_variable('MEMCACHIER_USERNAME')
MEMCACHE_PASSWORD = get_env_variable('MEMCACHIER_PASSWORD')

CACHES = {
    'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': MEMCACHE_SERVERS,
        'TIMEOUT': 500,
        'BINARY': True,
    }
}
