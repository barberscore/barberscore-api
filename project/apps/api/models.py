from __future__ import division

import logging
log = logging.getLogger(__name__)

import uuid

# import csv
import os
import datetime
from django.db import models

from django.conf import settings
from autoslug import AutoSlugField

from django.core.validators import (
    RegexValidator,
)

from django.core.exceptions import (
    ValidationError,
)

# from django.core.urlresolvers import reverse

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
        return self.name

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

    QUARTET = 1
    CHORUS = 2

    KIND_CHOICES = (
        (QUARTET, "Quartet"),
        (CHORUS, "Chorus"),
    )

    awards = models.ManyToManyField(
        'Award',
        through='GroupAward',
        related_name='groups',
    )

    district = models.ForeignKey(
        'District',
        null=True,
        blank=True,
    )

    kind = models.IntegerField(
        choices=KIND_CHOICES,
        default=QUARTET,
    )

    lead = models.ForeignKey(
        'Singer',
        help_text="""Lead""",
        blank=True,
        null=True,
        related_name='lead_groups',
    )

    tenor = models.ForeignKey(
        'Singer',
        help_text="""Tenor""",
        blank=True,
        null=True,
        related_name='tenor_groups',
    )

    baritone = models.ForeignKey(
        'Singer',
        help_text="""Baritone""",
        blank=True,
        null=True,
        related_name='baritone_groups',
    )

    bass = models.ForeignKey(
        'Singer',
        help_text="""Bass""",
        blank=True,
        null=True,
        related_name='bass_groups',
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

    bsmdb_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return self.name

    @property
    def bsmdb(self):
        if self.bsmdb_id:
            if self.kind == self.CHORUS:
                return 'http://www.bsmdb.com/Chorus.php?ChorusID={0}'.format(
                    self.bsmdb_id,
                )
            else:
                return 'http://www.bsmdb.com/Quartet.php?QuartetID={0}'.format(
                    self.bsmdb_id,
                )
        else:
            return None

    class Meta:
        ordering = (
            'name',
        )


class District(Common):
    BHS = 0
    CAR = 1
    CSD = 2
    DIX = 3
    EVG = 4
    FWD = 5
    ILL = 6
    JAD = 7
    LOL = 8
    MAD = 9
    NED = 10
    NSC = 11
    ONT = 12
    PIO = 13
    RMD = 14
    SLD = 15
    SUN = 16
    SWD = 17
    BABS = 18
    BHA = 19
    BHNZ = 20
    BING = 21
    DABS = 22
    FABS = 23
    IABS = 24
    NZABS = 25
    SABS = 26
    SNOBS = 27
    SPATS = 28

    DISTRICT_CHOICES = (
        (BHS, "BHS"),
        (CAR, "CAR"),
        (CSD, "CSD"),
        (DIX, "DIX"),
        (EVG, "EVG"),
        (FWD, "FWD"),
        (ILL, "ILL"),
        (JAD, "JAD"),
        (LOL, "LOL"),
        (MAD, "MAD"),
        (NED, "NED"),
        (NSC, "NSC"),
        (ONT, "ONT"),
        (PIO, "PIO"),
        (RMD, "RMD"),
        (SLD, "SLD"),
        (SUN, "SUN"),
        (SWD, "SWD"),
        (BABS, "BABS"),
        (BHA, "BHA"),
        (BHNZ, "BHNZ"),
        (BING, "BING"),
        (DABS, "DABS"),
        (FABS, "FABS"),
        (IABS, "IABS"),
        (NZABS, "NZABS"),
        (SABS, "SABS"),
        (SNOBS, "SNOBS"),
        (SPATS, "SPATS"),
    )

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

    abbr = models.IntegerField(
        null=True,
        blank=True,
        choices=DISTRICT_CHOICES,
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
        return self.name


class Convention(models.Model):
    YEAR_CHOICES = []
    for r in range(1994, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))

    INTERNATIONAL = 1
    MIDWINTER = 2
    FALL = 3
    SPRING = 4
    PACIFIC = 5

    KIND_CHOICES = (
        (INTERNATIONAL, 'International',),
        (MIDWINTER, 'Midwinter',),
        (FALL, 'Fall',),
        (SPRING, 'Spring',),
        (PACIFIC, 'Pacific',),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the convention.""",
        max_length=200,
        unique=True,
    )

    kind = models.IntegerField(
        choices=KIND_CHOICES,
        null=True,
        blank=True,
    )

    year = models.IntegerField(
        choices=YEAR_CHOICES,
        default=datetime.datetime.now().year,
        null=True,
        blank=True,
    )

    district = models.ForeignKey(
        'District',
        null=True,
        blank=True,
    )

    slug = AutoSlugField(
        populate_from='name',
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

    is_active = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = [
            'district',
            '-year',
        ]

        unique_together = (
            ('district', 'kind', 'year',),
        )

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.kind in [
            self.INTERNATIONAL,
            self.MIDWINTER,
            self.PACIFIC,
        ]:
            self.name = "{0} {1}".format(
                self.get_kind_display(),
                self.get_year_display(),
            )
        else:
            self.name = "{0} {1} {2}".format(
                self.district,
                self.get_kind_display(),
                self.get_year_display(),
            )
        super(Convention, self).save(*args, **kwargs)


class Contest(models.Model):

    YEAR_CHOICES = []
    for r in range(1994, (datetime.datetime.now().year + 1)):
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

    INTERNATIONAL = 1
    DISTRICT = 2
    REGIONAL = 3
    PRELIMS = 4

    LEVEL_CHOICES = (
        (INTERNATIONAL, "International"),
        (DISTRICT, "District"),
        (REGIONAL, "Regional"),
        (PRELIMS, "Prelims"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
    )

    name = models.CharField(
        max_length=200,
        unique=True,
    )

    level = models.IntegerField(
        choices=LEVEL_CHOICES,
        default=INTERNATIONAL,
    )

    kind = models.IntegerField(
        choices=KIND_CHOICES,
        default=QUARTET,
    )

    year = models.IntegerField(
        choices=YEAR_CHOICES,
        default=datetime.datetime.now().year,
    )

    district = models.ForeignKey(
        'District',
        null=True,
        blank=True,
    )

    convention = models.ForeignKey(
        'Convention',
        related_name='contests',
        null=True,
        blank=True,
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

    is_active = models.BooleanField(
        default=False,
    )

    class Meta:
        # unique_together = (
        #     ('kind', 'convention',),
        # )
        ordering = (
            'level',
            'kind',
            '-year',
            # 'district',
        )

    def clean(self):
            if self.level == self.INTERNATIONAL and self.district is not None:
                raise ValidationError('International does not have a district.')
            if self.level != self.INTERNATIONAL and self.district is None:
                raise ValidationError('You must provide a district.')
            if self.year != self.convention.year:
                raise ValidationError("The contest should be the same year as the convention.")

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.level == self.INTERNATIONAL:
            self.name = "{0} {1} {2}".format(
                self.get_level_display(),
                self.get_kind_display(),
                self.get_year_display(),
            )
        elif self.level == self.PRELIMS:
            self.name = "{0} {1} {2}".format(
                self.district,
                self.get_level_display(),
                self.get_year_display(),
            )
        else:
            self.name = "{0} {1} {2}".format(
                self.district,
                self.get_kind_display(),
                self.get_year_display(),
            )
        super(Contest, self).save(*args, **kwargs)

    # def create_group_from_scores(self, name, district_name, chapter_name=None):
    #     if self.kind == self.CHORUS:
    #         if name.startswith("The "):
    #             name = name.split("The ", 1)[1]
    #         if name.endswith(" Chorus"):
    #             name = name.split(" Chorus", 1)[0]
    #         name = name.strip()
    #         try:
    #             chorus = Chorus.objects.get(
    #                 name__icontains=name,
    #             )
    #             created = False
    #         except Chorus.MultipleObjectsReturned as e:
    #             log.error("Duplicate exists for {0}".format(name))
    #             raise e
    #         except Chorus.DoesNotExist:
    #             try:
    #                 district = District.objects.get(
    #                     name=district_name,
    #                 )
    #             except District.DoesNotExist as e:
    #                 # TODO Kludge
    #                 if district_name == 'AAMBS':
    #                     district = District.objects.get(name='BHA')
    #                 else:
    #                     log.error("No District match for {0}".format(
    #                         district_name)
    #                     )
    #                     district = District.objects.get(name='BHS')

    #             chorus = Chorus.objects.create(
    #                 name=name,
    #                 district=district,
    #                 chapter_name=chapter_name,
    #             )
    #             created = True
    #         log.info("{0} {1}".format(chorus, created))
    #         return chorus
    #     else:
    #         if name.startswith("The "):
    #             match = name.split("The ", 1)[1]
    #         else:
    #             match = name
    #         try:
    #             quartet = Quartet.objects.get(
    #                 name__endswith=match,
    #             )
    #             created = False
    #         except Quartet.MultipleObjectsReturned as e:
    #             log.error("Duplicate exists for {0}".format(match))
    #             raise e
    #         except Quartet.DoesNotExist:
    #             try:
    #                 district = District.objects.get(
    #                     name=district_name,
    #                 )
    #             except District.DoesNotExist as e:
    #                 # TODO Kludge
    #                 log.debug(district_name)
    #                 if district_name == 'AAMBS':
    #                     district = District.objects.get(name='BHA')
    #                 else:
    #                     log.error("No District match for {0}".format(
    #                         district_name)
    #                     )
    #                     district = District.objects.get(name='BHS')

    #             quartet = Quartet.objects.create(
    #                 name=name,
    #                 district=district,
    #             )
    #             created = True
    #         log.info("{0} {1}".format(quartet, created))
    #         return quartet

    # def import_scores(self):
    #     reader = csv.reader(self.scoresheet_csv)
    #     data = [row for row in reader]

    #     performance = {}

    #     for row in data:
    #         if not row[4]:
    #             row[4] = 'BHS'
    #         performance['contest'] = self
    #         performance['round'] = row[0]
    #         performance['place'] = row[1]
    #         try:
    #             performance['group'] = self.create_group_from_scores(
    #                 name=row[2],
    #                 chapter_name=row[3],
    #                 district_name=row[4],
    #             )
    #         except Exception as e:
    #             log.error(e)
    #             raise e

    #         performance['song1'] = row[5]
    #         performance['mus1'] = row[6]
    #         performance['prs1'] = row[7]
    #         performance['sng1'] = row[8]
    #         performance['song2'] = row[9]
    #         performance['mus2'] = row[10]
    #         performance['prs2'] = row[11]
    #         performance['sng2'] = row[12]
    #         try:
    #             performance['men'] = row[13]
    #             if not performance['men']:
    #                 performance['men'] = 4
    #         except IndexError:
    #             performance['men'] = 4
    #         result = Performance.objects.create(**performance)
    #         log.info("Created performance: {0}".format(result))
    #     return "Done"


class Contestant(models.Model):
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

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
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

    stagetime = models.DateTimeField(
        null=True,
        blank=True,
    )

    queue = models.IntegerField(
        null=True,
        blank=True,
    )

    quarters_place = models.IntegerField(
        null=True,
        blank=True,
    )

    quarters_score = models.FloatField(
        null=True,
        blank=True,
    )

    semis_place = models.IntegerField(
        null=True,
        blank=True,
    )

    semis_score = models.FloatField(
        null=True,
        blank=True,
    )

    finals_place = models.IntegerField(
        null=True,
        blank=True,
    )

    finals_score = models.FloatField(
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        self.name = "{0} {1}".format(
            self.contest,
            self.group,
        )
        try:
            self.stagetime = self.performances.latest(
                'stagetime'
            ).stagetime
        except Performance.DoesNotExist:
            self.stagetime = None
        try:
            self.queue = self.performances.latest(
                'stagetime'
            ).queue
        except Performance.DoesNotExist:
            self.queue = None
        try:
            self.quarters_place = self.performances.get(round=3).place
        except Performance.DoesNotExist:
            self.quarters_place = None
        try:
            self.quarters_score = self.performances.get(round=3).score
        except Performance.DoesNotExist:
            self.quarters_score = None
        try:
            self.semis_place = self.performances.get(round=2).place
        except Performance.DoesNotExist:
            self.semis_place = None
        try:
            self.semis_score = self.performances.get(round=2).score
        except Performance.DoesNotExist:
            self.semis_score = None
        try:
            self.finals_place = self.performances.get(round=1).place
        except Performance.DoesNotExist:
            self.finals_place = None
        try:
            self.finals_score = self.performances.get(round=1).score
        except Performance.DoesNotExist:
            self.finals_score = None
        super(Contestant, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = (
            '-contest',
            'place',
            '-score',
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
        (SEMIS, 'Semis',),
        (QUARTERS, 'Quarters',),
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

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
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

    mus1_rata = models.FloatField(
        blank=True,
        null=True,
        editable=False,
    )

    prs1_rata = models.FloatField(
        blank=True,
        null=True,
        editable=False,
    )

    sng1_rata = models.FloatField(
        blank=True,
        null=True,
        editable=False,
    )

    song1_rata = models.FloatField(
        blank=True,
        null=True,
        editable=False,
    )

    mus2_rata = models.FloatField(
        blank=True,
        null=True,
        editable=False,
    )

    prs2_rata = models.FloatField(
        blank=True,
        null=True,
        editable=False,
    )

    sng2_rata = models.FloatField(
        blank=True,
        null=True,
        editable=False,
    )

    song2_rata = models.FloatField(
        blank=True,
        null=True,
        editable=False,
    )

    score = models.FloatField(
        blank=True,
        null=True,
        editable=False,
    )

    song1_raw = models.IntegerField(
        blank=True,
        null=True,
        editable=False,
    )

    song2_raw = models.IntegerField(
        blank=True,
        null=True,
        editable=False,
    )

    total_raw = models.IntegerField(
        blank=True,
        null=True,
        editable=False,
    )

    # @property
    # def day(self):
    #     return self.stagetime.strftime("%A")

    class Meta:
        ordering = [
            'contestant',
            'round',
            'queue',
            'stagetime',
        ]
        unique_together = (
            ('contestant', 'round',),
        )

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.contestant.contest == Contest.CHORUS:
            self.name = "{0}".format(
                self.contestant,
            )
        else:
            self.name = "{0} {1}".format(
                self.contestant,
                self.get_round_display(),
            )
        if (
            self.mus1 and
            self.prs1 and
            self.sng1 and
            self.mus2 and
            self.prs2 and
            self.sng2
        ):
            try:
                panel = self.contestant.contest.panel
                self.song1_raw = sum([
                    self.mus1,
                    self.prs1,
                    self.sng1,
                ])
                self.song2_raw = sum([
                    self.mus2,
                    self.prs2,
                    self.sng2,
                ])
                self.total_raw = sum([
                    self.song1_raw,
                    self.song2_raw,
                ])
                self.mus1_rata = round(self.mus1 / panel, 1)
                self.prs1_rata = round(self.prs1 / panel, 1)
                self.sng1_rata = round(self.sng1 / panel, 1)
                self.song1_rata = round(self.song1_raw / (panel * 3), 1)
                self.mus2_rata = round(self.mus2 / panel, 1)
                self.prs2_rata = round(self.prs2 / panel, 1)
                self.sng2_rata = round(self.sng2 / panel, 1)
                self.song2_rata = round(self.song2_raw / (panel * 3), 1)
                self.score = round(self.total_raw / (panel * 6), 1)
            except TypeError:
                log.error("Check scores for performance {0}".format(self))

        super(Performance, self).save(*args, **kwargs)


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
        return self.name

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
        return self.name


class Note(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    performance = models.ForeignKey(
        'Performance',
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='notes',
    )

    text = models.TextField(
    )

    def __unicode__(self):
        return self.id

    class Meta:
        unique_together = (
            ('performance', 'user'),
        )
