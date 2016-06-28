# Local
from .base import *

# AWS S3  Settings
# `Static` means public-read, static resources like CSS, Images, etc.
# `Media` means user or admin-uploaded resources

# Configure AWS variables
AWS_ACCESS_KEY_ID = get_env_variable("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env_variable("AWS_SECRET_ACCESS_KEY")
AWS_PRELOAD_METADATA = True
AWS_REGION = "us-west-1"
AWS_S3_KEY_PREFIX = "files/"
AWS_S3_KEY_PREFIX_STATIC = "static/"
AWS_S3_BUCKET_AUTH = False
AWS_S3_BUCKET_NAME = "{0}".format(PROJECT_NAME)
AWS_S3_BUCKET_NAME_STATIC = "{0}".format(PROJECT_NAME)
AWS_S3_MAX_AGE_SECONDS_STATIC = 60 * 60  # 1 hour

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static Server Config
STATIC_STORAGE = 'django_s3_storage.storage.StaticS3Storage'
# STATIC_URL = 'https://{0}.s3-us-west-1.amazonaws.com/'.format(
#     AWS_STATIC_BUCKET_NAME,
# )

# Media (File Upload) Server Config
AWS_MEDIA_BUCKET_NAME = "{0}".format(PROJECT_NAME)
MEDIA_STORAGE = 'django_s3_storage.storage.S3Storage'
# MEDIA_URL = 'https://{0}.s3-us-west-1.amazonaws.com/'.format(
#     AWS_MEDIA_BUCKET_NAME,
# )

# Aliasing Django Defaults
DEFAULT_FILE_STORAGE = MEDIA_STORAGE
STATICFILES_STORAGE = STATIC_STORAGE

# CORS Settings
CORS_ORIGIN_WHITELIST = (
    'barberscore-ember.herokuapp.com',
    'barberscore.com',
    'barberscore.s3.amazonaws.com',
)

# Email
DEFAULT_FROM_EMAIL = 'admin@barberscore.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = get_env_variable("SENDGRID_USERNAME")
EMAIL_HOST_PASSWORD = get_env_variable("SENDGRID_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True

ALLOWED_HOSTS = [
    get_env_variable("HEROKU_HOST"),
    'api.barberscore.com',
]

INSTALLED_APPS += (
    'django_s3_storage',
)
