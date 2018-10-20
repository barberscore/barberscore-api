from django.db import models
import uuid
from model_utils import Choices

class Flat(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    year = models.IntegerField(
        null=True,
        blank=True,
    )

    district_code = models.CharField(
        blank=True,
        max_length=255,
    )

    SEASON_KIND = Choices(
        (1, 'summer', 'Summer',),
        (2, 'midwinter', 'Midwinter',),
        (3, 'fall', 'Fall',),
        (4, 'spring', 'Spring',),
    )

    season_kind = models.IntegerField(
        null=True,
        blank=True,
        choices=SEASON_KIND
    )

    complete_name = models.CharField(
        blank=True,
        max_length=255,
    )

    selection_name = models.CharField(
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

    CATEGORY = Choices(
        (30, 'music', 'Music'),
        (40, 'performance', 'Performance'),
        (50, 'singing', 'Singing'),
    )

    category = models.IntegerField(
        null=True,
        blank=True,
        choices=CATEGORY
    )

    appearance_num = models.IntegerField(
        null=True,
        blank=True,
    )

    song_num = models.IntegerField(
        null=True,
        blank=True,
    )

    panelist_num = models.IntegerField(
        null=True,
        blank=True,
    )

    points = models.IntegerField(
        null=True,
        blank=True,
    )

    panelist_name = models.CharField(
        blank=True,
        max_length=255,
    )

    group_name = models.CharField(
        blank=True,
        max_length=255,
    )

    song_title = models.CharField(
        blank=True,
        max_length=255,
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

    convention = models.ForeignKey(
        'Convention',
        related_name='flats',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    session = models.ForeignKey(
        'Session',
        related_name='flats',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    round = models.ForeignKey(
        'Round',
        related_name='flats',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    panelist = models.ForeignKey(
        'Panelist',
        related_name='flats',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    appearance = models.ForeignKey(
        'Appearance',
        related_name='flats',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    song = models.ForeignKey(
        'Song',
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
    group = models.ForeignKey(
        'Group',
        related_name='flats',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    person = models.ForeignKey(
        'Person',
        related_name='flats',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
