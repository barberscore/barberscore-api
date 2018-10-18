from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField

class Complete(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    mark = models.BooleanField(
        default=False,
    )

    row = models.IntegerField(
        null=True,
        blank=True,
    )

    year = models.IntegerField(
        null=True,
        blank=True,
    )

    season = models.CharField(
        blank=True,
        max_length=255,
    )

    district = models.CharField(
        blank=True,
        max_length=255,
    )

    convention_raw = models.CharField(
        blank=True,
        max_length=255,
    )

    session_raw = models.CharField(
        blank=True,
        max_length=255,
    )

    round_raw = models.CharField(
        blank=True,
        max_length=255,
    )

    category = models.CharField(
        blank=True,
        max_length=255,
    )

    panelist_name = models.CharField(
        blank=True,
        null=True,
        max_length=255,
    )

    panelist_num = models.IntegerField(
        null=True,
        blank=True,
    )
    points = ArrayField(
        base_field=models.IntegerField(
            null=True,
            blank=True,
        ),
        null=True,
        blank=True,
    )
    num_appearances = models.IntegerField(
        null=True,
        blank=True,
    )

    num_rounds = models.IntegerField(
        null=True,
        blank=True,
    )

    num_panelists = models.IntegerField(
        null=True,
        blank=True,
    )

    convention = models.ForeignKey(
        'Convention',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    session = models.ForeignKey(
        'Session',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    round = models.ForeignKey(
        'Round',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    panelist = models.ForeignKey(
        'Panelist',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
