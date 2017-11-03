web: waitress-serve --port=$PORT project.wsgi:application
release: django-admin migrate api --noinput
worker: django-admin rqworker default
