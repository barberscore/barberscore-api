from __future__ import division

from django.db import models

from django.conf import settings

from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Contestant(models.Model):
    """The name of the contestant"""

    contestant_CHOICES = (
        (1, "Quartet"),
        (2, "Chorus"),
        (3, "Collegiate"),
        (4, "Senior"),
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
    seed = models.IntegerField(blank=True, null=True)
    prelim = models.FloatField(blank=True, null=True)
    contestant_type = models.IntegerField(blank=True, null=True, choices=contestant_CHOICES)
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

    name = models.CharField(default="Contest", max_length=200)
    slug = models.SlugField(null=True)
    year = models.CharField(null=True, blank=True, max_length=4)
    contest_type = models.CharField(null=True, blank=True, max_length=20, choices=CONTEST_TYPE_CHOICES)
    level = models.CharField(max_length=200, blank=True, null=True, choices=LEVEL_CHOICES)

    def __unicode__(self):
        return '{year} {level} {contest_type}'.format(
            year=self.year,
            level=self.level,
            contest_type=self.contest_type)

    class Meta:
        ordering = ['year', 'level', 'contest_type']


class Performance(models.Model):

    ROUND_CHOICES = (
        ('Quarters', 'Quarter-Finals'),
        ('Semis', 'Semi-Finals'),
        ('Finals', 'Finals'),
    )

    contestant = models.ForeignKey(Contestant, blank=True, null=True)
    contest = models.ForeignKey(Contest, blank=True, null=True)
    slug = models.SlugField(blank=True)
    contest_round = models.CharField(max_length=20, blank=True, choices=ROUND_CHOICES)
    slot = models.IntegerField(blank=True, null=True)
    stage_time = models.DateTimeField()

    song_one = models.CharField(default="Song One", max_length=200)
    score_one = models.FloatField(blank=True, null=True)
    mus_one = models.FloatField(blank=True, null=True)
    prs_one = models.FloatField(blank=True, null=True)
    sng_one = models.FloatField(blank=True, null=True)

    song_two = models.CharField(default="Song Two", max_length=200)
    score_two = models.FloatField(blank=True, null=True)
    mus_two = models.FloatField(blank=True, null=True)
    prs_two = models.FloatField(blank=True, null=True)
    sng_two = models.FloatField(blank=True, null=True)
    # rating = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Rating', blank=True, null=True)

    def __unicode__(self):
        return '{contest} {contestant_round}, Slot {slot}: {contestant}'.format(
            contest=self.contest,
            contestant_round=self.contest_round,
            slot=self.slot,
            contestant=self.contestant)

    class Meta:
        ordering = ['contest', 'contest_round', 'slot']



class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    performance = models.ForeignKey(Performance, null=True)
    song_one = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    song_two = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    notes = models.TextField(blank=True)

    # def clean(self):
    # # Don't allow draft entries to have a pub_date.
    #     if self.song_one > 100 or self.song_one < 0:
    #         raise ValidationError('Rating must be between 0-100.')
    #     # Set the pub_date for published items if it hasn't been set already.
    #     if self.song_two > 100 or self.song_one < 0:
    #         raise ValidationError('Rating must be between 0-100.')
