from __future__ import division

import logging
log = logging.getLogger(__name__)

import uuid

import os
import datetime

import arrow

from django.db import (
    models,
)

from django.contrib.postgres.fields import (
    DateRangeField,
    DateTimeRangeField,
)

from psycopg2.extras import Range

from autoslug import AutoSlugField

from django.core.validators import (
    RegexValidator,
    MaxValueValidator,
    MinValueValidator,
)

from django_fsm import (
    transition,
    # FSMField,
    FSMIntegerField,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)

from django.core.exceptions import (
    ValidationError,
)

from model_utils.models import (
    TimeStampedModel,
)

from model_utils.fields import (
    MonitorField,
)

from model_utils import Choices

from mptt.models import (
    MPTTModel,
    TreeForeignKey,
)

from timezone_field import TimeZoneField

from phonenumber_field.modelfields import PhoneNumberField

from nameparser import HumanName

from .managers import (
    UserManager,
    PerformerQuerySet,
)

from .validators import (
    sessions_entered,
    validate_trimmed,
    dixon,
    is_scheduled,
    has_performers,
    has_contests,
    # round_scheduled,
    # contest_started,
    scores_entered,
    songs_entered,
    # rounds_finished,
    # round_finished,
    performances_finished,
    scores_validated,
    song_entered,
    score_entered,
    preceding_finished,
    # preceding_round_finished,
)


def generate_image_filename(instance, filename):
    f, ext = os.path.splitext(filename)
    return '{0}{1}'.format(instance.id, ext)


class Common(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the resource.""",
        max_length=200,
        blank=False,
        unique=True,
        validators=[
            validate_trimmed,
        ],
        error_messages={
            'unique': 'The name must be unique.  Add middle initials, suffixes, years, or other identifiers to make the name unique.',
        }
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    date = DateRangeField(
        help_text="""
            The active dates of the resource.""",
        null=True,
        blank=True,
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
    )

    phone = PhoneNumberField(
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
    )

    class Meta:
        abstract = True


class Arranger(TimeStampedModel):
    """Chorus relation"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
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

    PART = Choices(
        (1, 'arranger', 'Arranger'),
        (2, 'coarranger', 'Co-Arranger'),
    )

    part = models.IntegerField(
        choices=PART,
        default=PART.arranger,
    )

    catalog = models.ForeignKey(
        'Catalog',
        related_name='arrangers',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    person = models.ForeignKey(
        'Person',
        related_name='arrangements',
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1}".format(
            self.catalog,
            self.person,
        )
        super(Arranger, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('catalog', 'person',),
        )


class Award(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'inactive', 'Inactive',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    KIND = Choices(
        (1, 'quartet', 'Quartet',),
        (2, 'chorus', 'Chorus',),
        (3, 'seniors', 'Seniors',),
        (4, 'collegiate', 'Collegiate',),
        (5, 'novice', 'Novice',),
    )

    kind = models.IntegerField(
        choices=KIND,
        null=True,
        blank=True,
    )

    rounds = models.IntegerField(
    )

    long_name = models.CharField(
        max_length=200,
        blank=True,
        default='',
    )

    stix_num = models.IntegerField(
        null=True,
        blank=True,
    )

    stix_name = models.CharField(
        max_length=200,
        blank=True,
        default="",
    )

    organization = TreeForeignKey(
        'Organization',
        related_name='awards',
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            u"{0}".format(self.organization.name),
            u"{0}".format(self.get_kind_display()),
            u"{0}".format(self.long_name),
            u"Championship"
        ]))
        super(Award, self).save(*args, **kwargs)

    class Meta:
        ordering = (
            'organization__level',
            'organization__name',
            'kind',
            'long_name',
        )
        unique_together = (
            ('organization', 'long_name', 'kind',),
        )


