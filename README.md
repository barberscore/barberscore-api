# Barberscore

This is the back-end API that powers the new scoring system for the Barbershop Harmony Society.

## Installation Notes

This API is based on Django and the Django Rest Framework.  Here are the basics to set up your local environment.

Clone the repo (assumes `git` is being used).

Install the core dependencies (all are latest versions):
    - Python 3
    - PostgreSQL
    - MySQL
    - Redis
    - Pipenv

Use `pipenv` to install python dependencies.
```
pipenv sync --dev
```


Set the following Environment Variables:
Note: if you don't have credentials, talk to the Barberscore Admin.
```
DJANGO_SETTINGS_MODULE=settings.dev
PYTHONPATH=project
SECRET_KEY=(your secret here)

DATABASE_URL=(your credentials here)
BHS_DATABASE_URL=(your credentials here)
REDIS_URL=(your credentials here)

AUTH0_CLIENT_ID=(your credentials here)
AUTH0_CLIENT_SECRET=(your credentials here)
AUTH0_DOMAIN=(your credentials here)
AUTH0_API_ID=(your credentials here)
AUTH0_API_SECRET=(your credentials here)
AUTH0_AUDIENCE=(your credentials here)

CLOUDINARY_URL=(your credentials here)

WKHTMLTOPDF_PATH=/usr/local/bin/wkhtmltopdf (or your path)

```

Next, set up your local environment:
    - `createdb barberscore`
    - Run `django-admin migrate`.
    - Run `django-admin seed_data`.
    - Go to http://localhost:8000 and login with `admin@barberscore.com/password`.

If you have any questions let us know at admin@barberscore.com!