from django.db import models
import uuid
from django.core.exceptions import ValidationError

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
        related_name='oldflats',
    )
    class Meta:
        unique_together = (
            ('complete', 'selection', 'score'),
        )

    def clean(self):
        if self.complete.panelist.round != self.selection.song.appearance.round:
            raise ValidationError('Rounds do not match')
