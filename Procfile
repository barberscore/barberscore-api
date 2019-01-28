web: gunicorn project.wsgi
release: django-admin migrate api --noinput
worker: django-admin rqworker high default low -c prod --sentry-dsn=""
