import os
import datetime
# import arrow
import uuid
from django_pg import models
from autoslug import AutoSlugField

from django.core.validators import (
    RegexValidator,
)

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
            The name of the resource.""",
        max_length=200,
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
            The phone number of the resource.""",
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

    blurb = models.TextField(
        help_text="""
            A description/bio describing the resource.  Max 1000 characters.""",
        blank=True,
        max_length=1000,
    )

    notes = models.TextField(
        help_text="""
            Notes (for internal use only).""",
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return "{0}".format(self.name)

    class Meta:
        abstract = True
        ordering = ('name',)


class Singer(Common):
    timezone = TimeZoneField(
        default='US/Pacific',
    )

    chapter = models.ForeignKey(
        'Chapter',
        help_text="""
            The chapter of the singer.""",
        blank=True,
        null=True,
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
    prelim = models.FloatField(
        help_text="""
            The incoming prelim score.""",
        null=True,
        blank=True,
    )

    rank = models.IntegerField(
        help_text="""
            The incoming rank (based on prelim).""",
        null=True,
        blank=True,
    )

    members = models.ManyToManyField(
        'Singer',
        through='QuartetMember',
    )

    lead = models.ForeignKey(
        'Singer',
        blank=True,
        null=True,
        related_name='quartet_lead',
    )

    tenor = models.ForeignKey(
        'Singer',
        blank=True,
        null=True,
        related_name='quartet_tenor',
    )

    baritone = models.ForeignKey(
        'Singer',
        blank=True,
        null=True,
        related_name='quartet_baritone',
    )

    bass = models.ForeignKey(
        'Singer',
        blank=True,
        null=True,
        related_name='quartet_bass',
    )


class Chorus(Common):
    """An individual singer."""
    prelim = models.FloatField(
        help_text="""
            The incoming prelim score.""",
        null=True,
        blank=True,
    )

    rank = models.IntegerField(
        help_text="""
            The incoming rank (based on prelim).""",
        null=True,
        blank=True,
    )

    chapter = models.OneToOneField(
        'Chapter',
        null=True,
        blank=True,
    )

    director = models.CharField(
        help_text="""
            The name of the director(s) of the chorus.""",
        max_length=200,
        blank=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "choruses"


class Chapter(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        coerce_to=str,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the resource.""",
        max_length=200,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
    )

    code = models.CharField(
        help_text="""
            The Chapter code""",
        blank=True,
        null=True,
        max_length=20,
    )

    district = models.ForeignKey(
        'District',
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return "{0}".format(self.name)


class District(Common):
    DISTRICT = 1
    AFFILIATE = 2

    KIND_CHOICES = (
        (DISTRICT, "District"),
        (AFFILIATE, "Affiliate"),
    )

    abbreviation = models.CharField(
        null=True,
        blank=True,
        max_length=20,
    )

    kind = models.IntegerField(
        choices=KIND_CHOICES,
        default=1,
    )

    class Meta:
        ordering = ['kind', 'name']


class Convention(models.Model):
    YEAR_CHOICES = []
    for r in range(2010, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))

    INTERNATIONAL = 1
    # DISTRICT = 2

    SUMMER = 1
    # MIDWINTER = 2
    # FALL = 3
    # SPRING = 4

    LEVEL_CHOICES = (
        (INTERNATIONAL, 'International',),
        # (DISTRICT, 'District',)
    )

    KIND_CHOICES = (
        (SUMMER, 'Summer',),
        # (MIDWINTER, 'Midwinter',)
    )

    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        coerce_to=str,
        editable=False,
    )

    year = models.IntegerField(
        max_length=4,
        choices=YEAR_CHOICES,
        default=datetime.datetime.now().year,
    )

    level = models.IntegerField(
        choices=LEVEL_CHOICES,
        default=INTERNATIONAL,
    )

    kind = models.IntegerField(
        choices=KIND_CHOICES,
        default=SUMMER,
    )

    slug = AutoSlugField(
        populate_from=lambda instance: "{0}-{1}".format(instance.get_year_display(), instance.get_level_display()),
        always_update=True,
        # unique=True,
        null=True,
        blank=True,
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

    def __unicode__(self):
        return "{0} {1} {2}".format(
            self.get_year_display(),
            self.get_level_display(),
            self.get_kind_display(),
        )

    class Meta:
        ordering = ['-year', 'level', 'kind']


class Contest(models.Model):
    YEAR_CHOICES = []
    for r in range(2010, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))

    INTERNATIONAL = 1
    # DISTRICT = 2

    LEVEL_CHOICES = (
        (INTERNATIONAL, 'International',),
        # (DISTRICT, 'District',)
    )

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

    year = models.IntegerField(
        max_length=4,
        choices=YEAR_CHOICES,
        default=datetime.datetime.now().year,
    )

    level = models.IntegerField(
        choices=LEVEL_CHOICES,
        default=INTERNATIONAL,
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

    district = models.ForeignKey(
        'District',
        null=True,
        blank=True,
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

    def __unicode__(self):
        return "{0} {1} {2}".format(
            self.get_year_display(),
            self.get_level_display(),
            self.get_kind_display(),
        )

    class Meta:
        ordering = ['-year', 'level', 'kind']


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

    class Meta:
        abstract = True
        ordering = ['contest', 'round', 'queue']


class QuartetPerformance(Performance):
    quartet = models.ForeignKey(Quartet)

    round = models.IntegerField(
        choices=Performance.ROUND_CHOICES,
        default=Performance.QUARTERS,
    )

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

    def __unicode__(self):
        return "{0} {1}".format(
            self.contest,
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
