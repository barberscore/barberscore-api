from __future__ import division

import csv

import logging
log = logging.getLogger(__name__)

import os
import datetime
# import arrow
import uuid
from django_pg import models
from autoslug import AutoSlugField

from django.core.validators import (
    RegexValidator,
)

from django.core.urlresolvers import reverse

from timezone_field import TimeZoneField

from phonenumber_field.modelfields import PhoneNumberField

from nameparser import HumanName


def generate_image_filename(instance, filename):
    f, ext = os.path.splitext(filename)
    return '{0}{1}'.format(instance.id, ext)


class Common(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        coerce_to=str,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the resource.  Must be unique.  If there are singer name conflicts, please add middle initial, nickname, or other identifying information.""",
        max_length=200,
        unique=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
    )

    location = models.CharField(
        help_text="""
            The geographical location of the resource.""",
        max_length=200,
        blank=True,
    )

    website = models.URLField(
        help_text="""
            The website URL of the resource.""",
        blank=True,
    )

    facebook = models.URLField(
        help_text="""
            The facebook URL of the resource.""",
        blank=True,
    )

    twitter = models.CharField(
        help_text="""
            The twitter handle (in form @twitter_handle) of the resource.""",
        blank=True,
        max_length=16,
        validators=[
            RegexValidator(
                regex=r'@([A-Za-z0-9_]+)',
                message="""
                    Must be a single Twitter handle
                    in the form `@twitter_handle`.
                """,
            ),
        ],
    )

    email = models.EmailField(
        help_text="""
            The contact email of the resource.""",
        blank=True,
        null=True,
    )

    phone = PhoneNumberField(
        verbose_name='Phone Number',
        help_text="""
            The phone number of the resource.  Include country code.""",
        blank=True,
        null=True,
    )

    picture = models.ImageField(
        upload_to=generate_image_filename,
        help_text="""
            The picture/logo of the resource.""",
        blank=True,
        null=True,
    )

    description = models.TextField(
        help_text="""
            A description/bio of the resource.  Max 1000 characters.""",
        blank=True,
        max_length=1000,
    )

    notes = models.TextField(
        help_text="""
            Notes (for internal use only).""",
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class Singer(Common):

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return "{0}".format(self.name)

    def get_absolute_url(self):
        return reverse(
            'website:singer-detail',
            args=[self.slug],
        )

    @property
    def first_name(self):
        if self.name:
            name = HumanName(self.name)
            return name.first
        else:
            return None

    @property
    def last_name(self):
        if self.name:
            name = HumanName(self.name)
            return name.last
        else:
            return None


class Quartet(Common):
    """An individual quartet."""
    members = models.ManyToManyField(
        'Singer',
        through='QuartetMember',
        related_name='quartets',
    )

    awards = models.ManyToManyField(
        'Award',
        through='QuartetAward',
        related_name='quartets',
    )

    district = models.ForeignKey(
        'District',
        help_text="""
            This is the district the quartet is officially representing in the contest.""",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return "{0}".format(self.name)

    def get_absolute_url(self):
        return reverse(
            'website:quartet-detail',
            args=[self.slug],
        )


class Chorus(Common):
    """An individual chorus."""
    district = models.ForeignKey(
        'District',
        blank=True,
        null=True,
    )

    director = models.CharField(
        help_text="""
            The name of the director(s) of the chorus.""",
        max_length=200,
        blank=True,
    )

    chapter_name = models.CharField(
        help_text="""
            The name of the director(s) of the chorus.""",
        max_length=200,
        blank=True,
    )

    chapter_code = models.CharField(
        help_text="""
            The code of the director(s) of the chorus.""",
        max_length=200,
        blank=True,
    )

    awards = models.ManyToManyField(
        'Award',
        through='ChorusAward',
        related_name='choruses',
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "choruses"

    def __unicode__(self):
        return "{0}".format(self.name)

    def get_absolute_url(self):
        return reverse(
            'website:chorus-detail',
            args=[self.slug],
        )


class District(Common):
    BHS = 0
    DISTRICT = 1
    AFFILIATE = 2

    KIND_CHOICES = (
        (BHS, "BHS"),
        (DISTRICT, "District"),
        (AFFILIATE, "Affiliate"),
    )

    long_name = models.CharField(
        null=True,
        blank=True,
        max_length=200,
    )

    kind = models.IntegerField(
        choices=KIND_CHOICES,
        default=DISTRICT,
    )

    class Meta:
        ordering = ['kind', 'name']

    def __unicode__(self):
        return "{0}".format(self.name)

    def get_absolute_url(self):
        return reverse(
            'website:district-detail',
            args=[self.slug],
        )


class Convention(models.Model):
    YEAR_CHOICES = []
    for r in range(2010, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))

    SUMMER = 1
    MIDWINTER = 2
    FALL = 3
    SPRING = 4

    KIND_CHOICES = (
        (SUMMER, 'Summer',),
        (MIDWINTER, 'Midwinter',),
        (FALL, 'Fall',),
        (SPRING, 'Spring',),
    )

    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        coerce_to=str,
        editable=False,
    )

    district = models.ForeignKey(
        'District',
        null=True,
        blank=True,
    )

    kind = models.IntegerField(
        choices=KIND_CHOICES,
        default=SUMMER,
    )

    year = models.IntegerField(
        max_length=4,
        choices=YEAR_CHOICES,
        default=datetime.datetime.now().year,
    )

    slug = AutoSlugField(
        populate_from=lambda instance: "{0}-{1}-{2}".format(
            instance.district.name,
            instance.get_kind_display(),
            instance.get_year_display(),
        ),
        always_update=True,
        unique=True,
    )

    dates = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    location = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    timezone = TimeZoneField(
        default='US/Pacific',
    )

    class Meta:
        ordering = [
            'district',
            'kind',
            'year',
        ]

    def __unicode__(self):
        return "{0} {1} {2}".format(
            self.district.name,
            self.get_kind_display(),
            self.get_year_display(),
        )

    def get_absolute_url(self):
        return reverse(
            'website:convention-detail',
            args=[self.slug],
        )


class Contest(models.Model):
    QUARTET = 1
    CHORUS = 2
    SENIOR = 3
    COLLEGIATE = 4

    KIND_CHOICES = (
        (QUARTET, 'Quartet',),
        (CHORUS, 'Chorus',),
        (SENIOR, 'Senior',),
        (COLLEGIATE, 'Collegiate',),
    )

    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        coerce_to=str,
        editable=False,
    )

    kind = models.IntegerField(
        choices=KIND_CHOICES,
        default=QUARTET,
    )

    convention = models.ForeignKey(
        'Convention',
        null=True,
        blank=True,
    )

    slug = AutoSlugField(
        populate_from=lambda instance: "{0}-{1}-{2}".format(
            instance.convention.district.name,
            instance.get_kind_display(),
            instance.convention.year,
        ),
        always_update=True,
        unique=True,
        null=True,
        blank=True,
    )

    panel = models.IntegerField(
        help_text="""
            Size of the judging panel (typically
            three or five.)""",
        default=5,
    )

    scoresheet = models.FileField(
        blank=True,
        null=True,
    )

    scoresheet_csv = models.FileField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = [
            'convention__district',
            'kind',
            'convention__year',
        ]

    def __unicode__(self):
        return "{0} {1} {2}".format(
            self.convention.district.name,
            self.get_kind_display(),
            self.convention.year,
        )

    def get_absolute_url(self):
        return reverse(
            'website:contest-detail',
            args=[self.slug],
        )

    def parse_scores(self):
        raw = [row for row in csv.reader(
            self.scoresheet_csv.read().splitlines()
        )]
        l = len(raw)
        data = []
        i = 0
        #  Deinterlace and build list of dictionaries.
        while i < l:
            if (i % 2 == 0):  # zero-indexed rows
                row = raw[i]
                row.extend(raw[i + 1])
                data.append(row)
            else:  # Skip interlaced row; added supra
                pass
            i += 1

        if self.kind == self.CHORUS:
            for row in data:
                chorus, created = Chorus.objects.get_or_create(
                    name=row[8].split('(', 1)[0].strip(),
                )
                if created:
                    dis_name = row[8].split('[', 1)[1].split(']', 1)[0].strip().replace('[', '').replace(']', '')
                    log.debug(dis_name)
                    chorus.district = District.objects.get(
                        name=dis_name,
                    )
                    chorus.chapter_name = row[0].split(' ', 1)[1].strip()

                    chorus.save()
                    log.debug(chorus)
        else:
            # Create contestant objects first (if needed)
            for row in data:

                quartet, created = Quartet.objects.get_or_create(
                    name=row[0].split(' ', 1)[1].strip(),
                )
                if created:
                    quartet.district = District.objects.get(name=row[7].strip().replace('[', '').replace(']', ''))
                    quartet.save()
                    log.debug(quartet)

        performance = {}

        for row in data:
            performance['contest'] = self
            performance['place'] = row[0].split(' ', 1)[0]
            performance['song1'] = row[1].strip()
            performance['mus1'] = row[2].strip()
            performance['prs1'] = row[3].strip()
            performance['sng1'] = row[4].strip()

            if self.kind == self.CHORUS:
                performance['chorus'] = Chorus.objects.get(
                    name=row[8].split('(', 1)[0].strip(),
                )
                performance['men'] = row[7].strip()
                performance['song2'] = row[9].strip()
                performance['mus2'] = row[10].strip()
                performance['prs2'] = row[11].strip()
                performance['sng2'] = row[12].strip()
                ChorusPerformance.objects.create(**performance)
            else:
                performance['quartet'] = Quartet.objects.get(
                    name=row[0].split(' ', 1)[1].strip(),
                )
                performance['song2'] = row[8].strip()
                performance['mus2'] = row[9].strip()
                performance['prs2'] = row[10].strip()
                performance['sng2'] = row[11].strip()
                QuartetPerformance.objects.create(**performance)
        return "Done"


class Performance(models.Model):
    FINALS = 1
    SEMIS = 2
    QUARTERS = 3

    ROUND_CHOICES = (
        (FINALS, 'Finals',),
        (SEMIS, 'Semi-Finals',),
        (QUARTERS, 'Quarter-Finals',),
    )

    contest = models.ForeignKey(Contest)

    queue = models.IntegerField(
        null=True,
        blank=True,
    )

    stagetime = models.DateTimeField(
        help_text="""
            The title of the first song of the performance.""",
        blank=True,
        null=True,
    )

    place = models.IntegerField(
        null=True,
        blank=True,
    )

    song1 = models.CharField(
        help_text="""
            The title of the first song of the performance.""",
        blank=True,
        max_length=200,
    )

    mus1 = models.IntegerField(
        help_text="""
            The raw music score of the first song.""",
        blank=True,
        null=True,
    )

    prs1 = models.IntegerField(
        help_text="""
            The raw presentation score of the first song.""",
        blank=True,
        null=True,
    )

    sng1 = models.IntegerField(
        help_text="""
            The raw singing score of the first song.""",
        blank=True,
        null=True,
    )

    song2 = models.CharField(
        help_text="""
            The title of the second song of the performance.""",
        blank=True,
        max_length=200,
    )

    mus2 = models.IntegerField(
        help_text="""
            The raw music score of the second song.""",
        blank=True,
        null=True,
    )

    prs2 = models.IntegerField(
        help_text="""
            The raw presentation score of the second song.""",
        blank=True,
        null=True,
    )

    sng2 = models.IntegerField(
        help_text="""
            The raw singing score of the second song.""",
        blank=True,
        null=True,
    )

    @property
    def mus1_rata(self):
        if self.mus1:
            return self.mus1 / self.contest.panel
        else:
            return None

    @property
    def prs1_rata(self):
        if self.mus1:
            return self.prs1 / self.contest.panel
        else:
            return None

    @property
    def sng1_rata(self):
        if self.mus1:
            return self.sng1 / self.contest.panel
        else:
            return None

    def mus2_rata(self):
        if self.mus1:
            return self.mus2 / self.contest.panel
        else:
            return None

    @property
    def prs2_rata(self):
        if self.mus1:
            return self.prs2 / self.contest.panel
        else:
            return None

    @property
    def sng2_rata(self):
        if self.mus1:
            return self.sng2 / self.contest.panel
        else:
            return None

    @property
    def song1_raw(self):
        if self.mus1 and self.prs1 and self.sng1:
            return sum([self.mus1, self.prs1, self.sng1])
        else:
            return None

    @property
    def song2_raw(self):
        if self.mus2 and self.prs2 and self.sng2:
            return sum([self.mus2, self.prs2, self.sng2])
        else:
            return None

    @property
    def total_raw(self):
        if self.song1_raw and self.song2_raw:
            return sum([self.song1_raw, self.song2_raw])
        else:
            return None

    @property
    def song1_rata(self):
        if self.song1_raw:
            return self.song1_raw / (self.contest.panel * 3)
        else:
            return None

    @property
    def song2_rata(self):
        if self.song2_raw:
            return self.song2_raw / (self.contest.panel * 3)
        else:
            return None

    @property
    def total_percent(self):
        if self.song1_raw:
            return self.total_raw / (self.contest.panel * 6)
        else:
            return None

    class Meta:
        abstract = True


class QuartetPerformance(Performance):
    quartet = models.ForeignKey(Quartet)

    round = models.IntegerField(
        choices=Performance.ROUND_CHOICES,
        default=Performance.QUARTERS,
    )

    class Meta:
        ordering = [
            'contest',
            '-round',
            'quartet',
        ]

    def __unicode__(self):
        return "{0} {1} {2}".format(
            self.contest,
            self.get_round_display(),
            self.quartet,
        )


class ChorusPerformance(Performance):
    chorus = models.ForeignKey(Chorus)

    round = models.IntegerField(
        choices=Performance.ROUND_CHOICES,
        default=Performance.FINALS,
    )

    men = models.IntegerField(
        help_text="""
            The number of men on stage.""",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = [
            'contest',
            'round',
            'chorus',
        ]

    def __unicode__(self):
        return "{0} {1} {2}".format(
            self.contest,
            self.get_round_display(),
            self.chorus,
        )


class QuartetMember(models.Model):
    LEAD = 1
    TENOR = 2
    BARITONE = 3
    BASS = 4

    PART_CHOICES = (
        (LEAD, 'Lead'),
        (TENOR, 'Tenor'),
        (BARITONE, 'Baritone'),
        (BASS, 'Bass'),
    )

    singer = models.ForeignKey(Singer)
    quartet = models.ForeignKey(Quartet)
    contest = models.ForeignKey(Contest)
    part = models.IntegerField(
        choices=PART_CHOICES,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = [
            'quartet',
            'part',
            'singer',
            'contest',
        ]

    def __unicode__(self):
        return "{0} {1} {2} {3}".format(
            self.quartet,
            self.get_part_display(),
            self.singer,
            self.contest,
        )


class Award(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        coerce_to=str,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the award.  Must be unique.""",
        max_length=200,
        unique=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
    )

    description = models.CharField(
        null=True,
        blank=True,
        max_length=200,
    )

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return "{0}".format(self.name)

    def get_absolute_url(self):
        return reverse(
            'website:award-detail',
            args=[self.slug],
        )