class Catalog(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    song_name = models.CharField(
        blank=True,
        max_length=200,
    )

    tune = models.ForeignKey(
        'Tune',
        null=True,
        blank=True,
        related_name='catalogs',
        on_delete=models.SET_NULL,
    )

    bhs_id = models.IntegerField(
        null=True,
        blank=True,
    )

    bhs_published = models.DateField(
        null=True,
        blank=True,
    )

    bhs_songname = models.CharField(
        blank=True,
        max_length=200,
    )

    bhs_arranger = models.CharField(
        blank=True,
        max_length=200,
    )

    bhs_fee = models.FloatField(
        null=True,
        blank=True,
    )

    DIFFICULTY = Choices(
        (1, "Very Easy"),
        (2, "Easy"),
        (3, "Medium"),
        (4, "Hard"),
        (5, "Very Hard"),
    )

    bhs_difficulty = models.IntegerField(
        null=True,
        blank=True,
        choices=DIFFICULTY
    )

    TEMPO = Choices(
        (1, "Ballad"),
        (2, "Uptune"),
        (3, "Mixed"),
    )

    bhs_tempo = models.IntegerField(
        null=True,
        blank=True,
        choices=TEMPO,
    )

    bhs_medley = models.BooleanField(
        default=False,
    )

    is_parody = models.BooleanField(
        default=False,
    )

    is_medley = models.BooleanField(
        default=False,
    )


class Certification(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
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

    CATEGORY = Choices(
        (0, 'admin', 'Admin'),
        (1, 'music', 'Music'),
        (2, 'presentation', 'Presentation'),
        (3, 'singing', 'Singing'),
    )

    category = models.IntegerField(
        choices=CATEGORY,
    )

    STATUS = Choices(
        (0, 'new', 'New'),
        (1, 'active', 'Active'),
        (2, 'candidate', 'Candidate'),
        (3, 'inactive', 'Inactive'),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    date = DateRangeField(
        help_text="""
            The active dates of the resource.""",
        null=True,
        blank=True,
    )

    person = models.ForeignKey(
        'Person',
        related_name='certifications',
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1}".format(
            self.person,
            self.get_category_display(),
        )
        super(Certification, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('category', 'person',),
        )


class Chapter(Common):

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'inactive', 'Inactive',),
        (50, 'dup', 'Duplicate',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    code = models.CharField(
        help_text="""
            The chapter code.""",
        max_length=200,
        blank=True,
        validators=[
            validate_trimmed,
        ],
    )

    organization = TreeForeignKey(
        'Organization',
        related_name='chapters',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "name__icontains",)

    def __unicode__(self):
        return u"{0}".format(self.name)

    class Meta:
        ordering = (
            'name',
        )


class Contest(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=200,
        unique=True,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'built', 'Built',),
        (20, 'started', 'Started',),
        (25, 'finished', 'Finished',),
        (28, 'ranked', 'Ranked',),
        (30, 'final', 'Final',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    GOAL = Choices(
        (1, 'championship', "Championship"),
        (2, 'qualifier', "Qualifier"),
    )

    goal = models.IntegerField(
        help_text="""
            The objective of the contest.""",
        choices=GOAL,
    )

    qual_score = models.FloatField(
        help_text="""
            The objective of the contest.  Note that if the goal is `qualifier` then this must be set.""",
        null=True,
        blank=True,
    )

    YEAR_CHOICES = []
    for r in reversed(range(1939, (datetime.datetime.now().year + 2))):
        YEAR_CHOICES.append((r, r))

    year = models.IntegerField(
        choices=YEAR_CHOICES,
        null=True,
        blank=True,
    )

    ROUNDS_CHOICES = []
    for r in reversed(range(1, 4)):
        ROUNDS_CHOICES.append((r, r))

    # rounds = models.IntegerField(
    #     help_text="""
    #         The number of rounds that will be used in determining the contest.  Note that this may be fewer than the total number of rounds (rounds) in the parent session.""",
    #     choices=ROUNDS_CHOICES,
    #     null=True,
    #     blank=True,
    # )

    HISTORY = Choices(
        (0, 'new', 'New',),
        (10, 'none', 'None',),
        (20, 'pdf', 'PDF',),
        (30, 'places', 'Places',),
        (40, 'incomplete', 'Incomplete',),
        (50, 'complete', 'Complete',),
    )

    history = models.IntegerField(
        help_text="""Used to manage state for historical imports.""",
        choices=HISTORY,
        default=HISTORY.new,
    )

    history_monitor = MonitorField(
        help_text="""History last updated""",
        monitor='history',
    )

    scoresheet_pdf = models.FileField(
        help_text="""
            PDF of the OSS.""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    scoresheet_csv = models.FileField(
        help_text="""
            The parsed scoresheet (used for legacy imports).""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    subsession_id = models.IntegerField(
        null=True,
        blank=True,
    )

    subsession_text = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )

    session = models.ForeignKey(
        'Session',
        related_name='contests',
    )

    award = models.ForeignKey(
        'Award',
        related_name='contests',
    )

    @property
    def champion(self):
        return self.contestants.order_by('place').first()

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "name__icontains",)

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.award.organization.name,
            self.award.get_kind_display(),
            self.award.long_name,
            "Contest",
            str(self.session.convention.year),
        ]))
        super(Contest, self).save(*args, **kwargs)

    # def rank(self):
    #     contestants = self.contestants.all()
    #     for contestant in contestants:
    #         contestant.calculate()
    #         contestant.save()
    #     cursor = []
    #     i = 1
    #     for contestant in self.contestants.order_by('-total_points'):
    #         try:
    #             match = contestant.total_points == cursor[0].total_points
    #         except IndexError:
    #             contestant.place = i
    #             contestant.save()
    #             cursor.append(contestant)
    #             continue
    #         if match:
    #             contestant.place = i
    #             i += len(cursor)
    #             contestant.save()
    #             cursor.append(contestant)
    #             continue
    #         else:
    #             i += 1
    #             contestant.place = i
    #             contestant.save()
    #             cursor = [contestant]
    #     return "{0} Ready for Review".format(self)

    def start(self):
        # Triggered in UI
        # TODO seed performers?
        round = self.rounds.initial()
        p = 0
        for performer in self.performers.accepted().order_by('?'):
            performer.register()
            performer.save()
            round.performances.create(
                round=round,
                performer=performer,
                position=p,
            )
            p += 1
        return "{0} Started".format(self)

    # Check everything is done.
    @transition(
        field=status,
        source=STATUS.finished,
        target=STATUS.ranked,
        conditions=[
            # is_scheduled,
            # is_imsessioned,
            # has_performers,
            # has_contests,
        ],
    )
    def rank(self):
        # Denormalize
        for contestant in self.contestants.all():
            contestant.calculate()
            contestant.save()
        # Rank results
        cursor = []
        i = 1
        for contestant in self.contestants.order_by('-total_points'):
            try:
                match = contestant.total_points == cursor[0].total_points
            except IndexError:
                contestant.place = i
                contestant.save()
                cursor.append(contestant)
                continue
            if match:
                contestant.place = i
                i += len(cursor)
                contestant.save()
                cursor.append(contestant)
                continue
            else:
                i += 1
                contestant.place = i
                contestant.save()
                cursor = [contestant]
        return "{0} Ready for Review".format(self)

    class Meta:
        unique_together = (
            ('session', 'award', 'goal',)
        )
        ordering = (
            'session',
            'award',
            'goal',
        )


class Contestant(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (90, 'final', 'Final',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    performer = models.ForeignKey(
        'Performer',
        related_name='contestants',
    )

    contest = models.ForeignKey(
        'Contest',
        related_name='contestants',
    )

    # Denormalization
    place = models.IntegerField(
        help_text="""
            The final ranking relative to this contest.""",
        null=True,
        blank=True,
        editable=False,
    )

    mus_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_points = models.IntegerField(
        null=True,
        editable=False,
        blank=True,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    total_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    total_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.contest.award.organization.name,
            self.contest.award.get_kind_display(),
            self.contest.award.long_name,
            "Contest",
            str(self.contest.session.convention.year),
            self.performer.group.name,
        ]))
        super(Contestant, self).save(*args, **kwargs)

    def calculate(self):
        self.performer.calculate()
        self.performer.save()
        # If there are no performances, skip.
        if self.performer.performances.exists():
            agg = self.performer.performances.filter(
                round__num__lte=self.contest.award.rounds,
            ).filter(
                round__session=self.contest.session,
            ).aggregate(
                mus=models.Sum('mus_points'),
                prs=models.Sum('prs_points'),
                sng=models.Sum('sng_points'),
            )
            self.mus_points = agg['mus']
            self.prs_points = agg['prs']
            self.sng_points = agg['sng']

            # Calculate total points.
            try:
                self.total_points = sum([
                    self.mus_points,
                    self.prs_points,
                    self.sng_points,
                ])
            except TypeError:
                self.total_points = None

            # Calculate percentile
            try:
                size = self.contest.session.size
                possible = size * 2 * self.performer.performances.count()
                self.mus_score = round(self.mus_points / possible, 1)
                self.prs_score = round(self.prs_points / possible, 1)
                self.sng_score = round(self.sng_points / possible, 1)
                self.total_score = round(self.total_points / (possible * 3), 1)
            except TypeError:
                self.mus_score = None
                self.prs_score = None
                self.sng_score = None
            except ZeroDivisionError:
                self.mus_score = None
                self.prs_score = None
                self.sng_score = None

    class Meta:
        unique_together = (
            ('performer', 'contest',),
        )
        ordering = (
            'contest',
            'place',
        )


