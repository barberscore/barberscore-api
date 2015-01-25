import datetime
import uuid
from django_pg import models

from autoslug import AutoSlugField

from django.core.urlresolvers import reverse

from django.core.validators import (
    RegexValidator,
)

from timezone_field import TimeZoneField

from phonenumber_field.modelfields import PhoneNumberField

from nameparser import HumanName


class Singer(models.Model):
    """An individual singer."""
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        coerce_to=str,
        editable=False,
    )

    name = models.CharField(
        verbose_name="Full Name",
        help_text="""
            The Full Name of the Singer.""",
        max_length=100,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
    )

    phone = PhoneNumberField(
        verbose_name='mobile number',
        help_text="""
            The phone of the Singer.""",
        blank=True,
        null=True,
    )

    email = models.EmailField(
        verbose_name="Email Address",
        help_text="""
            The Email Address of the singer.""",
        blank=True,
        null=True,
    )

    bio = models.TextField(
        help_text="""
            A quick biography of the singer.""",
        null=True,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

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

    def __unicode__(self):
        if self.name:
            return "{0}".format(self.name)
        else:
            return self.id

    def get_absolute_url(self):
        return reverse('singer', args=[str(self.slug)])


class Quartet(models.Model):
    """An individual quartet."""
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        coerce_to=str,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the quartet.""",
        max_length=200,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
    )

    location = models.CharField(
        help_text="""
            The geographical location of the quartet.""",
        max_length=200,
        blank=True,
    )

    website = models.URLField(
        help_text="""
            The website URL of the quartet.""",
        blank=True,
    )

    facebook = models.URLField(
        help_text="""
            The facebook URL of the quartet.""",
        blank=True,
    )

    twitter = models.CharField(
        help_text="""
            The twitter handle (in form @twitter_handle) of the quartet.""",
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
            The contact email of the quartet.""",
        blank=True,
    )

    phone = PhoneNumberField(
        verbose_name='mobile number',
        help_text="""
            The contact number of the quartet.""",
        blank=True,
        null=True,
    )

    picture = models.ImageField(
        help_text="""
            The 'official' picture of the contestant.""",
        blank=True,
        null=True,
    )

    blurb = models.TextField(
        help_text="""
            A blurb describing the contestant.  Max 1000 characters.""",
        blank=True,
        max_length=1000,
    )

    district = models.ForeignKey(
        'District',
        help_text="""
            The district the quartet is representing.""",
        blank=True,
        null=True,
    )

    members = models.ManyToManyField(
        'Singer',
        through='QuartetMembership',
        null=True,
        blank=True,
    )

    @property
    def lead(self):
        lead = self.members.filter(
            quartetmembership__part=QuartetMembership.LEAD,
        ).last()
        return lead

    @property
    def tenor(self):
        tenor = self.members.filter(
            quartetmembership__part=QuartetMembership.TENOR,
        ).last()
        return tenor

    @property
    def baritone(self):
        baritone = self.members.filter(
            quartetmembership__part=QuartetMembership.BARITONE,
        ).last()
        return baritone

    @property
    def bass(self):
        bass = self.members.filter(
            quartetmembership__part=QuartetMembership.BASS,
        ).last()
        return bass

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('quartet', args=[str(self.slug)])

    class Meta:
        ordering = ['name']


