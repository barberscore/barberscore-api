from __future__ import division

import logging
log = logging.getLogger(__name__)

import uuid

import os
import datetime

from django.db import (
    models,
)

from django.db.models.query import (
    QuerySet,
)

from autoslug import AutoSlugField

from django.core.validators import (
    RegexValidator,
    # MaxValueValidator,
    # MinValueValidator,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
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

from model_utils.managers import (
    PassThroughManager,
)

from mptt.models import (
    MPTTModel,
    TreeForeignKey,
)

from timezone_field import TimeZoneField

from phonenumber_field.modelfields import PhoneNumberField

from nameparser import HumanName

from .validators import (
    validate_trimmed,
    dixon,
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

    start = models.DateField(
        help_text="""
            The founding/birth date of the resource.""",
        blank=True,
        null=True,
    )

    end = models.DateField(
        help_text="""
            The retirement/deceased date of the resource.""",
        blank=True,
        null=True,
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

    is_active = models.BooleanField(
        help_text="""
            A boolean for active/living resources.""",
        default=True,
    )

    class Meta:
        abstract = True


class Arranger(models.Model):
    """Chorus relation"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    PART = Choices(
        (1, 'arranger', 'Arranger'),
        (2, 'coarranger', 'Co-Arranger'),
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

    catalog = models.ForeignKey(
        'Catalog',
        related_name='arrangers',
        null=True,
        blank=True,
    )

    person = models.ForeignKey(
        'Person',
        related_name='arrangements',
    )

    part = models.IntegerField(
        choices=PART,
        default=PART.arranger,
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


class Award(models.Model):

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

    def __unicode__(self):
        return u"{0}".format(self.name)

    class Meta:
        ordering = (
            'name',
        )


class Catalog(models.Model):
    TEMPO = Choices(
        (1, "Ballad"),
        (2, "Uptune"),
        (3, "Mixed"),
    )

    DIFFICULTY = Choices(
        (1, "Very Easy"),
        (2, "Easy"),
        (3, "Medium"),
        (4, "Hard"),
        (5, "Very Hard"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    tune = models.ForeignKey(
        'Tune',
        null=True,
        blank=True,
        related_name='catalogs',
    )

    song_name = models.CharField(
        blank=True,
        max_length=200,
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

    bhs_difficulty = models.IntegerField(
        null=True,
        blank=True,
        choices=DIFFICULTY
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


class Contest(models.Model):

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'structured', 'Structured',),
        (15, 'ready', 'Ready',),
        (20, 'current', 'Current',),
        (25, 'review', 'Review',),
        (30, 'complete', 'Complete',),
    )

    HISTORY = Choices(
        (0, 'new', 'New',),
        (10, 'none', 'None',),
        (20, 'pdf', 'PDF',),
        (30, 'places', 'Places',),
        (40, 'incomplete', 'Incomplete',),
        (50, 'complete', 'Complete',),
    )

    YEAR_CHOICES = []
    for r in reversed(range(1939, (datetime.datetime.now().year + 2))):
        YEAR_CHOICES.append((r, r))

    ROUNDS_CHOICES = []
    for r in reversed(range(1, 4)):
        ROUNDS_CHOICES.append((r, r))

    PANEL_CHOICES = []
    for r in reversed(range(1, 6)):
        PANEL_CHOICES.append((r, r))

    KIND = Choices(
        (1, 'quartet', 'Quartet',),
        (2, 'chorus', 'Chorus',),
        (3, 'senior', 'Senior',),
        (4, 'collegiate', 'Collegiate',),
    )

    LEVEL = Choices(
        (1, 'international', "International"),
        (2, 'district', "District"),
        (3, 'division', "Division"),
    )

    GOAL = Choices(
        (1, 'championship', "Championship"),
        (2, 'prelims', "Prelims"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the contest (determined programmatically.)""",
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

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    history = models.IntegerField(
        choices=HISTORY,
        default=HISTORY.new,
    )

    history_monitor = MonitorField(
        help_text="""History last updated""",
        monitor='history',
    )

    organization = models.ForeignKey(
        'Organization',
        related_name='contests',
    )

    level = models.IntegerField(
        # help_text="""
        #     The level of the contest (currently only International is supported.)""",
        choices=LEVEL,
        # default=LEVEL.international,
    )

    kind = models.IntegerField(
        # help_text="""
        #     The kind of the contest (quartet, chorus, senior, collegiate.)""",
        choices=KIND,
        # default=KIND.quartet,
    )

    goal = models.IntegerField(
        help_text="""
            The objective of the contest""",
        choices=GOAL,
        # default=GOAL.championship,
    )

    year = models.IntegerField(
        default=datetime.datetime.now().year,
        choices=YEAR_CHOICES,
    )

    convention = models.ForeignKey(
        'Convention',
        help_text="""
            The convention at which this contest occurred.""",
        related_name='contests',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    panel = models.IntegerField(
        help_text="""
            Size of the judging panel (typically three or five.)""",
        choices=PANEL_CHOICES,
        # default=5,
    )

    rounds = models.IntegerField(
        help_text="""
            Bracket size""",
        choices=ROUNDS_CHOICES,
        # default=1,
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

    class Meta:
        unique_together = (
            ('level', 'kind', 'year', 'goal', 'organization'),
        )
        ordering = (
            'level',
            '-year',
            'kind',
        )

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "name__icontains",)

    # TODO
    # def clean(self):
    #         if self.level == self.LEVEL.international and self.district.name != 'BHS':
    #             raise ValidationError('International does not have a district.')
    #         if self.level != self.LEVEL.international and self.district is None:
    #             raise ValidationError('You must provide a district.')

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2} {3} {4}".format(
            self.organization,
            self.get_level_display(),
            self.get_kind_display(),
            self.get_goal_display(),
            self.year,
        )
        super(Contest, self).save(*args, **kwargs)

    def build_contest(self):
        """
            Return sentinels for juding panel.
        """
        r = 1
        while r <= self.rounds:
            self.sessions.create(
                contest=self,
                kind=r,
            )
            r += 1

        s = 1
        while s <= self.panel:
            self.judges.create(
                contest=self,
                category=1,
                slot=s,
            )
            self.judges.create(
                contest=self,
                category=2,
                slot=s,
            )
            self.judges.create(
                contest=self,
                category=3,
                slot=s,
            )
            s += 1
        self.status = self.STATUS.structured
        self.save()

    def draw_contest(self):
        cs = self.contestants.order_by('?')
        session = self.sessions.get(kind=self.rounds)
        p = 0
        for c in cs:
            session.performances.create(
                contestant=c,
                position=p,
                start=session.start,
            )
            p += 1
        self.status = self.STATUS.ready
        self.save()

    def start_contest(self):
        # Start first session.
        session = self.sessions.get(kind=self.rounds)
        session.start_session()
        self.status = self.STATUS.current
        contestants = self.contestants.all()
        for contestant in contestants:
            contestant.status = contestant.STATUS.current
        self.save()
        return "Contest Started"

    def end_contest(self):
        cursor = []
        i = 1
        # TODO rescore
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
        if self.goal == self.GOAL.championship:
            Winner.objects.create(
                contestant=self.contestants.get(place=1),
                award=Award.objects.get(
                    name='Champion',
                ),
                contest=self,
            )
        self.status = self.STATUS.review
        self.save()

        # TODO Confer awards
        return "Contest Ended"

    def confirm_contest(self):
        # Validation logic
        self.status = self.STATUS.complete
        self.save()
        return "Contest Confirmed"

    def seed(self):
        marker = []
        i = 1
        for contestant in self.contestants.order_by('-prelim'):
            try:
                match = contestant.prelim == marker[0].prelim
            except IndexError:
                contestant.seed = i
                contestant.save()
                marker.append(contestant)
                continue
            if match:
                contestant.seed = i
                i += len(marker)
                contestant.save()
                marker.append(contestant)
                continue
            else:
                i += 1
                contestant.seed = i
                contestant.save()
                marker = [contestant]
        return


class Contestant(models.Model):

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'ready', 'Ready',),
        (20, 'current', 'Current',),
        (30, 'complete', 'Complete',),
    )

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

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    contest = models.ForeignKey(
        'Contest',
        related_name='contestants',
    )

    group = models.ForeignKey(
        'Group',
        related_name='contestants',
    )

    organization = models.ForeignKey(
        'Organization',
        # help_text="""
        #     The district this contestant is representing.""",
        related_name='contestants',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    picture = models.ImageField(
        # help_text="""
        #     The song picture (as opposed to the "official" photo).""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    seed = models.IntegerField(
        # help_text="""
        #     The incoming rank based on prelim score.""",
        null=True,
        blank=True,
    )

    prelim = models.FloatField(
        # help_text="""
        #     The incoming prelim score.""",
        null=True,
        blank=True,
    )

    # TODO Everything below here must be protected in some way.  Different model?
    place = models.IntegerField(
        # help_text="""
        #     The final placement/rank of the contestant.""",
        null=True,
        blank=True,
    )

    men = models.IntegerField(
        # help_text="""
        #     The number of men on stage (only for chourses).""",
        default=4,
        null=True,
        blank=True,
    )

    mus_points = models.IntegerField(
        # help_text="""
        #     The total music points for this performance.""",
        null=True,
        blank=True,
        editable=False,
    )

    prs_points = models.IntegerField(
        # help_text="""
        #     The total presentation points for this performance.""",
        null=True,
        editable=False,
        blank=True,
    )

    sng_points = models.IntegerField(
        # help_text="""
        #     The total singing points for this performance.""",
        null=True,
        blank=True,
        editable=False,
    )

    total_points = models.IntegerField(
        # help_text="""
        #     The total points for this performance.""",
        null=True,
        blank=True,
        editable=False,
    )

    mus_score = models.FloatField(
        # help_text="""
        #     The percentile music score for this performance.""",
        null=True,
        blank=True,
        editable=False,
    )

    prs_score = models.FloatField(
        # help_text="""
        #     The percentile presentation score for this performance.""",
        null=True,
        blank=True,
        editable=False,
    )

    sng_score = models.FloatField(
        # help_text="""
        #     The percentile singing score for this performance.""",
        null=True,
        blank=True,
        editable=False,
    )

    total_score = models.FloatField(
        # help_text="""
        #     The total percentile score for this performance.""",
        null=True,
        blank=True,
        editable=False,
    )

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "name__icontains",)

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1}".format(
            self.contest,
            self.group,
        )

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
                possible = self.contest.panel * 2 * self.performances.count()
                self.mus_score = round(self.mus_points / possible, 1)
                self.prs_score = round(self.prs_points / possible, 1)
                self.sng_score = round(self.sng_points / possible, 1)
                self.total_score = round(self.total_points / (possible * 3), 1)
            except TypeError:
                self.mus_score = None
                self.prs_score = None
                self.sng_score = None
        super(Contestant, self).save(*args, **kwargs)

    @property
    def delta_score(self):
        try:
            return self.total_score - self.prelim
        except TypeError:
            return None

    @property
    def delta_place(self):
        try:
            return self.seed - self.place
        except TypeError:
            return None

    # @staticmethod
    # def autocomplete_search_fields():
    #     return ("name__icontains",)

    class Meta:
        ordering = (
            '-contest__year',
            'place',
        )
        unique_together = (
            ('group', 'contest',),
        )

    def clean(self):
        if self.singers.count() > 4:
            raise ValidationError('There can not be more than four persons in a quartet.')

    def denorm(self):
        ps = self.performances.all()
        for p in ps:
            songs = p.songs.all()
            for song in songs:
                song.save()
            p.save()
        self.save()
        return "De-normalized record"


