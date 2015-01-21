from .base import *

BUGSNAG = {
    "api_key": get_env_variable("BUGSNAG"),
    "project_root": PROJECT_ROOT,
}

MIDDLEWARE_CLASSES += (
    "bugsnag.django.middleware.BugsnagMiddleware",
)