class Collegiate(models.Model):
    """An individual quartet."""
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        coerce_to=str,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the quartet.""",
        max_length=200,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
    )

    location = models.CharField(
        help_text="""
            The geographical location of the quartet.""",
        max_length=200,
        blank=True,
    )

    website = models.URLField(
        help_text="""
            The website URL of the quartet.""",
        blank=True,
    )

    facebook = models.URLField(
        help_text="""
            The facebook URL of the quartet.""",
        blank=True,
    )

    twitter = models.CharField(
        help_text="""
            The twitter handle (in form @twitter_handle) of the quartet.""",
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
            The contact email of the quartet.""",
        blank=True,
    )

    phone = PhoneNumberField(
        verbose_name='mobile number',
        help_text="""
            The contact number of the quartet.""",
        blank=True,
        null=True,
    )

    picture = models.ImageField(
        help_text="""
            The 'official' picture of the contestant.""",
        blank=True,
        null=True,
    )

    blurb = models.TextField(
        help_text="""
            A blurb describing the contestant.  Max 1000 characters.""",
        blank=True,
        max_length=1000,
    )

    district = models.ForeignKey(
        'District',
        help_text="""
            The district the quartet is representing.""",
        blank=True,
        null=True,
    )

    members = models.ManyToManyField(
        'Singer',
        through='CollegiateMembership',
        null=True,
        blank=True,
    )

    @property
    def lead(self):
        lead = self.members.filter(
            collegiatemembership__part=CollegiateMembership.LEAD,
        ).last()
        return lead

    @property
    def tenor(self):
        tenor = self.members.filter(
            collegiatemembership__part=CollegiateMembership.TENOR,
        ).last()
        return tenor

    @property
    def baritone(self):
        baritone = self.members.filter(
            collegiatemembership__part=CollegiateMembership.BARITONE,
        ).last()
        return baritone

    @property
    def bass(self):
        bass = self.members.filter(
            collegiatemembership__part=CollegiateMembership.BASS,
        ).last()
        return bass

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('collegiate', args=[str(self.slug)])

    class Meta:
        ordering = ['name']


