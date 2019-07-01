# Barberscore API

This is the back-end API that powers the new scoring system for the Barbershop Harmony Society.

## Getting Started

This API is based on [Django](http://www.djangoproject.com) and the [Django Rest Framework](http://www.django-rest-framework.org).  Here are the basics to set up your local environment.

### Prerequisites

You will need the latest versions of the following core dependencies properly installed on your computer.

* [Git](https://git-scm.com)
* [Python 3](https://www.python.org)
* [PostgreSQL](https://www.postgresql.org)
* [MySQL](https://www.mysql.com)
* [Redis](https://redis.io)
* [Pipenv](https://docs.pipenv.org)


### Installation

Run these commands to get started

* `git clone https://github.com/barberscore/barberscore-api.git` (this repo)
* `cd barberscore-api`
* `pipenv sync --dev`
* `createdb barberscore`


### Configuration

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

CLOUDINARY_URL=(your credentials here)

WKHTMLTOPDF_PATH=/usr/local/bin/wkhtmltopdf (or your path)
```

### Running

Run these commands to start the app.

* `django-admin flush`
* `django-admin migrate`
* `django-admin seed_data`
* `django-admin runserver`
* Visit your app at [http://localhost:8000](http://localhost:8000)
* The initial login credentials are `admin@barberscore.com/password`

### Support

If you have any questions let us know at admin@barberscore.com!
