release: django-admin migrate api --noinput
web: waitress-serve --port=$PORT project.wsgi:application
