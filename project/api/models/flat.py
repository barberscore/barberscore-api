from django.db import models
import uuid

class Flat(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    complete = models.ForeignKey(
        'Complete',
        related_name='flats',
        on_delete=models.CASCADE,
    )
    selection = models.ForeignKey(
        'Selection',
        related_name='flats',
        on_delete=models.CASCADE,
    )
    score = models.OneToOneField(
        'Score',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    class Meta:
        unique_together = (
            ('complete', 'selection', 'score'),
        )
