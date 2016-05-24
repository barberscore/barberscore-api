# Django
from django.conf import settings

# First-Party
from storages.backends.s3boto import S3BotoStorage


class FixedS3BotoStorage(S3BotoStorage):
    """
    fix the broken javascript admin resources with S3Boto on Django 1.4
    for more info see http://code.larlet.fr/django-storages/issue/121/s3boto-admin-prefix-issue-with-django-14
    """
    def url(self, name):
        url = super(FixedS3BotoStorage, self).url(name)
        if name.endswith('/') and not url.endswith('/'):
            url += '/'
        return url


class MediaS3BotoStorage(FixedS3BotoStorage):
    """Passes the origin Storage through, but can be customized"""
    def __init__(self, *args, **kwargs):
        super(MediaS3BotoStorage, self).__init__(
            bucket=settings.AWS_MEDIA_BUCKET_NAME,
            acl='public-read',
            querystring_auth=False,
            location="files",
            *args, **kwargs
        )


class StaticS3BotoStorage(FixedS3BotoStorage):
    """Passes the origin Storage through, but can be customized"""
    def __init__(self, *args, **kwargs):
        super(StaticS3BotoStorage, self).__init__(
            bucket=settings.AWS_STATIC_BUCKET_NAME,
            acl='public-read',
            querystring_auth=False,
            location="static",
            *args, **kwargs
        )
