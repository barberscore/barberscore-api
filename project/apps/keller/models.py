import uuid

from model_utils import Choices

from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models

from .managers import RawPanelistManager
from .managers import CompleteManager
from .managers import SelectionManager


class RawPanelist(models.Model):
    id = models.IntegerField(
        primary_key=True,
        editable=False,
    )
    year = models.IntegerField(
    )
    season = models.CharField(
        max_length=255,
    )
    district = models.CharField(
        max_length=255,
    )
    convention = models.CharField(
        max_length=255,
    )
    session = models.CharField(
        max_length=255,
    )
    round = models.CharField(
        max_length=255,
    )
    category = models.CharField(
        max_length=255,
    )
    judge = models.CharField(
        max_length=255,
    )
    points = JSONField(
    )
    objects = RawPanelistManager()


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
        'api.score',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    class Meta:
        unique_together = (
            ('complete', 'selection', 'score'),
        )

    def clean(self):
        if self.complete.panelist.round != self.selection.song.appearance.round:
            raise ValidationError('Rounds do not match')


class Selection(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    mark = models.BooleanField(
        default=False,
    )

    row_id = models.IntegerField(
        null=True,
        blank=True,
    )

    year = models.IntegerField(
        null=True,
        blank=True,
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

    song = models.OneToOneField(
        'api.song',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    objects = SelectionManager()


class Complete(models.Model):
    """LCD: Panelist"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    row_id = models.IntegerField(
        null=True,
        blank=True,
    )

    year = models.IntegerField(
        null=True,
        blank=True,
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

    SEASON = Choices(
        (1, 'summer', 'Summer',),
        (2, 'midwinter', 'Midwinter',),
        (3, 'fall', 'Fall',),
        (4, 'spring', 'Spring',),
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

    CATEGORY_KIND = Choices(
        (30, 'mus', 'Music'),
        (40, 'per', 'Performance'),
        (50, 'sng', 'Singing'),
    )

    category_kind = models.IntegerField(
        null=True,
        blank=True,
        choices=CATEGORY_KIND
    )

    points = ArrayField(
        base_field=models.IntegerField(
            null=True,
            blank=True,
        ),
        null=True,
        blank=True,
    )

    person = models.ForeignKey(
        'bhs.person',
        related_name='completes',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    panelist = models.OneToOneField(
        'api.panelist',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    objects = CompleteManager()
