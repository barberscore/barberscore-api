# Standard Libary
from .base import *


# Database
DATABASES['bhs_db'] = dj_database_url.parse(
    get_env_variable("BHS_DATABASE_URL"),
    conn_max_age=600,
)

DATABASE_ROUTERS = [
    'routers.BHSRouter',
]

# Staticfiles
CLOUDINARY_URL = get_env_variable("CLOUDINARY_URL")
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
# STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'

# Email
EMAIL_BACKEND = get_env_variable("EMAIL_BACKEND")
EMAIL_PORT = get_env_variable("EMAIL_PORT")

# Auth0
AUTH0_CLIENT_ID = get_env_variable("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = get_env_variable("AUTH0_CLIENT_SECRET")
AUTH0_DOMAIN = get_env_variable("AUTH0_DOMAIN")
AUTH0_API_ID = get_env_variable("AUTH0_API_ID")
AUTH0_API_SECRET = get_env_variable("AUTH0_API_SECRET")
AUTH0_AUDIENCE = get_env_variable("AUTH0_AUDIENCE")


def jwt_get_username_from_payload_handler(payload):
    """Switch to email as JWT username payload."""
    return payload.get('email')

from cryptography import x509
from cryptography.hazmat.backends import default_backend


cert = get_env_variable("AUTH0_CERTIFICATE")
pem_data = cert.encode()
cert = x509.load_pem_x509_certificate(pem_data, default_backend())
jwt_public_key = cert.public_key()

JWT_AUTH = {
    'JWT_AUDIENCE': AUTH0_CLIENT_ID,
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': jwt_get_username_from_payload_handler,
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_PUBLIC_KEY': jwt_public_key,
    'JWT_ALGORITHM': 'RS256',
}

# Algolia
ALGOLIA = {
    'APPLICATION_ID': get_env_variable("ALGOLIASEARCH_APPLICATION_ID"),
    'API_KEY': get_env_variable("ALGOLIASEARCH_API_KEY"),
    'AUTO_INDEXING': get_env_variable("ALGOLIASEARCH_AUTO_INDEXING"),
    'INDEX_SUFFIX': get_env_variable("ALGOLIASEARCH_INDEX_SUFFIX"),
}

# Applications
INSTALLED_APPS += [
    'cloudinary_storage',
    'cloudinary',
    'algoliasearch_django',
]