class QuartetAward(models.Model):
    """Awards and placement"""
    quartet = models.ForeignKey(Quartet)
    contest = models.ForeignKey(Contest)
    award = models.ForeignKey(Award)


class ChorusAward(models.Model):
    """Awards and placement"""
    chorus = models.ForeignKey(Chorus)
    contest = models.ForeignKey(Contest)
    award = models.ForeignKey(Award)


class Finish(models.Model):
    """Awards and placement"""
    RANK_CHOICES = []
    for r in range(1, 50):
        RANK_CHOICES.append((r, r))

    contest = models.ForeignKey(
        Contest,
        null=True,
        blank=True,
    )

    place = models.IntegerField(
        choices=RANK_CHOICES,
        null=True,
        blank=True,
    )
    prelim = models.FloatField(
        null=True,
        blank=True,
    )
    seed = models.IntegerField(
        choices=RANK_CHOICES,
        null=True,
        blank=True,
    )

    score = models.FloatField(
        null=True,
        blank=True,
    )


class ChorusFinish(Finish):
    chorus = models.ForeignKey(
        Chorus,
        related_name='finishes',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Chorus Finishes"


class QuartetFinish(Finish):
    quartet = models.ForeignKey(
        Quartet,
        related_name='finishes',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Quartet Finishes"
