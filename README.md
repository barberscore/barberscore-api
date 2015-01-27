
[![Circle CI](https://circleci.com/gh/dbinetti/barberscore.svg?style=svg)](https://circleci.com/gh/dbinetti/barberscore)

# Barberscore


Program and score tracker for the Barbershop Harmony Society International Convention.

## Preface
The purpose of this project is to provide a simple, mobile-friendly app to track the performances at the International Convention of the BHS.

## Contributors
Big thank you to Alexander Boltenko with the Heralds of Harmony in Tampa, FL, who has hand-entered all the data and is keeping things up to date.  Great Job @russkibass!

## Installation
The site is built on the Django framework.  I'll go through (very opinionated) installation instructions below.  If you'd like to go off the reservation by all means feel free; I'm not going to explain the differences between MySQL and Postgres, etc.  Also, these instructions assume you're installing on a Mac because:
  - If you're on Linux you know what to do already.
  - If you're on Windows I can't help you.

### Install Basic Services
We need three basic services:
  - Python 2.7.6
  - PostgreSQL 9.3.x
  - ElasticSearch 1.2.x

First install [virtualenvwrapper] (http://virtualenvwrapper.readthedocs.org/en/latest/) and run `mkvirtualenv barberscore` to create a new, clean development environment.  Virtualenv will install Python, setuptools, and pip automatically.

Then, install [Homebrew] (http://brew.sh) and run `brew install postgres` and `brew install elasticsearch`.

~~~
NOTE:  The above steps are actually quite involved.  There is lots of adjusting PATH variables and initializing databases and what not; I can't go through all the details but just know that even with virtualenv and homebrew the task is not necessarily simple.
~~~

When postgres is ready, run `createdb barberscore` to get a database up.  We'll create the schema later.

### Install Dependencies
Next, cd to the directory where you keep your repos and run `git clone git@github.com:dbinetti/barberscore` to get the code.  When things are downloaded, run `pip install -r requirements/dev.txt` to load the dependencies for the python environment.  It will take a few minutes.

When that is done, `deactivate` use a text editor to open your postactivate script for your virtualenv (the default location will be `~/.virtualenvs/barberscore/bin/postactivate`).  There, we'll need to set some environment variables the app depends on.  Update that file to look something like this:

```#!/bin/bash
# This hook is run after this virtualenv is activated.

export PYTHONPATH=~/{{YOUR REPO PATH}}/barberscore/project/
export DJANGO_SETTINGS_MODULE='settings.dev'

export SECRET_KEY='{{SOME SECRET KEY}}'
export DATABASE_URL='postgres://{{DATABASE USER NAME}}:{{DATABASE PASSWORD}}@localhost/barberscore'
export DJANGO_DEBUG=true

export FULL_NAME="{{YOUR NAME}}"
export USER_EMAIL="{{YOUR EMAIL}}"

export BONSAI_URL='http://localhost:9200/'

export TWILIO_ACCOUNT_SID='ACb1b9bca9ccef183757e6ebdb64d063c3'
export TWILIO_AUTH_TOKEN='41bd31f387ba44b7bfd7cf4965ce06f7'
export TWILIO_FROM_NUMBER='+15005550006'

```

We adhere to a [12-factor] (http://12factor.net/) approach and this keeps sensitive data out of version control.  Note that these twilio variables are testing credentials and won't work under other circumstances.

When that is saved, reactivate your virtual env with `workon barberscore` and move on.

### Start Django
With everything in place you should now simply need to start Django with the followings steps.

run `django-admin migrate` to load the database schema.

once loaded, run `django-admin loaddata project/apps/convention/init.json` to load the most current fixture (based off the production data.)

<<placeholder; need to find a way to load media gracefully>>

Change any settings you might want to change, but otherwise it's simply `django-admin runserver` and you're good to go!

