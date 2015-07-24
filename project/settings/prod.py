from .base import *

import sys

# AWS S3  Settings
# This was hellaciously confusing to set up.
# `Static` means public-read, static resources like CSS, Images, etc.
# `Media` means private, user or admin-uploaded resources that have ACL


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Configure AWS variables
# Access credentials (global)
AWS_ACCESS_KEY_ID = get_env_variable("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env_variable("AWS_SECRET_ACCESS_KEY")
AWS_PRELOAD_METADATA = True

# Static Server Config
AWS_STATIC_BUCKET_NAME = "{0}".format(PROJECT_NAME)
STATIC_STORAGE = 'backends.StaticS3BotoStorage'
STATIC_URL = 'https://{0}.s3-us-west-1.amazonaws.com/'.format(
    AWS_STATIC_BUCKET_NAME,
)

# Media (aka File Upload) Server Config
AWS_MEDIA_BUCKET_NAME = "{0}".format(PROJECT_NAME)
MEDIA_STORAGE = 'backends.MediaS3BotoStorage'
MEDIA_URL = 'https://{0}.s3-us-west-1.amazonaws.com/'.format(
    AWS_MEDIA_BUCKET_NAME,
)

# Aliasing Django Defaults
DEFAULT_FILE_STORAGE = MEDIA_STORAGE
STATICFILES_STORAGE = STATIC_STORAGE


EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'
MANDRILL_API_KEY = get_env_variable("MANDRILL_APIKEY")
DEFAULT_FROM_EMAIL = 'noreply@barberscore.com'

# Haystack
from urlparse import urlparse
es = urlparse(get_env_variable("SEARCHBOX_URL"))

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': es.scheme + '://' + es.hostname + ':80',
        'INDEX_NAME': 'haystack',
        'KWARGS': {"http_auth": es.username + ':' + es.password},
    },
}

ALLOWED_HOSTS = [
    get_env_variable("HEROKU_HOST"),
    'api.barberscore.com',
]

INSTALLED_APPS += (
    'djrill',
)
