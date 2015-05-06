from __future__ import division

import logging
log = logging.getLogger(__name__)

import uuid

import csv
import os
import datetime
from django.db import models
from autoslug import AutoSlugField

from django.core.validators import (
    RegexValidator,
)

from django.core.urlresolvers import reverse

from model_utils.managers import InheritanceManager

from timezone_field import TimeZoneField

from phonenumber_field.modelfields import PhoneNumberField

from nameparser import HumanName


def generate_image_filename(instance, filename):
    f, ext = os.path.splitext(filename)
    return '{0}{1}'.format(instance.id, ext)


class Common(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
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

    # def get_absolute_url(self):
    #     return reverse(
    #         'website:singer-detail',
    #         args=[self.slug],
    #     )

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


class Group(Common):
    awards = models.ManyToManyField(
        'Award',
        through='GroupAward',
        related_name='groups',
    )

    district = models.ForeignKey(
        'District',
        help_text="""
            This is the district the group is officially representing in the contest.""",
        blank=True,
        null=True,
        related_name='groups',
    )

    objects = InheritanceManager()

    def __unicode__(self):
        return self.name


class Quartet(Group):
    """An individual quartet."""

    lead = models.ForeignKey(
        'Singer',
        help_text="""Lead""",
        blank=True,
        null=True,
        related_name='quartet_leads',
    )

    tenor = models.ForeignKey(
        'Singer',
        help_text="""Tenor""",
        blank=True,
        null=True,
        related_name='quartet_tenors',
    )

    baritone = models.ForeignKey(
        'Singer',
        help_text="""Baritone""",
        blank=True,
        null=True,
        related_name='quartet_baritones',
    )

    bass = models.ForeignKey(
        'Singer',
        help_text="""Bass""",
        blank=True,
        null=True,
        related_name='quartet_basses',
    )

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return "{0}".format(self.name)

    # def get_absolute_url(self):
    #     return reverse(
    #         'website:quartet-detail',
    #         args=[self.slug],
    #     )


class Chorus(Group):
    """An individual chorus."""
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

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "choruses"

    def __unicode__(self):
        return "{0}".format(self.name)

    # def get_absolute_url(self):
    #     return reverse(
    #         'website:chorus-detail',
    #         args=[self.slug],
    #     )


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
        default=BHS,
    )

    class Meta:
        ordering = [
            'kind',
            'name',
        ]

    def __unicode__(self):
        return "{0}".format(self.name)

    # def get_absolute_url(self):
    #     return reverse(
    #         'website:district-detail',
    #         args=[self.slug],
    #     )


