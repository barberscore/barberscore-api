from django.db import models
import uuid
from model_utils import Choices
from django.contrib.postgres.fields import ArrayField

class Selection(models.Model):
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

    season_raw = models.CharField(
        blank=True,
        max_length=255,
    )

    district_raw = models.CharField(
        blank=True,
        max_length=255,
    )

    event_raw = models.CharField(
        blank=True,
        max_length=255,
    )

    session_raw = models.CharField(
        blank=True,
        max_length=255,
    )

    SEASON = Choices(
        (1, 'summer', 'Summer',),
        (2, 'midwinter', 'Midwinter',),
        (3, 'fall', 'Fall',),
        (4, 'spring', 'Spring',),
    )

    season_kind = models.IntegerField(
        null=True,
        blank=True,
        choices=SEASON
    )

    district_code = models.CharField(
        blank=True,
        max_length=255,
    )

    convention_name = models.CharField(
        blank=True,
        max_length=255,
    )

    SESSION_KIND = Choices(
        (32, 'chorus', "Chorus"),
        (41, 'quartet', "Quartet"),
        (42, 'mixed', "Mixed"),
        (43, 'senior', "Senior"),
        (44, 'youth', "Youth"),
        (45, 'unknown', "Unknown"),
        (46, 'vlq', "VLQ"),
    )

    session_kind = models.IntegerField(
        null=True,
        blank=True,
        choices=SESSION_KIND
    )

    ROUND_KIND = Choices(
        (1, 'finals', 'Finals'),
        (2, 'semis', 'Semi-Finals'),
        (3, 'quarters', 'Quarter-Finals'),
    )

    round_kind = models.IntegerField(
        null=True,
        blank=True,
        choices=ROUND_KIND
    )

    group_name = models.CharField(
        blank=True,
        max_length=255,
    )

    appearance_num = models.IntegerField(
        null=True,
        blank=True,
    )

    song_num = models.IntegerField(
        null=True,
        blank=True,
    )

    song_title = models.CharField(
        blank=True,
        max_length=255,
    )

    totals = models.IntegerField(
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

    num_sessions = models.IntegerField(
        null=True,
        blank=True,
    )

    num_rounds = models.IntegerField(
        null=True,
        blank=True,
    )

    num_appearances = models.IntegerField(
        null=True,
        blank=True,
    )

    num_panelists = models.IntegerField(
        null=True,
        blank=True,
    )

    song = models.OneToOneField(
        'Song',
        on_delete=models.CASCADE,
    )
