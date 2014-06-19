import pytz

from django.db import models

from django.conf import settings


class Profile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL
    )

    nickname = models.CharField(
        max_length=25,
        blank=True,
    )

# timezone = forms.ChoiceField(choices=[(x, x) for x in pytz.common_timezones])

    timezone = models.CharField(
        max_length=200,
        default='US/Pacific',
        choices=[(x, x) for x in pytz.common_timezones],
    )

    def __unicode__(self):
        # TODO how to access username attr?
        return self.user.mobile
