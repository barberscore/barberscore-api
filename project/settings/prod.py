# Local
from .base import *

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

# CORS Settings
CORS_ORIGIN_WHITELIST = (
    'barberscore-ember.herokuapp.com',
    'barberscore.com',
    'barberscore.s3.amazonaws.com',
)

# Email
EMAIL_BACKEND = "sgbackend.SendGridBackend"
SENDGRID_USER = get_env_variable("SENDGRID_USERNAME")
SENDGRID_PASSWORD = get_env_variable("SENDGRID_PASSWORD")
DEFAULT_FROM_EMAIL = 'admin@barberscore.com'

ALLOWED_HOSTS = [
    get_env_variable("HEROKU_HOST"),
    'api.barberscore.com',
]
