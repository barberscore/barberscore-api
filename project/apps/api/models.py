from __future__ import division

import logging
log = logging.getLogger(__name__)

import uuid

import os
import datetime

from django.db import (
    models,
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


class Appearance(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (1, 'qualified', 'Qualified',),
        (2, 'current', 'Current',),
        (3, 'complete', 'Complete',),
        (4, 'flagged', 'Flagged',),
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
        related_name='appearances',
    )

    contestant = models.ForeignKey(
        'Contestant',
        related_name='appearances',
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
        #     The total music points for this appearance.""",
        null=True,
        blank=True,
    )

    prs_points = models.IntegerField(
        # help_text="""
        #     The total presentation points for this appearance.""",
        null=True,
        blank=True,
    )

    sng_points = models.IntegerField(
        # help_text="""
        #     The total singing points for this appearance.""",
        null=True,
        blank=True,
    )

    total_points = models.IntegerField(
        # help_text="""
        #     The total points for this appearance.""",
        null=True,
        blank=True,
    )

    mus_score = models.FloatField(
        # help_text="""
        #     The percentile music score for this appearance.""",
        null=True,
        blank=True,
    )

    prs_score = models.FloatField(
        # help_text="""
        #     The percentile presentation score for this appearance.""",
        null=True,
        blank=True,
    )

    sng_score = models.FloatField(
        # help_text="""
        #     The percentile singing score for this appearance.""",
        null=True,
        blank=True,
    )

    total_score = models.FloatField(
        # help_text="""
        #     The total percentile score for this appearance.""",
        null=True,
        blank=True,
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

        # Don't bother if there aren't performance scores.
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
        super(Appearance, self).save(*args, **kwargs)


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

    performance = models.ForeignKey(
        'Performance',
        related_name='arrangers',
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
        self.name = u"{0} {1} {2}".format(
            self.performance,
            self.get_part_display(),
            self.person,
        )
        super(Arranger, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('performance', 'person',),
        )


class Award(models.Model):

    KIND = Choices(
        (1, 'first', 'First Place Gold Medalist'),
        (2, 'second', 'Second Place Silver Medalist'),
        (3, 'third', 'Third Place Bronze Medalist'),
        (4, 'fourth', 'Fourth Place Bronze Medalist'),
        (5, 'fifth', 'Fifth Place Bronze Medalist'),
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

    kind = models.IntegerField(
        choices=KIND,
    )

    contestant = models.ForeignKey(
        'Contestant',
        related_name='awards',
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1}".format(
            self.contestant,
            self.get_kind_display(),
        )
        super(Award, self).save(*args, **kwargs)

    class Meta:
        ordering = (
            'name',
        )

        unique_together = (
            ('kind', 'contestant',),
        )


class Catalog(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

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

    song = models.ForeignKey(
        'Song',
        null=True,
        blank=True,
        related_name='catalogs',
    )

    person = models.ForeignKey(
        'Person',
        null=True,
        blank=True,
        related_name='catalogs',
    )

    song_match = models.CharField(
        blank=True,
        max_length=200,
    )

    name = models.CharField(
        max_length=200,
        unique=True,
    )

    person_match = models.CharField(
        blank=True,
        max_length=200,
    )

    fuzzy = models.TextField(
        blank=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    class Meta:
        unique_together = (
            ('person', 'song')
        )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} [{1}]".format(
            self.song,
            self.person,
        )
        super(Catalog, self).save(*args, **kwargs)


class Contest(models.Model):

    STATUS = Choices(
        (0, 'new', 'New',),
        (1, 'structured', 'Structured',),
        (2, 'current', 'Current',),
        (3, 'complete', 'Complete',),
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

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    name = models.CharField(
        help_text="""
            The name of the contest (determined programmatically.)""",
        max_length=200,
        unique=True,
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

    level = models.IntegerField(
        # help_text="""
        #     The level of the contest (currently only International is supported.)""",
        choices=LEVEL,
        default=LEVEL.international,
    )

    kind = models.IntegerField(
        # help_text="""
        #     The kind of the contest (quartet, chorus, senior, collegiate.)""",
        choices=KIND,
        default=KIND.quartet,
    )

    year = models.IntegerField(
        default=datetime.datetime.now().year,
        choices=YEAR_CHOICES,
    )

    organization = models.ForeignKey(
        'Organization',
        null=True,
        blank=True,
        related_name='contests',
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
        default=5,
        choices=PANEL_CHOICES,
        null=True,
        blank=True,
    )

    rounds = models.IntegerField(
        help_text="""
            Bracket size""",
        default=5,
        choices=ROUNDS_CHOICES,
    )

    goal = models.IntegerField(
        help_text="""
            The objective of the contest""",
        default=GOAL.championship,
        choices=GOAL,
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
        if self.level == self.LEVEL.international:
            self.name = u"{0} {1} {2} {3}".format(
                self.get_level_display(),
                self.get_kind_display(),
                self.get_goal_display(),
                self.year,
            )
        elif self.level == self.LEVEL.district:
            self.name = u"{0} {1} {2} {3} {4}".format(
                self.organization,
                self.get_level_display(),
                self.get_kind_display(),
                self.get_goal_display(),
                self.year,
            )
        else:
            self.name = u"{0} {1} {2} {3} {4}".format(
                'Unknown',
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

    def draw_contest(self):
        cs = self.contestants.order_by('?')
        session = self.sessions.get(kind=self.rounds)
        p = 0
        for c in cs:
            session.appearances.create(
                contestant=c,
                position=p,
                start=session.start,
            )
            p += 1

    def start_contest(self):
        session = self.sessions.get(kind=self.rounds)
        ls = session.appearances.all()
        for l in ls:
            p1 = l.performances.create(appearance=l, order=1)
            p2 = l.performances.create(appearance=l, order=2)
            for j in self.judges.filter(category__in=[1, 2, 3]):
                p1.scores.create(
                    performance=p1,
                    judge=j,
                )
                p2.scores.create(
                    performance=p2,
                    judge=j,
                )

    def promote_contest(self):
        current_session = self.sessions.get(
            status=self.sessions.model.STATUS.current,
        )
        next_session = self.sessions.get(
            kind=(current_session.kind - 1),
        )
        qualifiers = current_session.appearances.filter(
            place__lte=next_session.slots,
        ).order_by('?')
        p = 0
        for qualifier in qualifiers:
            l = next_session.appearances.create(
                contestant=qualifier.contestant,
                position=p,
                start=next_session.start,
            )
            p += 1
            p1 = l.performances.create(appearance=l, order=1)
            p2 = l.performances.create(appearance=l, order=2)
            for j in self.judges.filter(category__in=[1, 2, 3]):
                p1.scores.create(
                    performance=p1,
                    judge=j,
                )
                p2.scores.create(
                    performance=p2,
                    judge=j,
                )

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
        (1, 'qualified', 'Qualified',),
        (2, 'current', 'Current',),
        (3, 'complete', 'Complete',),
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
        #     The performance picture (as opposed to the "official" photo).""",
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
        #     The total music points for this appearance.""",
        null=True,
        blank=True,
    )

    prs_points = models.IntegerField(
        # help_text="""
        #     The total presentation points for this appearance.""",
        null=True,
        blank=True,
    )

    sng_points = models.IntegerField(
        # help_text="""
        #     The total singing points for this appearance.""",
        null=True,
        blank=True,
    )

    total_points = models.IntegerField(
        # help_text="""
        #     The total points for this appearance.""",
        null=True,
        blank=True,
    )

    mus_score = models.FloatField(
        # help_text="""
        #     The percentile music score for this appearance.""",
        null=True,
        blank=True,
    )

    prs_score = models.FloatField(
        # help_text="""
        #     The percentile presentation score for this appearance.""",
        null=True,
        blank=True,
    )

    sng_score = models.FloatField(
        # help_text="""
        #     The percentile singing score for this appearance.""",
        null=True,
        blank=True,
    )

    total_score = models.FloatField(
        # help_text="""
        #     The total percentile score for this appearance.""",
        null=True,
        blank=True,
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

        # If there are no appearances, skip.
        if self.appearances.exists():
            agg = self.appearances.all().aggregate(
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
                possible = self.contest.panel * 2 * self.appearances.count()
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


class Convention(models.Model):
    STATUS = Choices(
        (0, 'new', 'New',),
        (1, 'structured', 'Structured',),
        (2, 'current', 'Current',),
        (3, 'complete', 'Complete',),
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
        null=True,
        blank=True,
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
        if self.kind in [
            self.KIND.international,
            self.KIND.midwinter,
            self.KIND.pacific,
        ]:
            self.name = u"{0} {1}".format(
                self.get_kind_display(),
                self.year,
            )
        else:
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

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "name__icontains", "person__icontains",)

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
        (1, 'ready', 'Ready',),
        (2, 'current', 'Current',),
        (3, 'complete', 'Complete',),
        (4, 'flagged', 'Flagged',),
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

    appearance = models.ForeignKey(
        'Appearance',
        related_name='performances',
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
        related_name='performances',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    song = models.ForeignKey(
        'Song',
        related_name='performances',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # The following need to be protected until released.
    # Different model?

    mus_points = models.IntegerField(
        # help_text="""
        #     The total music points for this performance.""",
        null=True,
        blank=True,
    )

    prs_points = models.IntegerField(
        # help_text="""
        #     The total presentation points for this performance.""",
        null=True,
        blank=True,
    )

    sng_points = models.IntegerField(
        # help_text="""
        #     The total singing points for this performance.""",
        null=True,
        blank=True,
    )

    total_points = models.IntegerField(
        # help_text="""
        #     The total points for this performance.""",
        null=True,
        blank=True,
    )

    mus_score = models.FloatField(
        # help_text="""
        #     The percentile music score for this performance.""",
        null=True,
        blank=True,
    )

    prs_score = models.FloatField(
        # help_text="""
        #     The percentile presentation score for this performance.""",
        null=True,
        blank=True,
    )

    sng_score = models.FloatField(
        # help_text="""
        #     The percentile singing score for this performance.""",
        null=True,
        blank=True,
    )

    total_score = models.FloatField(
        # help_text="""
        #     The total percentile score for this performance.""",
        null=True,
        blank=True,
    )

    penalty = models.TextField(
        help_text="""
            Free form for penalties (notes).""",
        blank=True,
    )

    class Meta:
        ordering = [
            'appearance',
            'order',
        ]
        unique_together = (
            ('appearance', 'order',),
        )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2}".format(
            self.appearance,
            self.get_order_display(),
            "Song",
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
            possible = self.appearance.contestant.contest.panel
            self.mus_score = round(self.mus_points / possible, 1)
            self.prs_score = round(self.prs_points / possible, 1)
            self.sng_score = round(self.sng_points / possible, 1)
            self.total_score = round(self.total_points / (possible * 3), 1)
        except TypeError:
            self.mus_score = None
            self.prs_score = None
            self.sng_score = None
        super(Performance, self).save(*args, **kwargs)

    def dixon_test(self):
        return dixon(self.scores.all())


class Person(Common):

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
        (1, 'flagged', 'Flagged',),
        (2, 'confirmed', 'Confirmed',),
        (3, 'final', 'Final',),
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

    performance = models.ForeignKey(
        'Performance',
        related_name='scores',
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
            'performance__order',
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
            self.performance,
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
        (1, 'structured', 'Structured',),
        (2, 'current', 'Current',),
        (3, 'complete', 'Complete',),
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
            self.session.appearances.create(
                session=self.session,
                position=s,
                start=self.session.start,
            )
            s += 1

    def place_session(self):
        cursor = []
        i = 1
        for appearance in self.appearances.order_by('-total_points'):
            try:
                match = appearance.total_points == cursor[0].total_points
            except IndexError:
                appearance.place = i
                appearance.save()
                cursor.append(appearance)
                continue
            if match:
                appearance.place = i
                i += len(cursor)
                appearance.save()
                cursor.append(appearance)
                continue
            else:
                i += 1
                appearance.place = i
                appearance.save()
                cursor = [appearance]
        return


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


class DuplicateGroup(models.Model):
    parent = models.ForeignKey(
        Group,
        related_name='duplicates',
    )
    child = models.ForeignKey(
        Group,
        related_name='children',
    )
    score = models.IntegerField(
    )


class DuplicateSong(models.Model):
    parent = models.ForeignKey(
        Song,
        related_name='duplicates',
    )
    child = models.ForeignKey(
        Song,
        related_name='children',
    )
    score = models.IntegerField(
    )


class DuplicatePerson(models.Model):
    parent = models.ForeignKey(
        Person,
        related_name='duplicates',
    )
    child = models.ForeignKey(
        Person,
        related_name='children',
    )
    score = models.IntegerField(
    )
