from __future__ import division

from django.core.urlresolvers import reverse
from django.db import models

from timezone_field import TimeZoneField


class Contestant(models.Model):
    """The name of the contestant"""

    CONTESTANT_CHOICES = (
        (1, "Quartet"),
        (2, "Chorus"),
    )

    DISTRICT_CHOICES = (
        (0, 'Unknown'),
        (1, 'CAR'),
        (2, 'CSD'),
        (3, 'DIX'),
        (4, 'EVG'),
        (5, 'FWD'),
        (6, 'ILL'),
        (7, 'JAD'),
        (8, 'LOL'),
        (9, 'MAD'),
        (10, 'NED'),
        (11, 'NSC'),
        (12, 'ONT'),
        (13, 'PIO'),
        (14, 'RMD'),
        (15, 'SLD'),
        (16, 'SUN'),
        (17, 'SWD'),
        (18, 'BABS'),
        (19, 'NZABS'),
        (20, 'SNOBS'),
        (21, 'BHA'),
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    location = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    director = models.CharField(max_length=200, blank=True)
    lead = models.CharField(max_length=200, blank=True)
    tenor = models.CharField(max_length=200, blank=True)
    baritone = models.CharField(max_length=200, blank=True)
    bass = models.CharField(max_length=200, blank=True)
    contestant_type = models.IntegerField(choices=CONTESTANT_CHOICES)
    district = models.IntegerField(choices=DISTRICT_CHOICES, default=0)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('contestant', args=[str(self.slug)])

    class Meta:
        ordering = ['name']


class Contest(models.Model):

    CONTEST_LEVEL_CHOICES = (
        ('International', 'International'),
        ('CAR', 'CAR'),
        ('CSD', 'CSD'),
        ('DIX', 'DIX'),
        ('EVG', 'EVG'),
        ('FWD', 'FWD'),
        ('ILL', 'ILL'),
        ('JAD', 'JAD'),
        ('LOL', 'LOL'),
        ('MAD', 'MAD'),
        ('NED', 'NED'),
        ('NSC', 'NSC'),
        ('ONT', 'ONT'),
        ('PIO', 'PIO'),
        ('RMD', 'RMD'),
        ('SLD', 'SLD'),
        ('SUN', 'SUN'),
        ('SWD', 'SWD'),
    )

    CONTEST_TYPE_CHOICES = (
        ('Quartet', 'Quartet Contest'),
        ('Chorus', 'Chorus Contest'),
        ('Collegiate', 'Collegiate Contest'),
        ('Senior', 'Senior Contest'),
    )

    year = models.CharField(max_length=4)
    contest_level = models.CharField(max_length=20, choices=CONTEST_LEVEL_CHOICES)
    contest_type = models.CharField(max_length=20, choices=CONTEST_TYPE_CHOICES)
    slug = models.SlugField(max_length=200, unique=True)
    time_zone = TimeZoneField(default='US/Eastern')
    panel_size = models.IntegerField(default=5)
    score_sheet = models.FileField(upload_to='bbs', null=True, blank=True)

    def __unicode__(self):
        return '{year} {contest_level} {contest_type}'.format(
            year=self.year,
            contest_level=self.contest_level,
            contest_type=self.contest_type)

    def get_absolute_url(self):
        return reverse('contest', args=[str(self.slug)])

    class Meta:
        ordering = ['year', 'contest_level', 'contest_type']


class Score(models.Model):

    CONTEST_ROUND_CHOICES = (
        ('Quarters', 'Quarter-Finals'),
        ('Semis', 'Semi-Finals'),
        ('Finals', 'Finals'),
    )

    contest = models.ForeignKey(Contest)
    contestant = models.ForeignKey(Contestant)
    contest_round = models.CharField(max_length=20, choices=CONTEST_ROUND_CHOICES)
    slug = models.SlugField(max_length=200, unique=True)

    song1 = models.CharField(max_length=200)
    mus1 = models.IntegerField()
    prs1 = models.IntegerField()
    sng1 = models.IntegerField()

    song2 = models.CharField(max_length=200)
    mus2 = models.IntegerField()
    prs2 = models.IntegerField()
    sng2 = models.IntegerField()

    men_on_stage = models.IntegerField(null=True, default=4)

    def __unicode__(self):
        return '{contest} {contest_round} {contestant}'.format(
            contest=self.contest,
            contest_round=self.contest_round,
            contestant=self.contestant)

    def get_absolute_url(self):
        return reverse('score', args=[str(self.slug)])

    class Meta:
        ordering = ['contest', 'contest_round', 'contestant']
