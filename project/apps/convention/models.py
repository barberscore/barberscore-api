from __future__ import division

from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import (
    RegexValidator,
)


class Contestant(models.Model):
    """
    Contestants in International Competition.

    This class represents the individual contestants for the
    competition.  They call into two broad categories: quartets and choruses.
    We do not differentiate between collegiate, senior, or main competition
    here; that distinction is left to the `Contest` class.
    """

    QUARTET = 1
    CHORUS = 2

    CONTESTANT_CHOICES = (
        (QUARTET, "Quartet"),
        (CHORUS, "Chorus"),
    )

    contestant_type = models.IntegerField(
        help_text="""
            The type of contestant, either chorus or quartet.""",
        blank=True,
        null=True,
        choices=CONTESTANT_CHOICES
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

    district = models.CharField(
        help_text="""
            The abbreviation of the district the
            contestant is representing.""",
        max_length=50,
        blank=True,
    )

    prelim = models.FloatField(
        help_text="""
            The prelim score of the contestant.""",
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
        return self.performances.order_by('stagetime').first()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('contestant', args=[str(self.slug)])

    class Meta:
        ordering = ['contestant_type', 'name']


class Contest(models.Model):
    """
    Contests in International Competition.

    This class represents the type of contest itself.  Normal choices
    are `Quartet`, `Chorus`, `Collegiate` and `Senior`.  Further
    choices or hierarchical choices are possible, but not supported here.
    """

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
        help_text="""
            The contest type:  Quartet, Chorus, Collegiate or Senior.""",
        blank=True,
        null=True,
        choices=CONTEST_TYPE_CHOICES,
    )

    slug = models.SlugField(
        help_text="""
            The slug of the contest type.""",
        max_length=200,
        unique=True,
    )

    def __unicode__(self):
        return '{0}'.format(self.get_contest_type_display())

    class Meta:
        ordering = ['contest_type']


class Performance(models.Model):
    """
    Performances in International Competition.

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

    GF1 = 1
    QQ1 = 2
    QQ2 = 3
    CF1 = 4
    CF2 = 5
    QS1 = 6
    QF1 = 7

    SESSION_CHOICES = (
        (GF1, "Collegiate Finals"),
        (QQ1, "Quartet Quarter-Finals Session #1"),
        (QQ2, "Quartet Quarter-Finals Session #2"),
        (CF1, "Chorus Finals Session #1"),
        (CF2, "Chorus Finals Session #2"),
        (QS1, "Quartet Semi-Finals"),
        (QF1, "Quartet Finals"),
    )

    contest = models.ForeignKey(
        Contest,
        help_text="""
            The contest for this particular performance.""",
        null=True,
        blank=True,
        related_name='performances',
    )

    contestant = models.ForeignKey(
        Contestant,
        help_text="""
            The contestant for this particular performance.""",
        null=True,
        blank=True,
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
        blank=True,
        null=True,
    )

    stagetime = models.DateTimeField(
        help_text="""
            The approximate stagetime of the performance, in
            the local time of the venue.""",
    )

    session = models.IntegerField(
        help_text="""
            Contest rounds are broken down into sessions, which
            are tracked here.""",
        blank=True,
        null=True,
        choices=SESSION_CHOICES,
    )

    song1 = models.CharField(
        help_text="""
            The title of the first song of the performance.""",
        blank=True,
        null=True,
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
        null=True,
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

    # DENORMALIZED VALUES
    # The following values are denormalized, and the default population
    # happens via pre-save signals.  This allows for manual correction
    # as needed.
    song1_score = models.FloatField(
        help_text="""
            The percentile score of the first song.""",
        blank=True,
        null=True,
    )

    song2_score = models.FloatField(
        help_text="""
            The percentile score of the second song.""",
        blank=True,
        null=True,
    )

    performance_score = models.FloatField(
        help_text="""
            The percentile score of the performance (both songs).""",
        blank=True,
        null=True,
    )

    total_score = models.FloatField(
        help_text="""
            The running percentile score of performances to date
            by this particular contestant.""",
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
