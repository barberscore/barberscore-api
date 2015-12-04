from .base import *

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--nologcapture',
    '--with-coverage',
    '--cover-package=apps.api',
]

INSTALLED_APPS += (
    'django_nose',
)