class Convention(models.Model):
    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'structured', 'Structured',),
        (20, 'current', 'Current',),
        (30, 'complete', 'Complete',),
    )

    KIND = Choices(
        (1, 'international', 'International',),
        (2, 'midwinter', 'Midwinter',),
        (3, 'fall', 'Fall',),
        (4, 'spring', 'Spring',),
        (5, 'pacific', 'Pacific',),
    )

    YEAR_CHOICES = []
    for r in reversed(range(1939, (datetime.datetime.now().year + 2))):
        YEAR_CHOICES.append((r, r))

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the convention (determined programmatically.)""",
        max_length=200,
        unique=True,
    )

    status = models.IntegerField(
        help_text="""The current status""",
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    kind = models.IntegerField(
        help_text="""
            The kind of convention.""",
        choices=KIND,
    )

    year = models.IntegerField(
        default=datetime.datetime.now().year,
        choices=YEAR_CHOICES,
    )

    organization = models.ForeignKey(
        'Organization',
        help_text="""
            The district for the convention.  If International, this is 'BHS'.""",
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    dates = models.CharField(
        help_text="""
            The convention dates (will be replaced by start/end).""",
        max_length=200,
        blank=True,
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

    class Meta:
        ordering = [
            'organization',
            '-year',
        ]

        unique_together = (
            ('organization', 'kind', 'year',),
        )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2}".format(
            self.organization,
            self.get_kind_display(),
            self.year,
        )
        super(Convention, self).save(*args, **kwargs)


class Director(models.Model):
    """Chorus relation"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    PART = Choices(
        (1, 'director', 'Director'),
        (2, 'codirector', 'Co-Director'),
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

    contestant = models.ForeignKey(
        'Contestant',
        related_name='directors',
    )

    person = models.ForeignKey(
        'Person',
        related_name='choruses',
    )

    part = models.IntegerField(
        choices=PART,
        default=PART.director,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2}".format(
            self.contestant,
            self.get_part_display(),
            self.person,
        )
        super(Director, self).save(*args, **kwargs)

    def clean(self):
        if self.contestant.group.kind == Group.KIND.quartet:
            raise ValidationError('Quartets do not have directors.')

    class Meta:
        unique_together = (
            ('contestant', 'person',),
        )


