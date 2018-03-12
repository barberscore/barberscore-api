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