class Convention(models.Model):
    YEAR_CHOICES = []
    for r in range(2000, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))

    SUMMER = 1
    MIDWINTER = 2
    FALL = 3
    SPRING = 4
    PACIFIC = 5

    KIND_CHOICES = (
        (SUMMER, 'Summer',),
        (MIDWINTER, 'Midwinter',),
        (FALL, 'Fall',),
        (SPRING, 'Spring',),
        (PACIFIC, 'Pan-Pacific',),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    district = models.ForeignKey(
        'District',
    )

    kind = models.IntegerField(
        choices=KIND_CHOICES,
        default=SUMMER,
    )

    year = models.IntegerField(
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

        unique_together = (
            ('district', 'kind', 'year',),
        )

    def __unicode__(self):
        return "{0} {1} {2}".format(
            self.district.name,
            self.get_kind_display(),
            self.get_year_display(),
        )

    # def get_absolute_url(self):
    #     return reverse(
    #         'website:convention-detail',
    #         args=[self.slug],
    #     )


class Contest(models.Model):
    YEAR_CHOICES = []
    for r in range(2000, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))

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
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from=lambda instance: "{0}-{1}".format(
            instance.convention,
            instance.get_kind_display(),
        ),
        always_update=True,
        unique=True,
    )

    kind = models.IntegerField(
        choices=KIND_CHOICES,
        default=QUARTET,
    )

    convention = models.ForeignKey(
        'Convention',
        related_name='contests',
    )

    panel = models.IntegerField(
        help_text="""
            Size of the judging panel (typically
            three or five.)""",
        default=5,
    )

    scoresheet_pdf = models.FileField(
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    scoresheet_csv = models.FileField(
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    class Meta:
        unique_together = (
            ('kind', 'convention',),
        )

    def __unicode__(self):
        return "{0} {1}".format(
            self.convention,
            self.get_kind_display(),
        )

    # def get_absolute_url(self):
    #     return reverse(
    #         'website:contest-detail',
    #         args=[self.slug],
    #     )

    def create_group_from_scores(self, name, district_name, chapter_name=None):
        if self.kind == self.CHORUS:
            if name.startswith("The "):
                name = name.split("The ", 1)[1]
            if name.endswith(" Chorus"):
                name = name.split(" Chorus", 1)[0]
            name = name.strip()
            try:
                chorus = Chorus.objects.get(
                    name__icontains=name,
                )
                created = False
            except Chorus.MultipleObjectsReturned as e:
                log.error("Duplicate exists for {0}".format(name))
                raise e
            except Chorus.DoesNotExist:
                try:
                    district = District.objects.get(
                        name=district_name,
                    )
                except District.DoesNotExist as e:
                    # TODO Kludge
                    if district_name == 'AAMBS':
                        district = District.objects.get(name='BHA')
                    else:
                        log.error("No District match for {0}".format(
                            district_name)
                        )
                        district = District.objects.get(name='BHS')

                chorus = Chorus.objects.create(
                    name=name,
                    district=district,
                    chapter_name=chapter_name,
                )
                created = True
            log.info("{0} {1}".format(chorus, created))
            return chorus
        else:
            if name.startswith("The "):
                match = name.split("The ", 1)[1]
            else:
                match = name
            try:
                quartet = Quartet.objects.get(
                    name__endswith=match,
                )
                created = False
            except Quartet.MultipleObjectsReturned as e:
                log.error("Duplicate exists for {0}".format(match))
                raise e
            except Quartet.DoesNotExist:
                try:
                    district = District.objects.get(
                        name=district_name,
                    )
                except District.DoesNotExist as e:
                    # TODO Kludge
                    log.debug(district_name)
                    if district_name == 'AAMBS':
                        district = District.objects.get(name='BHA')
                    else:
                        log.error("No District match for {0}".format(
                            district_name)
                        )
                        district = District.objects.get(name='BHS')

                quartet = Quartet.objects.create(
                    name=name,
                    district=district,
                )
                created = True
            log.info("{0} {1}".format(quartet, created))
            return quartet

    def import_scores(self):
        reader = csv.reader(self.scoresheet_csv)
        data = [row for row in reader]

        performance = {}

        for row in data:
            if not row[4]:
                row[4] = 'BHS'
            performance['contest'] = self
            performance['round'] = row[0]
            performance['place'] = row[1]
            try:
                performance['group'] = self.create_group_from_scores(
                    name=row[2],
                    chapter_name=row[3],
                    district_name=row[4],
                )
            except Exception as e:
                log.error(e)
                raise e

            performance['song1'] = row[5]
            performance['mus1'] = row[6]
            performance['prs1'] = row[7]
            performance['sng1'] = row[8]
            performance['song2'] = row[9]
            performance['mus2'] = row[10]
            performance['prs2'] = row[11]
            performance['sng2'] = row[12]
            try:
                performance['men'] = row[13]
                if not performance['men']:
                    performance['men'] = 4
            except IndexError:
                performance['men'] = 4
            result = Performance.objects.create(**performance)
            log.info("Created performance: {0}".format(result))
        return "Done"


class Contestant(models.Model):
    """Awards and placement"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    contest = models.ForeignKey(
        'Contest',
        related_name='contestants',
    )

    group = models.ForeignKey(
        'Group',
        related_name='contestants',
    )

    seed = models.IntegerField(
        null=True,
        blank=True,
    )

    prelim = models.FloatField(
        null=True,
        blank=True,
    )

    place = models.IntegerField(
        null=True,
        blank=True,
    )

    score = models.FloatField(
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return "{0} {1}".format(
            self.contest,
            self.group,
        )

    class Meta:
        ordering = (
            'contest',
            'group',
            'place',
            'seed',
        )
        unique_together = (
            ('group', 'contest',),
        )


class Performance(models.Model):
    FINALS = 1
    SEMIS = 2
    QUARTERS = 3

    ROUND_CHOICES = (
        (FINALS, 'Finals',),
        (SEMIS, 'Semi-Finals',),
        (QUARTERS, 'Quarter-Finals',),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    contestant = models.ForeignKey(
        'Contestant',
        related_name='performances',
        null=True,
        blank=True,
    )

    round = models.IntegerField(
        choices=ROUND_CHOICES,
        default=FINALS,
    )

    queue = models.IntegerField(
        null=True,
        blank=True,
    )

    session = models.IntegerField(
        choices=(
            (1, 1),
            (2, 2)
        ),
        default=1,
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

    men = models.IntegerField(
        help_text="""
            Men on stage.""",
        blank=True,
        null=True,
        default=4,
    )

    class Meta:
        ordering = [
            'contestant',
            'round',
            'queue',
        ]
        # unique_together = (
        #     ('contestant', 'round', 'queue',),
        # )

    def __unicode__(self):
        return "{0} {1}".format(
            self.contestant,
            self.get_round_display(),
        )

    @property
    def mus1_rata(self):
        try:
            return self.mus1 / self.contestant.contest.panel
        except:
            return None

    @property
    def prs1_rata(self):
        try:
            return self.prs1 / self.contestant.contest.panel
        except:
            return None

    @property
    def sng1_rata(self):
        try:
            return self.sng1 / self.contestant.contest.panel
        except:
            return None

    @property
    def song1_raw(self):
        try:
            return sum([self.mus1, self.prs1, self.sng1])
        except:
            return None

    @property
    def song1_rata(self):
        try:
            return self.song1_raw / (self.contestant.contest.panel * 3)
        except:
            return None

    def mus2_rata(self):
        try:
            return self.mus2 / self.contestant.contest.panel
        except:
            return None

    @property
    def prs2_rata(self):
        try:
            return self.prs2 / self.contestant.contest.panel
        except:
            return None

    @property
    def sng2_rata(self):
        try:
            return self.sng2 / self.contestant.contest.panel
        except:
            return None

    @property
    def song2_raw(self):
        try:
            return sum([self.mus2, self.prs2, self.sng2])
        except:
            return None

    @property
    def song2_rata(self):
        try:
            return self.song2_raw / (self.contestant.contest.panel * 3)
        except:
            return None

    @property
    def total_raw(self):
        try:
            return sum([self.song1_raw, self.song2_raw])
        except:
            return None

    @property
    def total_rata(self):
        try:
            return self.total_raw / (self.contestant.contest.panel * 6)
        except:
            return None


class Award(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
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

    # def get_absolute_url(self):
    #     return reverse(
    #         'website:award-detail',
    #         args=[self.slug],
    #     )


class GroupAward(models.Model):
    """Awards and placement"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    group = models.ForeignKey(
        'Group',
    )

    contest = models.ForeignKey(
        'Contest',
    )

    award = models.ForeignKey(
        'Award',
    )

    def __unicode__(self):
        return "{0} {1} {2}".format(
            self.group,
            self.contest,
            self.award,
        )