class Group(Common):

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'inactive', 'Inactive',),
    )

    KIND = Choices(
        (1, 'quartet', 'Quartet'),
        (2, 'chorus', 'Chorus'),
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    kind = models.IntegerField(
        help_text="""
            The kind of group; choices are Quartet or Chorus.""",
        choices=KIND,
        default=KIND.quartet,
    )

    chapter_name = models.CharField(
        help_text="""
            The chapter name (only for choruses).""",
        max_length=200,
        blank=True,
    )

    chapter_code = models.CharField(
        help_text="""
            The chapter code (only for choruses).""",
        max_length=200,
        blank=True,
    )

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "name__icontains",)

    def __unicode__(self):
        return u"{0}".format(self.name)

    def clean(self):
        if self.kind == self.KIND.quartet and self.chapter_name:
            raise ValidationError(
                {'chapter_name': 'Chapter names are only for choruses.'}
            )
        if self.kind == self.KIND.quartet and self.chapter_code:
            raise ValidationError(
                {'chapter_code': 'Chapter codes are only for choruses.'}
            )

    class Meta:
        ordering = (
            'name',
        )

    fuzzy = models.TextField(
        blank=True,
    )


class JudgeQuerySet(QuerySet):
    def composite(self):
        return self.filter(category__in=[7, 8, 9])

    def practice(self):
        return self.filter(category__in=[4, 5, 6])

    def scoring(self):
        return self.filter(category__in=[1, 2, 3])

    def administrator(self):
        return self.filter(category=0)

    def contest(self):
        return self.filter(category__in=[0, 1, 2, 3])


