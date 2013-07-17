from .base import *

from memcacheify import memcacheify

DEBUG = bool(get_env_variable("DJANGO_DEBUG"))
TEMPLATE_DEBUG = DEBUG

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

AWS_ACCESS_KEY_ID = get_env_variable("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env_variable("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = get_env_variable("AWS_STORAGE_BUCKET_NAME")


DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'

DEFAULT_S3_PATH = "media"
STATIC_S3_PATH = "static"


INSTALLED_APPS += (
    'storages',
    'raven.contrib.django.raven_compat',
    's3_folder_storage',
)

RAVEN_CONFIG = {
    'dsn': get_env_variable("SENTRY_DSN"),
}

MEDIA_ROOT = "/{0}/".format(DEFAULT_S3_PATH)
STATIC_ROOT = "/{0}/".format(STATIC_S3_PATH)

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
        'URL': get_env_variable('SEARCHBOX_URL'),
        'INDEX_NAME': 'haystack',
    },
}

CACHES = memcacheify()

BROKER_URL = get_env_variable("CLOUDAMQP_URL")
CELERY_RESULT_BACKEND = "amqp"
BROKER_POOL_LIMIT = 1


NONCENSE_SERVER = {
    'default': {
        # 'BACKEND': '',
        'URL': 'http://noncense.herokuapp.com/',
        'CONSUMER_ID': get_env_variable("NONCENSE_CONSUMER_ID"),
        'CONSUMER_SECRET': get_env_variable("NONCENSE_CONSUMER_SECRET"),
    }
}
