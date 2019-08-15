web: gunicorn project.wsgi
release: django-admin migrate --noinput && sentry-cli releases new $HEROKU_SLUG_COMMIT --finalize && sentry-cli releases set-commits $HEROKU_SLUG_COMMIT --auto
worker: django-admin rqworker high default low
