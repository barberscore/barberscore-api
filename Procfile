web: gunicorn project.wsgi
release: django-admin migrate --noinput
worker: django-admin rqworker high default low
