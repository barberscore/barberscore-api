from __future__ import division

import pytz

from django.db import models

from django.conf import settings
from timezone_field import TimeZoneField


class Contestant(models.Model):
    """The name of the contestant"""

    CONTESTANT_CHOICES = (
        (1, "Quartet"),
        (2, "Chorus"),
    )

    DISTRICT_CHOICES = (
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
    slug = models.SlugField(null=True)
    location = models.CharField(blank=True, null=True, max_length=200)
    director = models.CharField(blank=True, null=True, max_length=200)
    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    contestant_type = models.IntegerField(blank=True, null=True, choices=CONTESTANT_CHOICES)
    district = models.IntegerField(blank=True, null=True, choices=DISTRICT_CHOICES)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Singer(models.Model):

    PART_CHOICES = (
        ("Lead", "Lead"),
        ("Tenor", "Tenor"),
        ("Baritone", "Baritone"),
        ("Bass", "Bass"),
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    part = models.CharField(max_length=20, choices=PART_CHOICES)
    contestant = models.ForeignKey(Contestant)

    def __unicode__(self):
        return self.name


class Contest(models.Model):

    CONTEST_TYPE_CHOICES = (
        ('Quartet', 'Quartet Contest'),
        ('Chorus', 'Chorus Contest'),
        ('Collegiate', 'Collegiate Contest'),
        ('Senior', 'Senior Contest'),
    )

    LEVEL_CHOICES = (
        ("INT", "International"),
        ("DIS", "District"),
        ("DIV", "Division"),
    )

    CONTEST_ROUND_CHOICES = (
        ('Quarters', 'Quarter-Finals'),
        ('Semis', 'Semi-Finals'),
        ('Finals', 'Finals'),
    )

    name = models.CharField(default="Contest", max_length=200)
    date = models.DateField(null=True)
    slug = models.SlugField(null=True)
    is_complete = models.BooleanField(default=False)
    year = models.CharField(null=True, blank=True, max_length=4)
    time_zone = TimeZoneField(null=True, blank=True)
    contest_type = models.CharField(null=True, blank=True, max_length=20, choices=CONTEST_TYPE_CHOICES)
    contest_round = models.CharField(null=True, blank=True, max_length=20, choices=CONTEST_ROUND_CHOICES)
    level = models.CharField(max_length=200, blank=True, null=True, choices=LEVEL_CHOICES)
    panel_size = models.IntegerField(null=True)

    def __unicode__(self):
        return '{year} {level} {contest_type} {contest_round}'.format(
            year=self.year,
            level=self.level,
            contest_type=self.contest_type,
            contest_round=self.contest_round)

    class Meta:
        ordering = ['year', 'level', 'contest_type']


class Song(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name


class Performance(models.Model):

    contestant = models.ForeignKey(Contestant, blank=True, null=True)
    contest = models.ForeignKey(Contest, blank=True, null=True)
    slug = models.SlugField(blank=True)
    slot = models.IntegerField(blank=True, null=True)
    place = models.IntegerField(blank=True, null=True)
    seed = models.IntegerField(blank=True, null=True)
    prelim = models.FloatField(blank=True, null=True)
    is_complete = models.BooleanField(default=False)
    is_scratch = models.BooleanField(default=False)
    men_on_stage = models.IntegerField(null=True)
    stage_time = models.DateTimeField()

    song_one = models.ForeignKey(Song, blank=True, null=True, related_name='song_one')
    name_one = models.CharField(max_length=200, blank=True)

    mus_one = models.IntegerField(blank=True, null=True)
    prs_one = models.IntegerField(blank=True, null=True)
    sng_one = models.IntegerField(blank=True, null=True)
    score_one = models.IntegerField(blank=True, null=True)

    avg_mus_one = models.FloatField(blank=True, null=True)
    avg_prs_one = models.FloatField(blank=True, null=True)
    avg_sng_one = models.FloatField(blank=True, null=True)
    avg_score_one = models.FloatField(blank=True, null=True)

    song_two = models.ForeignKey(Song, blank=True, null=True, related_name='song_two')
    name_two = models.CharField(max_length=200, blank=True)

    mus_two = models.IntegerField(blank=True, null=True)
    prs_two = models.IntegerField(blank=True, null=True)
    sng_two = models.IntegerField(blank=True, null=True)
    score_two = models.IntegerField(blank=True, null=True)

    avg_mus_two = models.FloatField(blank=True, null=True)
    avg_prs_two = models.FloatField(blank=True, null=True)
    avg_sng_two = models.FloatField(blank=True, null=True)
    avg_score_two = models.FloatField(blank=True, null=True)

    total_score = models.IntegerField(blank=True, null=True)
    avg_total_score = models.FloatField(blank=True, null=True)

        # def to_user_timezone(date, profile):
        #     timezone = profile.timezone if profile.timezone else settings.TIME_ZONE
        #     return date.replace(tzinfo=pytz.timezone(settings.TIME_ZONE)).astimezone(pytz.timezone(timezone))

    def __unicode__(self):
        return '{contest} Slot {slot}: {contestant}'.format(
            contest=self.contest,
            slot=self.slot,
            contestant=self.contestant)

    class Meta:
        ordering = ['contest', 'slot']
