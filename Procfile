web: gunicorn project.wsgi
release: django-admin migrate --noinput && sentry-cli releases new $HEROKU_SLUG_COMMIT --finalize
worker: django-admin rqworker high default low
