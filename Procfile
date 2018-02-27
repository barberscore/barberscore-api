web: gunicorn project.wsgi
release: django-admin migrate api --noinput
worker: django-admin rqworker high default --sentry-dsn=https://e221a00f63e5411680e1a91ddd38c6b2:ee5d09aaca9a4040a89efebf83c64af7@sentry.io/294985