class Judge(models.Model):
    """Contest Judge"""

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'scheduled', 'Scheduled',),
        (20, 'confirmed', 'Confirmed',),
        (30, 'complete', 'Complete',),
    )

    SLOT_CHOICES = []
    for r in range(1, 6):
        SLOT_CHOICES.append((r, r))

    CATEGORY = Choices(
        (0, 'admin', 'Admin'),
        (1, 'music', 'Music'),
        (2, 'presentation', 'Presentation'),
        (3, 'singing', 'Singing'),
        (4, 'music_candidate', 'Music Candidate'),
        (5, 'presentation_candidate', 'Presentation Candidate'),
        (6, 'singing_candidate', 'Singing Candidate'),
        (7, 'music_composite', 'Music Composite'),
        (8, 'presentation_composite', 'Presentation Composite'),
        (9, 'singing_composite', 'Singing Composite'),
    )

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

    contest = models.ForeignKey(
        'Contest',
        related_name='judges',
    )

    person = models.ForeignKey(
        'Person',
        related_name='panels',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    category = models.IntegerField(
        choices=CATEGORY,
        null=True,
        blank=True,
    )

    slot = models.IntegerField(
        choices=SLOT_CHOICES,
        null=True,
        blank=True,
    )

    organization = models.ForeignKey(
        'Organization',
        related_name='judges',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    is_practice = models.BooleanField(
        default=False,
    )

    objects = PassThroughManager.for_queryset_class(JudgeQuerySet)()

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "name__icontains", "person__icontains",)

    @property
    def designation(self):
        return u"{0[0]}-{1:02d}".format(
            self.get_category_display(),
            self.slot,
        )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} Judge {1}{2}".format(
            self.contest,
            self.category,
            self.slot,
        )
        super(Judge, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('contest', 'category', 'slot'),
        )
        ordering = (
            'contest',
            'category',
            'slot',
        )