class Convention(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'scheduled', 'Scheduled',),
        (20, 'started', 'Started',),
        (30, 'finished', 'Finished',),
        (50, 'final', 'Final',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    KIND = Choices(
        (1, 'international', 'International',),
        (2, 'midwinter', 'Midwinter',),
        (3, 'fall', 'Fall',),
        (4, 'spring', 'Spring',),
        (9, 'video', 'Video',),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of convention.""",
        choices=KIND,
    )

    DIVISION = Choices(
        (200, 'evgd1', "Division I"),
        (210, 'evgd2', "Division II"),
        (220, 'evgd3', "Division III"),
        (230, 'evgd4', "Division IV"),
        (240, 'evgd5', "Division V"),
        (250, 'fwdaz', "Arizona Division"),
        (260, 'fwdnenw', "NE/NW Division"),
        (270, 'fwdsesw', "SE/SW Division"),
        (280, 'lolp1', "Division One/Packerland Division"),
        (290, 'lolnp', "Northern Plains Division"),
        (300, 'lol10sw', "10,000 Lakes and Southwest Division"),
        (310, 'madatl', "Atlantic Division"),
        (320, 'madnw', "Northern and Western Division"),
        (330, 'madsth', "Southern Division"),
        (340, 'nedsun', "Sunrise Division"),
    )

    division = models.IntegerField(
        help_text="""
            Detail if division/combo convention.""",
        choices=DIVISION,
        null=True,
        blank=True,
    )

    YEAR_CHOICES = []
    for r in reversed(range(1939, (datetime.datetime.now().year + 2))):
        YEAR_CHOICES.append((r, r))

    year = models.IntegerField(
        choices=YEAR_CHOICES,
        editable=False,
    )

    date = DateRangeField(
        help_text="""
            The convention dates (will be replaced by start/end).""",
    )

    location = models.CharField(
        help_text="""
            The location of the convention.""",
        max_length=200,
        blank=True,
    )

    timezone = TimeZoneField(
        help_text="""
            The local timezone of the convention.""",
        default='US/Pacific',
    )

    organization = TreeForeignKey(
        'Organization',
        help_text="""
            The organization hosting the convention.""",
    )

    stix_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    stix_div = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    stix_file = models.FileField(
        help_text="""
            The bbstix file.""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    @property
    def human_date(self):
        if self.date:
            if self.date.upper - self.date.lower == datetime.timedelta(1):
                dates = "{0}".format(
                    arrow.get(self.date.lower).format('MMMM D, YYYY'),
                )
            else:
                dates = "{0} - {1}".format(
                    arrow.get(self.date.lower).format('MMMM D'),
                    arrow.get(self.date.upper).format('MMMM D, YYYY'),
                )
        else:
            dates = self.date
        return dates

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.year = arrow.get(self.date.lower).year
        self.name = " ".join(filter(None, [
            self.organization.name,
            self.get_division_display(),
            self.get_kind_display(),
            u"Convention",
            str(self.year),
        ]))
        super(Convention, self).save(*args, **kwargs)

    class Meta:
        ordering = [
            '-year',
            'organization__name',
        ]

        unique_together = (
            ('organization', 'kind', 'year', 'division',),
        )

    @transition(
        field=status,
        source=STATUS.new,
        target=STATUS.scheduled,
        conditions=[
            # TODO Date and location
        ]
    )
    def schedule(self):
        # Triggered from UI
        return

    @transition(
        field=status,
        source=STATUS.scheduled,
        target=STATUS.started,
        conditions=[
            # TODO Within window?
        ]
    )
    def start(self):
        # Triggered from UI
        return

    @transition(
        field=status,
        source=STATUS.started,
        target=STATUS.finished,
        conditions=[
            # Outside of window?
            # Ensure session finished?
        ]
    )
    def finish(self):
        # Triggered from UI
        return

    @transition(
        field=status,
        source=STATUS.finished,
        target=STATUS.final,
        conditions=[
            # Everything else finalized
        ]
    )
    def finalize(self):
        # Triggered from UI
        return


class Director(TimeStampedModel):
    """Chorus relation"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
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

    PART = Choices(
        (1, 'director', 'Director'),
        (2, 'codirector', 'Co-Director'),
    )

    part = models.IntegerField(
        choices=PART,
        default=PART.director,
    )

    performer = models.ForeignKey(
        'Performer',
        related_name='directors',
    )

    person = models.ForeignKey(
        'Person',
        related_name='choruses',
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2}".format(
            self.performer,
            self.get_part_display(),
            self.person,
        )
        super(Director, self).save(*args, **kwargs)

    def clean(self):
        if self.performer.group.kind == Group.KIND.quartet:
            raise ValidationError('Quartets do not have directors.')

    class Meta:
        unique_together = (
            ('performer', 'person',),
        )


class Group(Common):

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'inactive', 'Inactive',),
        (50, 'dup', 'Duplicate',),
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    KIND = Choices(
        (1, 'quartet', 'Quartet'),
        (2, 'chorus', 'Chorus'),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of group; choices are Quartet or Chorus.""",
        choices=KIND,
        default=KIND.quartet,
    )

    chapter = models.ForeignKey(
        'Chapter',
        related_name='groups',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    group_id = models.IntegerField(
        null=True,
        blank=True,
    )

    bhs_name = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_district = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_location = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_contact = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_expiration = models.CharField(
        max_length=255,
        blank=True,
    )

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "name__icontains",)

    def __unicode__(self):
        return u"{0}".format(self.name)

    class Meta:
        ordering = (
            'name',
        )


class Judge(TimeStampedModel):
    """Contest Judge"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'scheduled', 'Scheduled',),
        (20, 'confirmed', 'Confirmed',),
        (30, 'final', 'Final',),
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    CATEGORY = Choices(
        (0, 'admin', 'Admin'),
        (1, 'music', 'Music'),
        (2, 'presentation', 'Presentation'),
        (3, 'singing', 'Singing'),
    )

    category = models.IntegerField(
        choices=CATEGORY,
    )

    KIND = Choices(
        (10, 'official', 'Official'),
        (20, 'practice', 'Practice'),
        (30, 'composite', 'Composite'),
    )

    kind = models.IntegerField(
        choices=KIND,
    )

    slot = models.IntegerField(
        null=True,
        blank=True,
    )

    session = models.ForeignKey(
        'Session',
        related_name='judges',
    )

    round = models.ForeignKey(
        'Round',
        related_name='judges',
    )

    person = models.ForeignKey(
        'Person',
        related_name='panels',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={'is_judge': True},
        # limit_choices_to=models.Q(certifications__isnull=False),
    )

    organization = TreeForeignKey(
        'Organization',
        related_name='judges',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    panel_id = models.IntegerField(
        null=True,
        blank=True,
    )

    @property
    def designation(self):
        if self.kind == self.KIND.official:
            designation = u"{0[0]}{1:1d}".format(
                self.get_category_display(),
                self.slot,
            )
        else:
            designation = u"{0[0]}{1:1d}".format(
                self.get_category_display().lower(),
                self.slot,
            )
        return designation

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2} {3}".format(
            self.session,
            self.get_kind_display(),
            self.get_category_display(),
            self.slot,
        )
        super(Judge, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('session', 'category', 'kind', 'slot'),
        )
        ordering = (
            'session',
            'category',
            'kind',
            'slot',
        )


class Organization(MPTTModel, TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the resource.""",
        max_length=200,
        validators=[
            validate_trimmed,
        ],
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        # unique=True,
        max_length=255,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'inactive', 'Inactive',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    LEVEL = Choices(
        (0, 'international', "International"),
        (1, 'district', "District/Affiliates"),
        (2, 'division', "Division"),
    )

    level = models.IntegerField(
        help_text="""
            The level of the contest.  Note that this may be different than the level of the parent session.""",
        choices=LEVEL,
        null=True,
        blank=True,
    )

    KIND = Choices(
        ('International', [
            (0, 'international', "International"),
            (50, 'hi', "Harmony Incorporated"),
        ]),
        ('District', [
            (10, 'district', "District"),
            (20, 'noncomp', "Noncompetitive"),
            (30, 'affiliate', "Affiliate"),
        ]),
        ('Division', [
            (40, 'division', "Division"),
        ]),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of organization.""",
        choices=KIND,
        null=True,
        blank=True,
    )

    date = DateRangeField(
        help_text="""
            The active dates of the resource.""",
        null=True,
        blank=True,
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
    )

    phone = PhoneNumberField(
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
    )

    short_name = models.CharField(
        help_text="""
            A short-form name for the resource.""",
        blank=True,
        max_length=200,
    )

    long_name = models.CharField(
        help_text="""
            A long-form name for the resource.""",
        blank=True,
        max_length=200,
    )

    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        on_delete=models.SET_NULL,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    class MPTTMeta:
        order_insertion_by = [
            'kind',
            'short_name',
        ]
        # ordering = [
        #     'tree_id',
        # ]


class Performance(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'started', 'Started',),
        (20, 'finished', 'Finished',),
        (30, 'entered', 'Entered',),
        (40, 'flagged', 'Flagged',),
        (50, 'accepted', 'Accepted',),
        (90, 'final', 'Final',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    position = models.PositiveSmallIntegerField(
        'Position',
    )

    scheduled = DateTimeRangeField(
        help_text="""
            The scheduled performance window.""",
        null=True,
        blank=True,
    )

    actual = DateTimeRangeField(
        help_text="""
            The actual performance window.""",
        null=True,
        blank=True,
    )

    # Denormalized
    place = models.IntegerField(
        help_text="""
            The final ranking relative to this round.""",
        null=True,
        blank=True,
        editable=False,
    )

    mus_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    total_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    total_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    round = models.ForeignKey(
        'Round',
        related_name='performances',
    )

    performer = models.ForeignKey(
        'Performer',
        related_name='performances',
    )

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "name__icontains",)

    @property
    def draw(self):
        try:
            return "{0:02d}".format(self.position + 1)
        except TypeError:
            return None

    @property
    def start_dt(self):
        return self.scheduled.lower

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1}".format(
            self.round,
            self.performer.group,
        )
        self.name = " ".join(filter(None, [
            self.round.session.convention.organization.name,
            self.round.session.convention.get_division_display(),
            self.round.session.convention.get_kind_display(),
            self.round.session.get_kind_display(),
            self.round.get_kind_display(),
            str(self.round.session.convention.year),
            "Performance",
            str(self.draw),
        ]))
        super(Performance, self).save(*args, **kwargs)

    class Meta:
        ordering = (
            'round',
            'position',
        )
        unique_together = (
            ('round', 'position',),
        )

    def calculate(self):
        for song in self.songs.all():
            song.calculate()
            song.save()
        if self.songs.exists():
            agg = self.songs.all().aggregate(
                mus=models.Sum('mus_points'),
                prs=models.Sum('prs_points'),
                sng=models.Sum('sng_points'),
            )
            self.mus_points = agg['mus']
            self.prs_points = agg['prs']
            self.sng_points = agg['sng']

            # Calculate total points.
            try:
                self.total_points = sum([
                    self.mus_points,
                    self.prs_points,
                    self.sng_points,
                ])
            except TypeError:
                self.total_points = None

            # Calculate percentile scores
            try:
                possible = self.round.session.size * 2
                self.mus_score = round(self.mus_points / possible, 1)
                self.prs_score = round(self.prs_points / possible, 1)
                self.sng_score = round(self.sng_points / possible, 1)
                self.total_score = round(self.total_points / (possible * 3), 1)
            except TypeError:
                self.mus_score = None
                self.prs_score = None
                self.sng_score = None

    def get_preceding(self):
        try:
            obj = self.__class__.objects.get(
                round=self.round,
                position=self.position - 1,
            )
            return obj
        except self.DoesNotExist:
            return None

    def get_next(self):
        try:
            obj = self.__class__.objects.get(
                round=self.round,
                position=self.position + 1,
            )
            return obj
        except self.DoesNotExist:
            return None

    # @transition(
    #     field=status,
    #     source=STATUS.new,
    #     target=STATUS.built,
    #     conditions=[
    #     ]
    # )
    # def build(self):
    #     return

    # @transition(
    #     field=status,
    #     source=STATUS.built,
    #     target=STATUS.ready,
    # )
    # def prep(self):
    #     return

    @transition(
        field=status,
        source=[
            STATUS.new,
        ],
        target=STATUS.started,
        conditions=[
            # preceding_finished,
        ]
    )
    def start(self):
        # Triggered from UI

        # # Set start time
        # self.actual = Range(
        #     arrow.now().datetime,
        #     None,
        # )

        # Creates Song and Score sentinels.
        i = 1
        while i <= 2:
            song = self.songs.create(
                performance=self,
                order=i,
            )
            for judge in self.round.judges.filter(
                kind=self.round.judges.model.KIND.official,
            ).exclude(
                category=self.round.judges.model.CATEGORY.admin,
            ):
                song.scores.create(
                    song=song,
                    judge=judge,
                    category=judge.category,
                    kind=judge.kind,
                )
            i += 1
        return

    @transition(
        field=status,
        source=STATUS.started,
        target=STATUS.finished,
        conditions=[
        ]
    )
    def finish(self):
        # Triggered from UI
        # self.actual = (
        #     self.actual.lower,
        #     arrow.now().datetime,
        # )
        return

    @transition(
        field=status,
        source=STATUS.finished,
        target=STATUS.entered,
        conditions=[
            songs_entered,
            scores_entered,
        ]
    )
    def enter(self):
        # Calls post-transition signal for dixon test
        return

    @transition(
        field=status,
        source=[
            STATUS.entered,
        ],
        target=STATUS.flagged,
        # conditions=[
        #     round_finished,   TODO No is_flagged
        # ]
    )
    def flag(self):
        return

    @transition(
        field=status,
        source=[
            STATUS.entered,
            STATUS.flagged,
        ],
        target=STATUS.accepted,
        # conditions=[
        #     round_finished,   TODO No is_flagged
        # ]
    )
    def accept(self):
        return

    @transition(
        field=status,
        source=STATUS.accepted,
        target=STATUS.final,
        conditions=[
        ]
    )
    def finalize(self):
        return


class Performer(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'qualified', 'Qualified',),
        (20, 'accepted', 'Accepted',),
        (30, 'declined', 'Declined',),
        (40, 'dropped', 'Dropped',),
        (50, 'official', 'Official',),
        (60, 'finished', 'Finished',),
        (90, 'final', 'Final',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    picture = models.ImageField(
        help_text="""
            The on-stage session picture (as opposed to the "official" photo).""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    men = models.IntegerField(
        help_text="""
            The number of men on stage.""",
        default=4,
        null=True,
        blank=True,
    )

    # Denormalized
    seed = models.IntegerField(
        help_text="""
            The incoming rank based on prelim score.""",
        null=True,
        blank=True,
        # editable=False,
    )

    prelim = models.FloatField(
        help_text="""
            The incoming prelim score.""",
        null=True,
        blank=True,
        # editable=False,
    )

    place = models.IntegerField(
        help_text="""
            The final placement/rank of the performer for the entire session (ie, not a specific contest).""",
        null=True,
        blank=True,
        editable=False,
    )

    mus_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_points = models.IntegerField(
        null=True,
        editable=False,
        blank=True,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    total_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    total_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    session = models.ForeignKey(
        'Session',
        related_name='performers',
    )

    group = models.ForeignKey(
        'Group',
        related_name='performers',
    )

    organization = TreeForeignKey(
        'Organization',
        related_name='performers',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    @property
    def delta_score(self):
        """ The difference between qualifying score and final score.""",
        try:
            return self.total_score - self.prelim
        except TypeError:
            return None

    @property
    def delta_place(self):
        """ The difference between qualifying rank and final rank.""",
        try:
            return self.seed - self.place
        except TypeError:
            return None

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "name__icontains",)

    objects = PerformerQuerySet.as_manager()

    def __unicode__(self):
        return u"{0}".format(self.name)

    def clean(self):
        if self.singers.count() > 4:
            raise ValidationError('There can not be more than four persons in a quartet.')

    def save(self, *args, **kwargs):
        # self.name = u"{0} {1}".format(
        #     self.session,
        #     self.group.name,
        # )
        self.name = " ".join(filter(None, [
            self.session.convention.organization.name,
            self.session.convention.get_division_display(),
            self.session.convention.get_kind_display(),
            str(self.session.convention.year),
            self.session.get_kind_display(),
            "Performer",
            self.group.name,
        ]))
        super(Performer, self).save(*args, **kwargs)

    class Meta:
        ordering = (
            'session',
            'group',
        )
        unique_together = (
            ('group', 'session',),
        )

    def calculate(self):
        for performance in self.performances.all():
            performance.calculate()
            performance.save()
        # If there are no performances, skip.
        if self.performances.exists():
            agg = self.performances.all().aggregate(
                mus=models.Sum('mus_points'),
                prs=models.Sum('prs_points'),
                sng=models.Sum('sng_points'),
            )
            self.mus_points = agg['mus']
            self.prs_points = agg['prs']
            self.sng_points = agg['sng']

            # Calculate total points.
            try:
                self.total_points = sum([
                    self.mus_points,
                    self.prs_points,
                    self.sng_points,
                ])
            except TypeError:
                self.total_points = None

            # Calculate percentile
            try:
                possible = self.session.size * 2 * self.performances.count()
                self.mus_score = round(self.mus_points / possible, 1)
                self.prs_score = round(self.prs_points / possible, 1)
                self.sng_score = round(self.sng_points / possible, 1)
                self.total_score = round(self.total_points / (possible * 3), 1)
            except TypeError:
                self.mus_score = None
                self.prs_score = None
                self.sng_score = None

    @transition(
        field=status,
        source=STATUS.new,
        target=STATUS.qualified
    )
    def qualify(self):
        # Send notice?
        return "{0} Qualified".format(self)

    @transition(
        field=status,
        source=[
            STATUS.qualified,
            STATUS.declined,
        ],
        target=STATUS.accepted,
    )
    def accept(self):
        # Send notice?
        return "{0} Accepted".format(self)

    @transition(
        field=status,
        source=[
            STATUS.qualified,
            STATUS.accepted,
        ],
        target=STATUS.declined,
    )
    def decline(self):
        # Send notice?
        return "{0} Declined".format(self)

    @transition(
        field=status,
        source=STATUS.accepted,
        target=STATUS.official,
    )
    def register(self):
        # Triggered by contest start
        return "{0} Official".format(self)

    @transition(
        field=status,
        source=STATUS.official,
        target=STATUS.dropped,
    )
    def drop(self):
        # Send notice?
        return "{0} Dropped".format(self)

    @transition(
        field=status,
        source=STATUS.official,
        target=STATUS.finished,
    )
    def finish(self):
        # Send notice?
        return "{0} Finished".format(self)

    @transition(
        field=status,
        source=STATUS.finished,
        target=STATUS.final,
    )
    def finalize(self):
        # Send notice?
        return "{0} Finalized".format(self)


class Person(Common):

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'inactive', 'Inactive',),
        (30, 'retired', 'Retired',),
        (40, 'deceased', 'Deceased',),
        (50, 'stix', 'Stix Issue',),
        (60, 'dup', 'Possible Duplicate',),
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    member = models.IntegerField(
        null=True,
        blank=True,
    )

    # Denormalization for searching
    common_name = models.CharField(
        max_length=255,
        blank=True,
        editable=False,
        default='',
    )

    # Denormalization for searching
    full_name = models.CharField(
        max_length=255,
        blank=True,
        editable=False,
        default='',
    )

    # Denormalization for searching
    formal_name = models.CharField(
        max_length=255,
        blank=True,
        editable=False,
        default='',
    )

    # Denormalization to make autocomplete work
    is_judge = models.BooleanField(
        default=False,
        editable=False,
    )

    organization = TreeForeignKey(
        'Organization',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    bhs_member_id = models.IntegerField(
        null=True,
        blank=True,
    )

    bhs_name = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_city = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_state = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_phone = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_email = models.EmailField(
        blank=True,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.is_judge = self.certifications.exists()
        name = HumanName(self.name)
        if name.nickname:
            self.common_name = " ".join(filter(None, [
                u"{0}".format(name.nickname),
                u"{0}".format(name.last),
                u"{0}".format(name.suffix),
            ]))
        else:
            self.common_name = u'{0}'.format(self.name)
        self.formal_name = " ".join(filter(None, [
            u'{0}'.format(name.first),
            u'{0}'.format(name.last),
            u'{0}'.format(name.suffix),
        ]))
        super(Person, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "name__icontains",)

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

    @property
    def nick_name(self):
        if self.name:
            name = HumanName(self.name)
            return name.nickname
        else:
            return None


class Round(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'built', 'Built',),
        (15, 'ready', 'Ready',),
        (20, 'started', 'Started',),
        (25, 'finished', 'Finished',),
        (28, 'ranked', 'Ranked',),
        (30, 'final', 'Final',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    KIND = Choices(
        (1, 'finals', 'Finals'),
        (2, 'semis', 'Semi-Finals'),
        (3, 'quarters', 'Quarter-Finals'),
    )

    kind = models.IntegerField(
        choices=KIND,
    )

    num = models.IntegerField(
    )

    date = DateRangeField(
        help_text="""
            The active dates of the resource.""",
        null=True,
        blank=True,
    )

    slots = models.IntegerField(
        null=True,
        blank=True,
    )

    stix_name = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )

    session = models.ForeignKey(
        'Session',
        related_name='rounds',
    )

    class Meta:
        ordering = (
            'session',
            'kind',
        )
        unique_together = (
            ('session', 'kind',),
        )

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.session.convention.organization.name,
            self.session.convention.get_division_display(),
            self.session.convention.get_kind_display(),
            self.session.get_kind_display(),
            self.get_kind_display(),
            str(self.session.convention.year),
        ]))
        super(Round, self).save(*args, **kwargs)

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "name__icontains",)

    def __unicode__(self):
        return u"{0}".format(self.name)

    def get_preceding(self):
        try:
            obj = self.__class__.objects.get(
                contest=self.contest,
                kind=self.kind + 1,
            )
            return obj
        except self.DoesNotExist:
            return None

    def get_next(self):
        try:
            obj = self.__class__.objects.get(
                contest=self.contest,
                kind=self.kind - 1,
            )
            return obj
        except self.DoesNotExist:
            return None

    def next_performance(self):
        try:
            return self.performances.filter(
                status=self.performances.model.STATUS.ready,
            ).order_by('position').first()
        except self.performances.model.DoesNotExist:
            return None

    @transition(
        field=status,
        source=STATUS.new,
        target=STATUS.started,
        conditions=[
            # round_drawn,
            # round_scheduled,
            # contest_started,
            # preceding_round_finished,
        ]
    )
    def start(self):
        # Triggered in UI
        return

    @transition(
        field=status,
        source=STATUS.started,
        target=STATUS.finished,
        conditions=[
            # performances_finished,
        ]
    )
    def finish(self):
        for performance in self.performances.all():
            performance.calculate()
            performance.save()
        return

    @transition(
        field=status,
        source=STATUS.finished,
        target=STATUS.ranked,
        conditions=[
            # Add performances ACCEPTED
        ]
    )
    def rank(self):
        # TODO Validate performances over
        cursor = []
        i = 1
        for performance in self.performances.order_by('-total_points'):
            try:
                match = performance.total_points == cursor[0].total_points
            except IndexError:
                performance.place = i
                performance.save()
                cursor.append(performance)
                continue
            if match:
                performance.place = i
                i += len(cursor)
                performance.save()
                cursor.append(performance)
                continue
            else:
                i += 1
                performance.place = i
                performance.save()
                cursor = [performance]
        return "Round Ended"

    @transition(
        field=status,
        source=STATUS.ranked,
        target=STATUS.final,
    )
    def finalize(self):
        return
        # # TODO Some validation
        # try:
        #     # TODO This is an awful lot to be in a try/except; refactor?
        #     next_round = self.contest.rounds.get(
        #         kind=(self.kind - 1),
        #     )
        #     qualifiers = self.performances.filter(
        #         place__lte=next_round.slots,
        #     ).order_by('?')
        #     p = 0
        #     for qualifier in qualifiers:
        #         l = next_round.performances.create(
        #             performer=qualifier.performer,
        #             position=p,
        #             # start=next_round.start,
        #         )
        #         p += 1
        #         p1 = l.songs.create(performance=l, order=1)
        #         p2 = l.songs.create(performance=l, order=2)
        #         for j in self.contest.judges.scoring():
        #             p1.scores.create(
        #                 song=p1,
        #                 judge=j,
        #             )
        #             p2.scores.create(
        #                 song=p2,
        #                 judge=j,
        #             )
        # except self.DoesNotExist:
        #     pass
        # return 'Round Confirmed'
    # def draw_contest(self):
    #     cs = self.performers.order_by('?')
    #     round = self.rounds.get(kind=self.rounds)
    #     p = 0
    #     for c in cs:
    #         round.performances.create(
    #             performer=c,
    #             position=p,
    #             start=round.start,
    #         )
    #         p += 1
    #     self.status = self.STATUS.ready
    #     self.save()


