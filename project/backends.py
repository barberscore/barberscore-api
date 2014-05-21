from django.conf import settings

from storages.backends.s3boto import S3BotoStorage


class MediaS3BotoStorage(S3BotoStorage):
    """Extends storage class to provide a private bucket."""
    def __init__(self, *args, **kwargs):
        super(MediaS3BotoStorage, self).__init__(
            bucket=settings.AWS_MEDIA_BUCKET_NAME,
            acl='private',
            querystring_auth=True,
            querystring_expire=60,
            *args, **kwargs
        )


class StaticS3BotoStorage(S3BotoStorage):
    """Passes the origin Storage through, but can be customized"""
    def __init__(self, *args, **kwargs):
        super(StaticS3BotoStorage, self).__init__(
            bucket=settings.AWS_STATIC_BUCKET_NAME,
            acl='public-read',
            querystring_auth=False,
            *args, **kwargs
        )