class Organization(MPTTModel, Common):
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
    )

    class MPTTMeta:
        order_insertion_by = [
            'name',
        ]

    def __unicode__(self):
        return u"{0}".format(self.name)


class Performance(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'structured', 'Structured',),
        (15, 'ready', 'Ready',),
        (20, 'current', 'Current',),
        (25, 'review', 'Review',),
        (30, 'complete', 'Complete',),
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

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    session = models.ForeignKey(
        'Session',
        related_name='performances',
    )

    contestant = models.ForeignKey(
        'Contestant',
        related_name='performances',
    )

    position = models.PositiveSmallIntegerField(
        'Position',
    )

    place = models.IntegerField(
        null=True,
        blank=True,
    )

    start = models.DateTimeField(
        null=True,
        blank=True,
    )

    # The following need to be protected until released.
    # Different model?

    mus_points = models.IntegerField(
        # help_text="""
        #     The total music points for this performance.""",
        null=True,
        blank=True,
        editable=False,
    )

    prs_points = models.IntegerField(
        # help_text="""
        #     The total presentation points for this performance.""",
        null=True,
        blank=True,
        editable=False,
    )

    sng_points = models.IntegerField(
        # help_text="""
        #     The total singing points for this performance.""",
        null=True,
        blank=True,
        editable=False,
    )

    total_points = models.IntegerField(
        # help_text="""
        #     The total points for this performance.""",
        null=True,
        blank=True,
        editable=False,
    )

    mus_score = models.FloatField(
        # help_text="""
        #     The percentile music score for this performance.""",
        null=True,
        blank=True,
        editable=False,
    )

    prs_score = models.FloatField(
        # help_text="""
        #     The percentile presentation score for this performance.""",
        null=True,
        blank=True,
        editable=False,
    )

    sng_score = models.FloatField(
        # help_text="""
        #     The percentile singing score for this performance.""",
        null=True,
        blank=True,
        editable=False,
    )

    total_score = models.FloatField(
        # help_text="""
        #     The total percentile score for this performance.""",
        null=True,
        blank=True,
        editable=False,
    )

    penalty = models.TextField(
        help_text="""
            Free form for penalties (notes).""",
        blank=True,
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

    def start_performance(self):
        self.status = self.STATUS.current
        self.save()

    def end_performance(self):
        result = dixon(self)
        self.status = self.STATUS.review
        self.save()
        return result

    def confirm_performance(self):
        self.status = self.STATUS.complete
        self.save()

    class Meta:
        ordering = [
            'session',
            'position',
        ]
        # unique_together = (
        #     ('contestant', 'kind',),
        # )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1}".format(
            self.session,
            self.contestant.group,
        )

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

            #  Calculate percentile scores
            try:
                possible = self.contestant.contest.panel * 2
                self.mus_score = round(self.mus_points / possible, 1)
                self.prs_score = round(self.prs_points / possible, 1)
                self.sng_score = round(self.sng_points / possible, 1)
                self.total_score = round(self.total_points / (possible * 3), 1)
            except TypeError:
                self.mus_score = None
                self.prs_score = None
                self.sng_score = None
        super(Performance, self).save(*args, **kwargs)


