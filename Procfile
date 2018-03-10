web: gunicorn project.wsgi
release: python manage.py migrate api --noinput
worker: python manage.py rqworker high default --sentry-dsn=https://e221a00f63e5411680e1a91ddd38c6b2:ee5d09aaca9a4040a89efebf83c64af7@sentry.io/294985
