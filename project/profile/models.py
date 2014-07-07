from __future__ import division

from django.conf import settings

import pytz

from django.db import models

from convention.models import (
    Contestant,
)


class Profile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL
    )

    nickname = models.CharField(
        max_length=25,
        blank=True,
    )

    timezone = models.CharField(
        max_length=200,
        default='US/Pacific',
        choices=[(x, x) for x in pytz.common_timezones],
    )

    def __unicode__(self):
        # TODO how to access username attr?
        if self.nickname:
            return self.nickname
        else:
            return self.user.mobile


class Note(models.Model):

    profile = models.ForeignKey(
        Profile,
        related_name='notes',
    )

    contestant = models.ForeignKey(
        Contestant,
        related_name='notes',
    )

    note = models.TextField(
        help_text="""
            Notes on each contestant."""
    )

    def __unicode__(self):
        return "{0} - {1}".format(self.profile, self.contestant)
