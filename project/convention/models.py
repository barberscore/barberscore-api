from django.core.exceptions import ValidationError

from django.utils import timezone
from django.conf import settings

import pytz

from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import (
    RegexValidator,
)


class Contestant(models.Model):
    """
    Contestants.

    This class represents a particular contestant.  Historical information
    is not maintained.
    """

    QUARTET = 1
    CHORUS = 2

    CONTESTANT_CHOICES = (
        (QUARTET, "Quartet"),
        (CHORUS, "Chorus"),
    )

    UNK = 0
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
    NZABS = 20
    SNOBS = 21

    DISTRICT_CHOICES = (
        (UNK, 'UNK'),
        (CAR, 'CAR'),
        (CSD, 'CSD'),
        (DIX, 'DIX'),
        (EVG, 'EVG'),
        (FWD, 'FWD'),
        (ILL, 'ILL'),
        (JAD, 'JAD'),
        (LOL, 'LOL'),
        (MAD, 'MAD'),
        (NED, 'NED'),
        (NSC, 'NSC'),
        (ONT, 'ONT'),
        (PIO, 'PIO'),
        (RMD, 'RMD'),
        (SLD, 'SLD'),
        (SUN, 'SUN'),
        (SWD, 'SWD'),
        (BABS, 'BABS'),
        (BHA, 'BHA'),
        (NZABS, 'NZABS'),
        (SNOBS, 'SNOBS'),
    )

    contestant_type = models.IntegerField(
        help_text="""
            The type of contestant, either chorus or quartet.""",
        choices=CONTESTANT_CHOICES,
        default=QUARTET,
    )

    name = models.CharField(
        help_text="""
            The name of the contestant.""",
        max_length=200,
    )

    slug = models.SlugField(
        help_text="""
            The slug, generated in a signal from the name field.""",
        max_length=200,
        unique=True,
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

    phone = models.CharField(
        help_text="""
            The contact phone number of the contestant.""",
        max_length=20,
        blank=True,
    )

    director = models.CharField(
        help_text="""
            The name of the director(s) of the chorus.""",
        max_length=200,
        blank=True,
    )

    lead = models.CharField(
        help_text="""
            The name of the quartet lead.""",
        max_length=50,
        blank=True,
    )

    tenor = models.CharField(
        help_text="""
            The name of the quartet tenor.""",
        max_length=50,
        blank=True,
    )

    baritone = models.CharField(
        help_text="""
            The name of the quartet baritone.""",
        max_length=50,
        blank=True,
    )

    bass = models.CharField(
        help_text="""
            The name of the quartet bass.""",
        max_length=50,
        blank=True,
    )

    district = models.IntegerField(
        help_text="""
            The district the
            contestant is representing.""",
        default=UNK,
        choices=DISTRICT_CHOICES,
    )

    prelim = models.FloatField(
        help_text="""
            The prelim score of the contestant.""",
        null=True,
        blank=True,
    )

    rank = models.IntegerField(
        help_text="""
            The incoming rank based on prelim score.""",
        null=True,
        blank=True,
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

    @property
    def next_performance(self):
        try:
            next_performance = self.performances.order_by('stagetime').first()
        except:
            next_performance = None
        return next_performance

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('contestant', args=[str(self.slug)])

    class Meta:
        ordering = ['contestant_type', 'name']


class Contest(models.Model):
    """
    Contests.

    This class represents a particular contest.
    """

    QUARTET = 1
    CHORUS = 2
    COLLEGIATE = 3
    SENIOR = 4

    CONTEST_TYPE_CHOICES = (
        (QUARTET, 'Quartet'),
        (CHORUS, 'Chorus'),
        (COLLEGIATE, 'Collegiate'),
        (SENIOR, 'Senior'),
    )

    contest_type = models.IntegerField(
        help_text="""
            The contest type:  Quartet, Chorus, Collegiate or Senior.""",
        choices=CONTEST_TYPE_CHOICES,
        default=QUARTET,
    )

    INTERNATIONAL = 1
    DISTRICT = 2
    DIVISION = 3

    CONTEST_LEVEL_CHOICES = (
        (INTERNATIONAL, 'International'),
        # (DISTRICT, 'District'),
        # (DIVISION, 'Division'),
    )

    contest_level = models.IntegerField(
        help_text="""
            The contest level:  International, District, etc..
            Currently only International is supported.""",
        choices=CONTEST_LEVEL_CHOICES,
        default=INTERNATIONAL,
    )

    year = models.CharField(
        help_text="""
            The year of the contest, as a Char.""",
        default='2014',
        max_length=4,
    )

    slug = models.SlugField(
        help_text="""
            The slug of the contest type.""",
        max_length=200,
        unique=True,
    )

    def __unicode__(self):
        return '{0} {1} {2}'.format(
            self.year,
            self.get_contest_level_display(),
            self.get_contest_type_display(),
        )

    class Meta:
        ordering = (
            '-year',
            'contest_level',
            'contest_type',
        )


class Performance(models.Model):
    """
    Performances.

    This class represents the join of a contestant and a contest.
    Each performance consists of two songs in a contest round.  Rounds
    are only applicable to the quartet contest in the context, but the
    field is included for data architecture consistency.
    """

    QUARTERS = 1
    SEMIS = 2
    FINALS = 3

    CONTEST_ROUND_CHOICES = (
        (QUARTERS, 'Quarter-Finals'),
        (SEMIS, 'Semi-Finals'),
        (FINALS, 'Finals'),
    )

    ONE = 1
    TWO = 2

    SESSION_CHOICES = (
        (ONE, "Session #1"),
        (TWO, "Session #2"),
    )

    contest = models.ForeignKey(
        Contest,
        help_text="""
            The contest for this particular performance.""",
        related_name='performances',
    )

    contestant = models.ForeignKey(
        Contestant,
        help_text="""
            The contestant for this particular performance.""",
        related_name='performances',
    )

    contest_round = models.IntegerField(
        help_text="""
            The performance contest round.""",
        choices=CONTEST_ROUND_CHOICES,
        default=FINALS,
    )

    appearance = models.IntegerField(
        help_text="""
            The appearance order, within a given round.""",
        null=True,
        blank=True,
    )

    stagetime = models.DateTimeField(
        help_text="""
            The approximate stagetime of the performance, in
            the local time of the venue. """,
        default=timezone.now,
    )

    session = models.IntegerField(
        help_text="""
            The session number.""",
        default=ONE,
        choices=SESSION_CHOICES,
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

    men_on_stage = models.IntegerField(
        help_text="""
            The number of men on stage (relevant for chorus only.)""",
        blank=True,
        null=True,
    )

    place = models.IntegerField(
        help_text="""
            The ordinal placement of the contestant in this
            particular contest.""",
        blank=True,
        null=True,
    )

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
    def song1_percent(self):
        if self.song1_raw:
            return self.song1_raw / 1500
        else:
            return None

    @property
    def song2_percent(self):
        if self.song2_raw:
            return self.song2_raw / 1500
        else:
            return None

    @property
    def total_percent(self):
        if self.song1_raw:
            return self.total_raw / 3000
        else:
            return None

    def clean(self):
        """
        Multi-field (ie, model) validation.
        """
        if self.contest.contest_type != Contest.QUARTET and self.contest_round != self.FINALS:
            raise ValidationError(
                """Only Quartets have Quarter- and Semi-Final Rounds."""
            )
        if (self.contest.contest_type != Contest.CHORUS and self.contestant.contestant_type == Contestant.CHORUS) or (self.contest.contest_type == Contest.CHORUS and self.contestant.contestant_type != Contestant.CHORUS):
            raise ValidationError(
                    """Contestant and Contest mismatch: {contestant_type} != {contest_type}""".format(
                        contestant_type=self.contestant.get_contestant_type_display(),
                        contest_type=self.contest.get_contest_type_display(),
                    ),
                code='type_mismatch',
                params={
                    'contestant_type': self.contestant.get_contestant_type_display(),
                    'contest_type': self.contest.get_contest_type_display(),
                }
            )

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
        unique_together = (
            'contest',
            'contest_round',
            'appearance',
        )


class Profile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL
    )

    nickname = models.CharField(
        max_length=25,
        blank=True,
    )

    timezone = models.CharField(
        max_length=200,
        default='US/Pacific',
        choices=[(x, x) for x in pytz.common_timezones],
    )

    def __unicode__(self):
        # TODO how to access username attr?
        if self.nickname:
            return self.nickname
        else:
            return self.user.mobile


class Note(models.Model):

    profile = models.ForeignKey(
        Profile,
        related_name='notes',
    )

    contestant = models.ForeignKey(
        Contestant,
        related_name='notes',
    )

    note = models.TextField(
        help_text="""
            Notes on each contestant."""
    )

    def __unicode__(self):
        return "{0} - {1}".format(self.profile, self.contestant)
