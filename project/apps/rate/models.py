from django.db import models

from django.conf import settings

from django.core.validators import MaxValueValidator, MinValueValidator

from apps.bbs.models import Performance


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    performance = models.ForeignKey(Performance, null=True)
    song_one = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    song_two = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    notes = models.TextField(blank=True)