class Person(Common):

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'inactive', 'Inactive',),
        (30, 'retired', 'Retired',),
        (40, 'deceased', 'Deceased',),
    )

    KIND = Choices(
        (1, 'individual', "Individual"),
        (2, 'team', "Team"),
    )

    kind = models.IntegerField(
        help_text="""
            Most persons are individuals; however, they can be grouped into teams for the purpose of multi-arranger songs.""",
        choices=KIND,
        default=KIND.individual,
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u"{0}".format(self.name)

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

    fuzzy = models.TextField(
        blank=True,
    )


class Score(models.Model):
    """
        The Score is never released publicly.  These are the actual
        Judge's scores from the contest.
    """
    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'flagged', 'Flagged',),
        (20, 'passed', 'Passed',),
        (30, 'complete', 'Complete',),
    )

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

    status = models.IntegerField(
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
        null=True,
        blank=True,
    )

    judge = models.ForeignKey(
        'Judge',
        related_name='scores',
    )

    points = models.IntegerField(
        help_text="""
            The number of points awarded (0-100)""",
        null=True,
        blank=True,
        # validators=[
        #     MaxValueValidator(
        #         100,
        #         message='Points must be between 0 - 100',
        #     ),
        #     MinValueValidator(
        #         0,
        #         message='Points must be between 0 - 100',
        #     ),
        # ]
    )

    class Meta:
        ordering = (
            'judge',
            'song__order',
        )

    @property
    def category(self):
        return self.judge.get_category_display()

    @property
    def is_practice(self):
        return self.judge.is_practice

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2:02d}".format(
            self.song,
            self.judge.get_category_display(),
            self.judge.slot,
        )
        super(Score, self).save(*args, **kwargs)


class Session(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'structured', 'Structured',),
        (15, 'ready', 'Ready',),
        (20, 'current', 'Current',),
        (25, 'review', 'Review',),
        (30, 'complete', 'Complete',),
    )

    KIND = Choices(
        (1, 'finals', 'Finals'),
        (2, 'semis', 'Semis'),
        (3, 'quarters', 'Quarters'),
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

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    contest = models.ForeignKey(
        'Contest',
        related_name='sessions',
    )

    kind = models.IntegerField(
        choices=KIND,
        default=KIND.finals,
    )

    start = models.DateField(
        null=True,
        blank=True,
    )

    slots = models.IntegerField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = [
            'contest',
            'kind',
        ]
        unique_together = (
            ('contest', 'kind',),
        )

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "name__icontains",)

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1}".format(
            self.contest,
            self.get_kind_display(),
        )
        super(Session, self).save(*args, **kwargs)

    def build_session(self):
        """
            Return sentinels for contestants.
        """
        s = 0
        while s < self.session.slots:
            self.session.performances.create(
                session=self.session,
                position=s,
                start=self.session.start,
            )
            s += 1

    def start_session(self):
        ls = self.performances.all()
        for l in ls:
            p1 = l.songs.create(performance=l, order=1)
            p2 = l.songs.create(performance=l, order=2)
            for j in self.contest.judges.scoring():
                p1.scores.create(
                    song=p1,
                    judge=j,
                )
                p2.scores.create(
                    song=p2,
                    judge=j,
                )
        performance = self.performances.get(position=0)
        performance.start_performance()
        self.status = self.STATUS.current
        self.save()
        return "Session Started"

    def end_session(self):
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
        self.status = self.STATUS.review
        self.save()
        return "Session Ended"

    def confirm_session(self):
        # TODO Some validation
        try:
            # TODO This is an awful lot to be in a try/except; refactor?
            next_session = self.contest.sessions.get(
                kind=(self.kind - 1),
            )
            qualifiers = self.performances.filter(
                place__lte=next_session.slots,
            ).order_by('?')
            p = 0
            for qualifier in qualifiers:
                l = next_session.performances.create(
                    contestant=qualifier.contestant,
                    position=p,
                    start=next_session.start,
                )
                p += 1
                p1 = l.songs.create(performance=l, order=1)
                p2 = l.songs.create(performance=l, order=2)
                for j in self.contest.judges.scoring():
                    p1.scores.create(
                        song=p1,
                        judge=j,
                    )
                    p2.scores.create(
                        song=p2,
                        judge=j,
                    )
        except self.DoesNotExist:
            pass
        self.status = self.STATUS.complete
        self.save()
        return 'Session Confirmed'