class Chorus(models.Model):
    """An individual singer."""
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        coerce_to=str,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the chorus.""",
        max_length=200,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
    )

    chapter = models.OneToOneField(
        'Chapter',
        null=True,
        blank=True,
    )

    location = models.CharField(
        help_text="""
            The geographical location of the contestant.""",
        max_length=200,
        blank=True,
    )

    website = models.URLField(
        help_text="""
            The website URL of the contestant.""",
        blank=True,
    )

    facebook = models.URLField(
        help_text="""
            The facebook URL of the contestant.""",
        blank=True,
    )

    twitter = models.CharField(
        help_text="""
            The twitter handle (in form @twitter_handle) of the contestant.""",
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
            The contact email of the contestant.""",
        blank=True,
    )

    phone = PhoneNumberField(
        verbose_name='mobile number',
        help_text="""
            The Full Name of the Singer.""",
        blank=True,
        null=True,
    )

    director = models.CharField(
        help_text="""
            The name of the director(s) of the chorus.""",
        max_length=200,
        blank=True,
    )

    district = models.ForeignKey(
        'District',
        help_text="""
            The district the
            contestant is representing.""",
        blank=True,
        null=True,
    )

    picture = models.ImageField(
        help_text="""
            The 'official' picture of the contestant.""",
        blank=True,
        null=True,
    )

    blurb = models.TextField(
        help_text="""
            A blurb describing the contestant.  Max 1000 characters.""",
        blank=True,
        max_length=1000,
    )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('chorus', args=[str(self.slug)])

    class Meta:
        ordering = ['name']
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
            The name of the chapter.""",
        max_length=200,
    )

    code = models.CharField(
        help_text="""
            The Chapter code""",
        blank=True,
        null=True,
        max_length=20,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
    )

    district = models.ForeignKey(
        'District',
    )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('chapter', args=[str(self.slug)])


class District(models.Model):
    DISTRICT = 1
    AFFILIATE = 2

    KIND_CHOICES = (
        (DISTRICT, "District"),
        (AFFILIATE, "Affiliate"),
    )

    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        coerce_to=str,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the district.""",
        max_length=200,
    )

    abbreviation = models.CharField(
        null=True,
        blank=True,
        max_length=20,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
    )

    kind = models.IntegerField(
        choices=KIND_CHOICES,
        default=1,
    )

    location = models.CharField(
        help_text="""
            The geographical location of the district.""",
        max_length=200,
        blank=True,
    )

    website = models.URLField(
        help_text="""
            The website URL of the district.""",
        blank=True,
    )

    facebook = models.URLField(
        help_text="""
            The facebook URL of the district.""",
        blank=True,
    )

    twitter = models.CharField(
        help_text="""
            The twitter handle (in form @twitter_handle) of the district.""",
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
            The contact email of the district.""",
        blank=True,
    )

    phone = PhoneNumberField(
        verbose_name='mobile number',
        help_text="""
            District phone number.""",
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('district', args=[str(self.slug)])

    class Meta:
        ordering = ['kind', 'name']


class Contest(models.Model):
    YEAR_CHOICES = []
    for r in range(1939, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))

    INTERNATIONAL = 1
    DISTRICT = 2

    LEVEL_CHOICES = (
        (INTERNATIONAL, 'International',),
        (DISTRICT, 'District',)
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

    def __unicode__(self):
        return "{0} {1} {2}".format(
            self.get_level_display(),
            self.get_year_display(),
            self.get_kind_display(),
        )


class QuartetMembership(models.Model):
    UNKNOWN = 0
    LEAD = 1
    TENOR = 2
    BARITONE = 3
    BASS = 4

    PART_CHOICES = (
        (UNKNOWN, "Unknown"),
        (LEAD, "Lead"),
        (TENOR, "Tenor"),
        (BARITONE, "Baritone"),
        (BASS, "Bass"),
    )

    singer = models.ForeignKey(Singer)
    quartet = models.ForeignKey(Quartet)
    contest = models.ForeignKey(Contest, null=True, blank=True, default=None)
    part = models.IntegerField(
        choices=PART_CHOICES,
        default=UNKNOWN,
    )

    def __unicode__(self):
        return "{0}, {1}, {2}, {3}".format(
            self.quartet,
            self.get_part_display(),
            self.singer,
            self.contest,
        )


class CollegiateMembership(models.Model):
    UNKNOWN = 0
    LEAD = 1
    TENOR = 2
    BARITONE = 3
    BASS = 4

    PART_CHOICES = (
        (UNKNOWN, "Unknown"),
        (LEAD, "Lead"),
        (TENOR, "Tenor"),
        (BARITONE, "Baritone"),
        (BASS, "Bass"),
    )

    singer = models.ForeignKey(Singer)
    collegiate = models.ForeignKey(Collegiate)
    contest = models.ForeignKey(Contest, null=True, blank=True, default=None)
    part = models.IntegerField(
        choices=PART_CHOICES,
        default=UNKNOWN,
    )

    def __unicode__(self):
        return "{0}, {1}, {2}, {3}".format(
            self.collegiate,
            self.get_part_display(),
            self.singer,
            self.contest,
        )


class QuartetPerformance(models.Model):
    FINALS = 1
    SEMIS = 2
    QUARTERS = 3

    ROUND_CHOICES = (
        (FINALS, 'Finals',),
        (SEMIS, 'Semi-Finals',),
        (QUARTERS, 'Quarter-Finals',),
    )

    quartet = models.ForeignKey(Quartet)
    contest = models.ForeignKey(Contest)
    round = models.IntegerField(
        choices=ROUND_CHOICES,
        null=True,
        blank=True,
    )

    appearance = models.IntegerField(
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

    def __unicode__(self):
        return "{0} {1} {2}".format(
            self.quartet,
            self.contest,
            self.get_round_display(),
        )


class ChorusPerformance(models.Model):
    FINALS = 1

    ROUND_CHOICES = (
        (FINALS, 'Finals',),
    )

    chorus = models.ForeignKey(Chorus)
    contest = models.ForeignKey(Contest)
    round = models.IntegerField(
        choices=ROUND_CHOICES,
        default=FINALS
    )

    appearance = models.IntegerField(
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


class CollegiatePerformance(models.Model):
    FINALS = 1

    ROUND_CHOICES = (
        (FINALS, 'Finals',),
    )

    collegiate = models.ForeignKey(Collegiate)
    contest = models.ForeignKey(Contest)
    round = models.IntegerField(
        choices=ROUND_CHOICES,
        default=FINALS
    )
