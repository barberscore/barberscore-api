from __future__ import division

from django.db import models


class Contestant(models.Model):
    """The name of the contestant"""

    QUARTET = 1
    CHORUS = 2

    CONTESTANT_CHOICES = (
        (QUARTET, "Quartet"),
        (CHORUS, "Chorus"),
    )

    contestant_type = models.IntegerField(
        blank=True,
        null=True,
        choices=CONTESTANT_CHOICES
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    location = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    website2 = models.CharField(blank=True, null=True, max_length=200)
    facebook2 = models.CharField(blank=True, null=True, max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    director = models.CharField(max_length=200, blank=True)
    lead = models.CharField(max_length=200, blank=True)
    tenor = models.CharField(max_length=200, blank=True)
    baritone = models.CharField(max_length=200, blank=True)
    bass = models.CharField(max_length=200, blank=True)
    district = models.CharField(max_length=200, blank=True)
    prelim = models.FloatField(null=True, blank=True)
    picture = models.ImageField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['contestant_type']


class Contest(models.Model):

    QUARTET = 1
    CHORUS = 2
    COLLEGIATE = 3
    SENIOR = 4

    CONTEST_TYPE_CHOICES = (
        (QUARTET, 'Quartet Contest'),
        (CHORUS, 'Chorus Contest'),
        (COLLEGIATE, 'Collegiate Contest'),
        (SENIOR, 'Senior Contest'),
    )

    contest_type = models.IntegerField(
        blank=True,
        null=True,
        choices=CONTEST_TYPE_CHOICES,
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
    )

    def __unicode__(self):
        return '{0}'.format(self.get_contest_type_display())

    class Meta:
        ordering = ['contest_type']


class Performance(models.Model):

    QUARTERS = 1
    SEMIS = 2
    FINALS = 3

    CONTEST_ROUND_CHOICES = (
        (QUARTERS, 'Quarter-Finals'),
        (SEMIS, 'Semi-Finals'),
        (FINALS, 'Finals'),
    )

    contest = models.ForeignKey(
        Contest,
        null=True,
        blank=True,
        related_name='performances',
    )

    contestant = models.ForeignKey(
        Contestant,
        null=True,
        blank=True,
        related_name='performances',
    )

    contest_round = models.IntegerField(
        choices=CONTEST_ROUND_CHOICES,
        default=0,
    )

    slug = models.SlugField(
        null=True,
        blank=True,
    )

    appearance = models.IntegerField(
        blank=True,
        null=True,
    )

    song1 = models.CharField(
        blank=True,
        null=True,
        max_length=200,
    )

    mus1 = models.FloatField(
        blank=True,
        null=True,
    )
    prs1 = models.FloatField(
        blank=True,
        null=True,
    )

    sng1 = models.FloatField(
        blank=True,
        null=True,
    )

    song2 = models.CharField(
        blank=True,
        null=True,
        max_length=200,
    )

    mus2 = models.FloatField(
        blank=True,
        null=True,
    )

    prs2 = models.FloatField(
        blank=True,
        null=True,
    )

    sng2 = models.FloatField(
        blank=True,
        null=True,
    )

    men_on_stage = models.IntegerField(
        blank=True,
        null=True,
        default=4,
    )

    @property
    def score1(self):
        if self.sng1 and self.mus1 and self.prs1:
            return round((self.sng1 + self.mus1 + self.prs1) / 3, 1)
        else:
            return None

    @property
    def score2(self):
        if self.sng2 and self.mus2 and self.prs2:
            return round((self.sng2 + self.mus2 + self.prs2) / 3, 1)
        else:
            return None

    def __unicode__(self):
        return '{0}, {1}'.format(
            self.contestant,
            self.get_contest_round_display(),
        )

    class Meta:
        ordering = (
            'contest',
            'contest_round',
            'appearance',
        )
