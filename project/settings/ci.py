from .base import *

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--nologcapture',
]

INSTALLED_APPS += (
    'django_nose',
)