class Singer(models.Model):
    """Quartet Relation"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    PART = Choices(
        (1, 'tenor', 'Tenor'),
        (2, 'lead', 'Lead'),
        (3, 'baritone', 'Baritone'),
        (4, 'bass', 'Bass'),
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

    contestant = models.ForeignKey(
        'Contestant',
        related_name='singers',
    )

    person = models.ForeignKey(
        'Person',
        related_name='quartets',
    )

    part = models.IntegerField(
        choices=PART,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2}".format(
            self.contestant,
            self.get_part_display(),
            self.person,
        )
        super(Singer, self).save(*args, **kwargs)

    def clean(self):
        # if self.contestant.group.kind == Group.CHORUS:
        #     raise ValidationError('Choruses do not have quartet singers.')
        if self.part:
            if [s['part'] for s in self.contestant.singers.values(
                'part'
            )].count(self.part) > 1:
                raise ValidationError('There can not be more than one of the same part in a quartet.')

    class Meta:
        unique_together = (
            ('contestant', 'person',),
        )
        ordering = (
            '-name',
        )


class Song(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'flagged', 'Flagged',),
        (20, 'passed', 'Passed',),
        (30, 'complete', 'Complete',),
    )

    ORDER = Choices(
        (1, 'first', 'First'),
        (2, 'second', 'Second'),
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

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    performance = models.ForeignKey(
        'Performance',
        related_name='songs',
        null=True,
        blank=True,
    )

    order = models.IntegerField(
        choices=ORDER,
    )

    is_parody = models.BooleanField(
        default=False,
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

    # The following need to be protected until released.
    # Different model?

    title = models.CharField(
        max_length=255,
        blank=True,
        editable=False,
    )

    arranger = models.CharField(
        max_length=255,
        blank=True,
        editable=False,
    )

    mus_points = models.IntegerField(
        # help_text="""
        #     The total music points for this song.""",
        null=True,
        blank=True,
        editable=False,
    )

    prs_points = models.IntegerField(
        # help_text="""
        #     The total presentation points for this song.""",
        null=True,
        blank=True,
        editable=False,
    )

    sng_points = models.IntegerField(
        # help_text="""
        #     The total singing points for this song.""",
        null=True,
        blank=True,
        editable=False,
    )

    total_points = models.IntegerField(
        # help_text="""
        #     The total points for this song.""",
        null=True,
        blank=True,
        editable=False,
    )

    mus_score = models.FloatField(
        # help_text="""
        #     The percentile music score for this song.""",
        null=True,
        blank=True,
        editable=False,
    )

    prs_score = models.FloatField(
        # help_text="""
        #     The percentile presentation score for this song.""",
        null=True,
        blank=True,
        editable=False,
    )

    sng_score = models.FloatField(
        # help_text="""
        #     The percentile singing score for this song.""",
        null=True,
        blank=True,
        editable=False,
    )

    total_score = models.FloatField(
        # help_text="""
        #     The total percentile score for this song.""",
        null=True,
        blank=True,
        editable=False,
    )

    penalty = models.TextField(
        help_text="""
            Free form for penalties (notes).""",
        blank=True,
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
            self.get_order_display(),
            "Tune",
        )

        if self.catalog:
            self.title = self.catalog.song_name
            self.arranger = ", ".join(
                [l['person__name'] for l in self.catalog.arrangers.values('person__name')]
            )

        if self.scores.exists():
            self.mus_points = self.scores.filter(
                judge__category__in=[1, 7]
            ).aggregate(mus=models.Sum('points'))['mus']
            self.prs_points = self.scores.filter(
                judge__category__in=[2, 8]
            ).aggregate(prs=models.Sum('points'))['prs']
            self.sng_points = self.scores.filter(
                judge__category__in=[3, 9]
            ).aggregate(sng=models.Sum('points'))['sng']

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
            possible = self.performance.contestant.contest.panel
            self.mus_score = round(self.mus_points / possible, 1)
            self.prs_score = round(self.prs_points / possible, 1)
            self.sng_score = round(self.sng_points / possible, 1)
            self.total_score = round(self.total_points / (possible * 3), 1)
        except TypeError:
            self.mus_score = None
            self.prs_score = None
            self.sng_score = None
        super(Song, self).save(*args, **kwargs)


class Tune(models.Model):
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

    fuzzy = models.TextField(
        blank=True,
    )


class Winner(models.Model):
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

    contestant = models.ForeignKey(
        'Contestant',
        related_name='winners',
    )

    award = models.ForeignKey(
        'Award',
        related_name='winners',
    )

    contest = models.ForeignKey(
        'Contest',
        related_name='winners',
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1}".format(
            self.contestant,
            self.award,
        )
        super(Winner, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('contestant', 'award',),
        )


class UserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        user = self.model(
            email=self.normalize_email(email),
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(
            email=email,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


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