class Score(TimeStampedModel):
    """
        The Score is never released publicly.  These are the actual
        Judge's scores from the contest.
    """
    STATUS = Choices(
        (0, 'new', 'New',),
        (20, 'entered', 'Entered',),
        (30, 'flagged', 'Flagged',),
        (35, 'validated', 'Validated',),
        (40, 'confirmed', 'Confirmed',),
        (50, 'final', 'Final',),
    )

    CATEGORY = Choices(
        (0, 'admin', 'Admin'),
        (1, 'music', 'Music'),
        (2, 'presentation', 'Presentation'),
        (3, 'singing', 'Singing'),
    )

    KIND = Choices(
        (10, 'official', 'Official'),
        (20, 'practice', 'Practice'),
        (30, 'composite', 'Composite'),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    song = models.ForeignKey(
        'Song',
        related_name='scores',
    )

    judge = models.ForeignKey(
        'Judge',
        related_name='scores',
    )

    category = models.IntegerField(
        choices=CATEGORY,
    )

    kind = models.IntegerField(
        choices=KIND,
    )

    dixon_test = models.NullBooleanField(
    )

    points = models.IntegerField(
        help_text="""
            The number of points contested (0-100)""",
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(
                100,
                message='Points must be between 0 - 100',
            ),
            MinValueValidator(
                0,
                message='Points must be between 0 - 100',
            ),
        ]
    )

    class Meta:
        ordering = (
            'song',
            'judge',
        )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.id.hex,
        ]))
        super(Score, self).save(*args, **kwargs)

    # @transition(
    #     field=status,
    #     source=STATUS.new,
    #     target=STATUS.flagged,
    #     conditions=[
    #         score_entered,
    #         # TODO Could be 'performance_finished' here if want to prevent admin UI
    #     ]
    # )
    # def flag(self):
    #     # Triggered from dixon test in performance.finish()
    #     return

    # @transition(
    #     field=status,
    #     source=[
    #         STATUS.new,
    #         STATUS.flagged,
    #     ],
    #     target=STATUS.validated,
    #     conditions=[
    #         score_entered,
    #         # TODO Could be 'performance_finished' here if want to prevent admin UI
    #     ]
    # )
    # def validate(self):
    #     # Triggered from dixon test in performance.finish() or UI
    #     return

    # @transition(
    #     field=status,
    #     source=[
    #         STATUS.validated,
    #     ],
    #     target=STATUS.confirmed,
    #     conditions=[
    #         # song_entered,
    #     ]
    # )
    # def confirm(self):
    #     return

    # @transition(
    #     field=status,
    #     source=STATUS.confirmed,
    #     target=STATUS.final,
    # )
    # def finalize(self):
    #     return


