from timezone_field import TimeZoneField

from django.db import models

from django.conf import settings


class Profile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL
    )

    nickname = models.CharField(
        max_length=25,
        blank=True,
        unique=True,
    )

    timezone = TimeZoneField(
        default='America/Los_Angeles'
    )

    def __unicode__(self):
        # TODO how to access username attr?
        return self.user.mobile
