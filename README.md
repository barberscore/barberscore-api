# Barberscore

This is the back-end API that powers the new scoring system for the Barbershop Harmony Society.

## Installation Notes

This API is based on Django and the Django Rest Framework.  Here are the basics to set up your local environment.

Clone the repo.

Install the core platform:
  - PostgreSQL 9.6
  - Python 3.6
  - Pip 9.0

Use Pip to install all the dev requirements via the `pip -r project/requirements/dev.txt` command.  

Next, set up your local environment:
  - Create local database.
  - Run `django-admin migrate` from the location of the cloned repo.
  - Create a super user via `django-admin createsuperuser`.

You may also wish to seed the database with sample data using:
  - `django-admin seed_database`

If you have any questions let us know at admin@barberscore.com!