class Session(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'built', 'Built',),
        (20, 'started', 'Started',),
        (25, 'ranked', 'Ranked',),
        (30, 'finished', 'Finished',),
        (50, 'final', 'Final',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    KIND = Choices(
        (1, 'quartet', 'Quartet',),
        (2, 'chorus', 'Chorus',),
        (3, 'seniors', 'Seniors',),
        (4, 'collegiate', 'Collegiate',),
        (5, 'novice', 'Novice',),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of session.  Generally this will be either quartet or chorus, with the exception being International and Midwinter which hold exclusive Collegiate and Senior sessions respectively.""",
        choices=KIND,
    )

    SIZE_CHOICES = []
    for r in reversed(range(1, 6)):
        SIZE_CHOICES.append((r, r))

    size = models.IntegerField(
        help_text="""
            Size of the judging panel (per category).""",
        choices=SIZE_CHOICES,
    )

    ROUNDS_CHOICES = []
    for r in reversed(range(1, 4)):
        ROUNDS_CHOICES.append((r, r))

    # num_rounds = models.IntegerField(
    #     help_text="""
    #         Number of rounds (rounds) for the session.""",
    #     choices=ROUNDS_CHOICES,
    #     default=1,
    #     null=True,
    #     blank=True,
    # )

    date = DateRangeField(
        help_text="""
            The active dates of the session.""",
        null=True,
        blank=True,
    )

    # Denormalized
    YEAR_CHOICES = []
    for r in reversed(range(1939, (datetime.datetime.now().year + 2))):
        YEAR_CHOICES.append((r, r))

    year = models.IntegerField(
        choices=YEAR_CHOICES,
        editable=False,
    )

    # Legacy
    HISTORY = Choices(
        (0, 'new', 'New',),
        (10, 'none', 'None',),
        (20, 'pdf', 'PDF',),
        (30, 'places', 'Places',),
        (40, 'incomplete', 'Incomplete',),
        (50, 'complete', 'Complete',),
    )

    history = models.IntegerField(
        help_text="""Used to manage state for historical imports.""",
        choices=HISTORY,
        default=HISTORY.new,
    )

    history_monitor = MonitorField(
        help_text="""History last updated""",
        monitor='history',
    )

    scoresheet_pdf = models.FileField(
        help_text="""
            The historical PDF OSS.""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    scoresheet_csv = models.FileField(
        help_text="""
            The parsed scoresheet (used for legacy imports).""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    # Denormalized
    organization = TreeForeignKey(
        'Organization',
        related_name='sessions',
        editable=False,
    )

    convention = models.ForeignKey(
        'Convention',
        related_name='sessions',
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.year = self.convention.year
        self.organization = self.convention.organization
        self.name = " ".join(filter(None, [
            self.convention.organization.name,
            self.convention.get_division_display(),
            self.convention.get_kind_display(),
            self.get_kind_display(),
            "Session",
            str(self.convention.year),
        ]))
        super(Session, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('convention', 'kind',),
        )
        ordering = (
            '-year',
            'convention',
            'kind',
        )

    @transition(
        field=status,
        source=STATUS.new,
        target=STATUS.built,
        conditions=[
            # is_scheduled,
            # is_imsessioned,
            # has_performers,
            # has_contests,
        ],
    )
    def build(self):
        # Triggered in UI
        return

    @transition(
        field=status,
        source=STATUS.built,
        target=STATUS.started,
        conditions=[
            # is_scheduled,
            # is_imsessioned,
            # has_performers,
            # has_contests,
        ],
    )
    def start(self):
        # Triggered in UI
        # TODO seed performers?
        round = self.rounds.get(num=1)
        p = 0
        for performer in self.performers.accepted().order_by('?'):
            performer.register()
            performer.save()
            round.performances.create(
                round=round,
                performer=performer,
                position=p,
            )
            p += 1
        return "{0} Started".format(self)

    @transition(
        field=status,
        source=STATUS.started,
        target=STATUS.finished,
        conditions=[
            # is_scheduled,
            # is_imsessioned,
            # has_performers,
            # has_contests,
        ],
    )
    def finish(self):
        # Triggered in UI
        return

    @transition(
        field=status,
        source=STATUS.finished,
        target=STATUS.ranked,
        conditions=[
            # is_scheduled,
            # is_imsessioned,
            # has_performers,
            # has_contests,
        ],
    )
    def rank(self):
        for performer in self.performances.all():
            performer.calculate()
            performer.save()
        for contest in self.contests.all():
            contest.rank()
            contest.save()
        return

    @transition(
        field=status,
        source=STATUS.ranked,
        target=STATUS.final,
        conditions=[
            # is_scheduled,
            # is_imsessioned,
            # has_performers,
            # has_contests,
        ],
    )
    def finalize(self):
        # Triggered in UI
        return


class Singer(TimeStampedModel):
    """Quartet Relation"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
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

    PART = Choices(
        (1, 'tenor', 'Tenor'),
        (2, 'lead', 'Lead'),
        (3, 'baritone', 'Baritone'),
        (4, 'bass', 'Bass'),
    )

    part = models.IntegerField(
        choices=PART,
    )

    performer = models.ForeignKey(
        'Performer',
        related_name='singers',
    )

    person = models.ForeignKey(
        'Person',
        related_name='quartets',
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def clean(self):
        # if self.performer.group.kind == Group.CHORUS:
        #     raise ValidationError('Choruses do not have quartet singers.')
        if self.part:
            if [s['part'] for s in self.performer.singers.values(
                'part'
            )].count(self.part) > 1:
                raise ValidationError('There can not be more than one of the same part in a quartet.')

    class Meta:
        unique_together = (
            ('performer', 'person',),
        )
        ordering = (
            '-name',
        )

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2}".format(
            self.performer,
            self.get_part_display(),
            self.person,
        )
        super(Singer, self).save(*args, **kwargs)


class Song(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        # (10, 'built', 'Built',),
        # (20, 'entered', 'Entered',),
        # (30, 'flagged', 'Flagged',),
        # (35, 'validated', 'Validated',),
        (40, 'confirmed', 'Confirmed',),
        (50, 'final', 'Final',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    ORDER = Choices(
        (1, 'first', 'First'),
        (2, 'second', 'Second'),
    )

    order = models.IntegerField(
        choices=ORDER,
    )

    title = models.CharField(
        max_length=255,
        blank=True,
    )

    arranger = models.CharField(
        max_length=255,
        blank=True,
    )

    is_parody = models.BooleanField(
        default=False,
    )

    # Denormalized values
    mus_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    total_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    total_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    catalog = models.ForeignKey(
        'Catalog',
        related_name='songs',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    tune = models.ForeignKey(
        'Tune',
        related_name='songs',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    performance = models.ForeignKey(
        'Performance',
        related_name='songs',
    )

    class Meta:
        ordering = [
            'performance',
            'order',
        ]
        unique_together = (
            ('performance', 'order',),
        )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2}".format(
            self.performance,
            'Song',
            self.order,
        )
        self.name = " ".join(filter(None, [
            self.performance.round.session.convention.organization.name,
            self.performance.round.session.convention.get_division_display(),
            self.performance.round.session.convention.get_kind_display(),
            self.performance.round.session.get_kind_display(),
            self.performance.round.get_kind_display(),
            str(self.performance.round.session.convention.year),
            "Performance",
            str(self.performance.draw),
            'Song',
            str(self.order),
        ]))
        super(Song, self).save(*args, **kwargs)

    def calculate(self):
        if self.scores.exists():
            # Only use the Scores model when we have scores
            # from a judging panel.  Otherwise, use what's
            # already there (typically imported).
            scores = self.scores.exclude(
                kind=self.scores.model.KIND.practice,
            ).order_by(
                'category',
            ).values(
                'category',
            ).annotate(
                total=models.Sum('points')
            )
            for score in scores:
                if score['category'] == self.scores.model.CATEGORY.music:
                    self.mus_points = score['total']
                if score['category'] == self.scores.model.CATEGORY.presentation:
                    self.prs_points = score['total']
                if score['category'] == self.scores.model.CATEGORY.singing:
                    self.sng_points = score['total']

            # Calculate total points.
            try:
                self.total_points = sum([
                    self.mus_points,
                    self.prs_points,
                    self.sng_points,
                ])
            except TypeError:
                self.total_points = None

            # Calculate percentile scores.
            try:
                possible = self.performance.round.session.size
                self.mus_score = round(self.mus_points / possible, 1)
                self.prs_score = round(self.prs_points / possible, 1)
                self.sng_score = round(self.sng_points / possible, 1)
                self.total_score = round(self.total_points / (possible * 3), 1)
            except TypeError:
                self.mus_score = None
                self.prs_score = None
                self.sng_score = None


class Tune(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=200,
        unique=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "name__icontains",)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u"{0}".format(self.name)


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    email = models.EmailField(
        unique=True,
        help_text="""Your email address will be your username.""",
    )
    name = models.CharField(
        max_length=200,
        help_text="""Your full name.""",
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )
    date_joined = models.DateField(
        auto_now_add=True,
    )

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
