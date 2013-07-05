from timezone_field import TimeZoneField

from django.db import models

from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    nickname = models.CharField(max_length=25, blank=True, unique=True)
    timezone = TimeZoneField(blank=True, null=True)
    prediction = models.TextField(blank=True)
