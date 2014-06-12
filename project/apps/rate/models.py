# import pytz

from timezone_field import TimeZoneField

from django.db import models

from django.conf import settings

from django.core.validators import MaxValueValidator, MinValueValidator

from apps.convention.models import (
    Performance,
    Contestant,
)


# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL)
#     first_name = models.CharField(max_length=200, blank=True)
#     last_name = models.CharField(max_length=200, blank=True)
#     nickname = models.CharField(max_length=25, blank=True, unique=True)
#     timezone = TimeZoneField(blank=True, null=True)
#     prediction = models.TextField(blank=True)


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    performance = models.ForeignKey(Performance, null=True)
    song_one = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    song_two = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    notes = models.TextField(blank=True)


class Prediction(models.Model):

    TOP_TEN = (
        (40, 'A Mighty Wind'),
        (45, 'After Hours'),
        (32, 'Da Capo'),
        (48, 'Forefront'),
        (31, 'Main Street'),
        (39, 'Masterpiece'),
        (24, 'Musical Island Boys'),
        (29, 'The Crush'),
        (44, 'Throwback'),
        (4, 'Via Voice'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    first = models.IntegerField(null=True, blank=True, choices=TOP_TEN)
    second = models.IntegerField(null=True, blank=True, choices=TOP_TEN)
    third = models.IntegerField(null=True, blank=True, choices=TOP_TEN)
    fourth = models.IntegerField(null=True, blank=True, choices=TOP_TEN)
    fifth = models.IntegerField(null=True, blank=True, choices=TOP_TEN)
    sixth = models.IntegerField(null=True, blank=True, choices=TOP_TEN)
    seventh = models.IntegerField(null=True, blank=True, choices=TOP_TEN)
    eigth = models.IntegerField(null=True, blank=True, choices=TOP_TEN)
    ninth = models.IntegerField(null=True, blank=True, choices=TOP_TEN)
    tenth = models.IntegerField(null=True, blank=True, choices=TOP_TEN)

    def __unicode__(self):
        return self.user
