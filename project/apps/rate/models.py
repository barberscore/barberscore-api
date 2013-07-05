# import pytz

from timezone_field import TimeZoneField

from django.db import models

from django.conf import settings

from django.core.validators import MaxValueValidator, MinValueValidator

from apps.bbs.models import Performance


# class UserProfile(models.Model):
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
