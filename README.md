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

You'll need to set the following Environment Variables:
```
DJANGO_SETTINGS_MODULE='settings.dev'
PYTHONPATH="project"
SECRET_KEY=(your secret here)

DATABASE_URL=(your credentials here)

AUTH0_CLIENT_ID='C68OwqrFDjUa6lv8t4jZQPDksWmrtvoF'
AUTH0_CLIENT_SECRET=(get from admin)
AUTH0_DOMAIN='barberscore-dev.auth0.com'
AUTH0_API_ID='SUFlInihKYP3Dt7FNVRMFnyZE5aujqym'
AUTH0_API_SECRET=(get from admin)
AUTH0_AUDIENCE='https://barberscore-dev.auth0.com/api/v2/'
AUTH0_PUBLIC_KEY="-----BEGIN CERTIFICATE-----
MIIC+jCCAeKgAwIBAgIJbuZM6FlzJ6TDMA0GCSqGSIb3DQEBBQUAMCQxIjAgBgNV
BAMTGWJhcmJlcnNjb3JlLWRldi5hdXRoMC5jb20wHhcNMTYxMDI2MjAzNDE0WhcN
MzAwNzA1MjAzNDE0WjAkMSIwIAYDVQQDExliYXJiZXJzY29yZS1kZXYuYXV0aDAu
Y29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArktLSct+7BT6SDLJ
k6P7esPEk2rWTd6+S97gB8oZ9I4WTiGx7jsPgoYn9pUltnHF2r0N1WuOM8UCUMfk
b/lwHcpBGsNx2cxsvr0oVsgKEynJNn0ynRCR2EH7b/iYrtOtMyE1CXtMMgT9vMhS
e/mE8VxsTvgev1nQmR8lq/jXZvLY068/BbicWsrJ11/7toSiJEMH3yEwzlK7ZRDj
Oorp0sp3//ZCZeP4ep9SwK/dNthUgAe1yfQokKQCnW5aMYYZgMG4RDIKND28PGMe
7QmesTbSzoXTPDZBMLJC0o/CSZlQrPzg5SmfyGO0sl+ZnWt9PBeCYjLgtBbKDOH9
o8gNTQIDAQABoy8wLTAMBgNVHRMEBTADAQH/MB0GA1UdDgQWBBS9m0sa23+rX1a1
3/2+h9f2UTlrzDANBgkqhkiG9w0BAQUFAAOCAQEALsbWOoKVb4hEFl7akai9bqRK
DMxXf6ZBu7tQMFVDE3xr5Rzc11aeyUCWA9oIrv07JNHQI1OPrXHSKdd+UDAiO2N1
pTIfrOjySNxBoTkr0IJWp+SQjiNr+vvbJGSgThvebHmxNVIQ+WQosVmWHobuZ+tF
LXyoMAxse01/vNGW3LqsMWG32icIQ4Xra2wKmXag/oQGlu4NASRuEhtP8Lp47v1D
m+rablf5MmFd3dtErVU9a3cqeGUEIjYhTK18slv55LOEdMPklRgkDUlvCIxd3RA1
yZw/f9vAojVPQmXNY95Kzg14aqhiRGSeNhG6BRMnDvzm3/rx4UezNmLxT6F1cg==
-----END CERTIFICATE-----
"

DOCRAPTOR_API_KEY=(sign up at https://docraptor.com)

CLOUDINARY_URL=(sign up at https://cloudinary.com)
```

Next, set up your local environment:
  - Create local database.
  - Run `django-admin migrate` from the location of the cloned repo.
  - Create a super user via `django-admin createsuperuser`.

You may also wish to seed the database with sample data using:
  - `django-admin seed_database`

If you have any questions let us know at admin@barberscore.com!
