from django.db import models
import uuid

class Flat(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    points = models.IntegerField(
        null=True,
        blank=True,
    )
    complete = models.ForeignKey(
        'Complete',
        related_name='flats',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    selection = models.ForeignKey(
        'Selection',
        related_name='flats',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    score = models.OneToOneField(
        'Score',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
