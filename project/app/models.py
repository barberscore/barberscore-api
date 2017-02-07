# Future
from __future__ import division

# Standard Libary
import datetime
import logging
import os
import random
import uuid

# Third-Party
import docraptor
from django_fsm import (
    RETURN_VALUE,
    FSMIntegerField,
    transition,
)
from dry_rest_permissions.generics import allow_staff_or_superuser
from model_utils import Choices
from model_utils.models import TimeStampedModel
from mptt.models import (
    MPTTModel,
    TreeForeignKey,
)
from nameparser import HumanName
from ranking import Ranking
from timezone_field import TimeZoneField

# Django
from django.apps import apps as api_apps
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.contrib.postgres.fields import (
    ArrayField,
    FloatRangeField,
    IntegerRangeField,
)
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import (
    models,
)
from django.utils import (
    encoding,
)

# Local
from .managers import (
    UserManager,
)

docraptor.configuration.username = settings.DOCRAPTOR_API_KEY
doc_api = docraptor.DocApi()

log = logging.getLogger(__name__)


def generate_image_filename(instance, filename):
    f, ext = os.path.splitext(filename)
    return '{0}{1}'.format(instance.id, ext)


class Assignment(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        null=True,
        editable=False,
    )

    STATUS = Choices(
        (-10, 'archived', 'Archived',),
        (0, 'new', 'New',),
        (10, 'scheduled', 'Scheduled',),
        (20, 'confirmed', 'Confirmed',),
        (25, 'validated', 'Validated',),
        (30, 'final', 'Final',),
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    KIND = Choices(
        (5, 'drcj', 'DRCJ'),
        (10, 'ca', 'CA'),
        (20, 'aca', 'ACA'),
        (30, 'music', 'Music'),
        (40, 'presentation', 'Presentation'),
        (50, 'singing', 'Singing'),
    )

    kind = models.IntegerField(
        choices=KIND,
    )

    # FKs
    convention = models.ForeignKey(
        'Convention',
        related_name='assignments',
        on_delete=models.CASCADE,
    )

    person = models.ForeignKey(
        'Person',
        related_name='assignments',
        on_delete=models.CASCADE,
    )

    # Internals
    class Meta:
        unique_together = (
            ('convention', 'person',)
        )

    class JSONAPIMeta:
        resource_name = "assignment"

    def __unicode__(self):
        return self.nomen

    def save(self, *args, **kwargs):
        self.nomen = " ".join(filter(None, [
            "{0}".format(self.person),
            "{0}".format(self.convention),
            self.get_kind_display(),
        ]))
        super(Assignment, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        if request.user.is_authenticated():
            return any([
                True,
            ])
        return False


class Award(TimeStampedModel):
    """
    Award Model.

    The specific award conferred by an organization.
    Typically given once a year.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        null=True,
        editable=False,
    )

    name = models.CharField(
        help_text="""Award Name.""",
        max_length=255,
    )

    STATUS = Choices(
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    KIND = Choices(
        (1, 'quartet', 'Quartet',),
        (2, 'chorus', 'Chorus',),
        (10, 'seniors', 'Seniors',),
        (20, 'collegiate', 'Collegiate',),
        (30, 'youth', 'Youth',),
    )

    kind = models.IntegerField(
        choices=KIND,
    )

    SEASON = Choices(
        (1, 'summer', 'Summer',),
        (2, 'midwinter', 'Midwinter',),
        (3, 'fall', 'Fall',),
        (4, 'spring', 'Spring',),
        (9, 'video', 'Video',),
    )

    championship_season = models.IntegerField(
        choices=SEASON,
        null=True,
        blank=True,
    )

    qualifier_season = models.IntegerField(
        choices=SEASON,
        null=True,
        blank=True,
    )

    SIZE = Choices(
        (100, 'p1', 'Plateau 1',),
        (110, 'p2', 'Plateau 2',),
        (120, 'p3', 'Plateau 3',),
        (130, 'p4', 'Plateau 4',),
        (140, 'pa', 'Plateau A',),
        (150, 'paa', 'Plateau AA',),
        (160, 'paaa', 'Plateau AAA',),
        (170, 'paaaa', 'Plateau AAAA',),
        (180, 'pb', 'Plateau B',),
        (190, 'pi', 'Plateau I',),
        (200, 'pii', 'Plateau II',),
        (210, 'piii', 'Plateau III',),
        (220, 'piv', 'Plateau IV',),
        (230, 'small', 'Small',),
    )

    size = models.IntegerField(
        choices=SIZE,
        null=True,
        blank=True,
    )

    size_range = IntegerRangeField(
        null=True,
        blank=True,
    )

    SCOPE = Choices(
        (100, 'p1', 'Plateau 1',),
        (110, 'p2', 'Plateau 2',),
        (120, 'p3', 'Plateau 3',),
        (130, 'p4', 'Plateau 4',),
        (140, 'pa', 'Plateau A',),
        (150, 'paa', 'Plateau AA',),
        (160, 'paaa', 'Plateau AAA',),
        (170, 'paaaa', 'Plateau AAAA',),
        (175, 'paaaaa', 'Plateau AAAAA',),
    )

    scope = models.IntegerField(
        choices=SCOPE,
        null=True,
        blank=True,
    )

    scope_range = FloatRangeField(
        null=True,
        blank=True,
    )

    is_primary = models.BooleanField(
        help_text="""The primary award; requires qualification.""",
        default=False,
    )

    is_improved = models.BooleanField(
        help_text="""Designates 'Most-Improved'.  Implies manual.""",
        default=False,
    )

    is_novice = models.BooleanField(
        help_text="""Award for Novice groups.""",
        default=False,
    )

    is_manual = models.BooleanField(
        help_text="""Award must be determined manually.""",
        default=False,
    )

    is_multi = models.BooleanField(
        help_text="""Award spans conventions; must be determined manually.""",
        default=False,
    )

    is_district_representative = models.BooleanField(
        help_text="""Boolean; true means the district rep qualifies.""",
        default=False,
    )

    championship_rounds = models.IntegerField(
        help_text="""Number of rounds to determine the championship""",
    )

    qualifier_rounds = models.IntegerField(
        help_text="""Number of rounds to qualify for the award.""",
        null=True,
        blank=True,
    )

    threshold = models.FloatField(
        help_text="""
            The score threshold for automatic qualification (if any.)
        """,
        null=True,
        blank=True,
    )

    minimum = models.FloatField(
        help_text="""
            The minimum score required for qualification (if any.)
        """,
        null=True,
        blank=True,
    )

    advance = models.FloatField(
        help_text="""
            The score threshold to advance to next round (if any) in
            multi-round qualification.
        """,
        null=True,
        blank=True,
    )

    # FKs
    entity = TreeForeignKey(
        'Entity',
        related_name='awards',
        on_delete=models.CASCADE,
    )

    # Internals
    class JSONAPIMeta:
        resource_name = "award"

    def __unicode__(self):
        return self.nomen

    def save(self, *args, **kwargs):
        self.nomen = self.name
        super(Award, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        if request.user.is_authenticated():
            return any([
                self.entity.memberships.filter(
                    officers__office__short_name='DRCJ'
                )
            ])
        return False


class Catalog(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        null=True,
        editable=False,
    )

    STATUS = Choices(
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New'),
        (10, 'active', 'Active'),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    bhs_id = models.IntegerField(
        unique=True,
    )

    title = models.CharField(
        max_length=200,
    )

    published = models.DateField(
        null=True,
        blank=True,
    )

    arranger = models.CharField(
        blank=True,
        max_length=200,
    )

    arranger_fee = models.FloatField(
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

    difficulty = models.IntegerField(
        null=True,
        blank=True,
        choices=DIFFICULTY,
    )

    GENDER = Choices(
        (1, "Male"),
        (2, "Female"),
        (3, "Mixed"),
    )

    gender = models.IntegerField(
        null=True,
        blank=True,
        choices=GENDER,
    )

    TEMPO = Choices(
        (1, "Ballad"),
        (2, "Uptune"),
        (3, "Mixed"),
    )

    tempo = models.IntegerField(
        null=True,
        blank=True,
        choices=TEMPO,
    )

    is_medley = models.BooleanField(
        default=False,
    )

    is_learning = models.BooleanField(
        default=False,
    )

    VOICING = Choices(
        (1, "Barbershop"),
        (2, "Chorus + Quartet"),
        (3, "Double Quartet"),
        (4, "Ensemble + Soloist"),
    )

    voicing = models.IntegerField(
        null=True,
        blank=True,
        choices=VOICING,
    )

    # Internals
    class JSONAPIMeta:
        resource_name = "catalog"

    def __unicode__(self):
        return self.nomen

    def save(self, *args, **kwargs):
        self.nomen = " ".join(filter(None, [
            self.title,
            str(self.bhs_id),
        ]))
        super(Catalog, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


class Contest(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        null=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'opened', 'Opened',),
        (15, 'closed', 'Closed',),
        (35, 'validated', 'Validated',),
        (42, 'finished', 'Finished',),
        (45, 'published', 'Published',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    is_qualifier = models.BooleanField(
        default=False,
    )

    # FKs
    session = models.ForeignKey(
        'Session',
        related_name='contests',
        on_delete=models.CASCADE,
    )

    award = models.ForeignKey(
        'Award',
        related_name='contests',
        on_delete=models.CASCADE,
    )

    # Internals
    class Meta:
        unique_together = (
            ('session', 'award',)
        )

    class JSONAPIMeta:
        resource_name = "contest"

    def __unicode__(self):
        return self.nomen

    def save(self, *args, **kwargs):
        self.nomen = " ".join(filter(None, [
            self.award.name,
            self.session.nomen,
        ]))
        super(Contest, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        if request.user.is_authenticated():
            return any([
                True,
            ])
        return False

    # Methods
    def ranking(self, point_total):
        if not point_total:
            return None
        contestants = self.contestants.all()
        points = [contestant.contestantscore.calculate_total_points() for contestant in contestants]
        points = sorted(points, reverse=True)
        ranking = Ranking(points, start=1)
        rank = ranking.rank(point_total)
        return rank

    # Transitions
    @transition(field=status, source='*', target=STATUS.finished)
    def finish(self, *args, **kwargs):
        return


class ContestScore(Contest):
    champion = models.ForeignKey(
        'Performer',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # Internals
    class JSONAPIMeta:
        resource_name = "contestscore"

    # Methods
    def calculate(self, *args, **kwargs):
        if self.is_qualifier:
            champion = None
        else:
            try:
                champion = self.contestants.get(contestantscore__rank=1).performer
            except self.contestants.model.DoesNotExist:
                champion = None
            except self.contestants.model.MultipleObjectsReturned:
                champion = self.contestants.filter(contestantscore__rank=1).order_by(
                    '-contestantscore__sng_points',
                    '-contestantscore__mus_points',
                    '-contestantscore__prs_points',
                ).first().performer
        self.champion = champion

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        if request.user.is_authenticated():
            return any([
                True,
                # self.award.organization.representative.user == request.user,
                # self.session.assignments.filter(
                #     judge__user=request.user,
                #     category=self.session.assignments.model.category.ADMIN,
                # ),
                # self.status == self.STATUS.published,
            ])
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        if request.user.is_authenticated():
            return any([
                True,
                # self.award.organization.representative.user == request.user,
                # self.session.assignments.filter(
                #     judge__user=request.user,
                #     category=self.session.assignments.model.category.ADMIN,
                # ),
            ])
        return False


class Contestant(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=500,
        null=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'eligible', 'Eligible',),
        (20, 'ineligible', 'Ineligible',),
        (40, 'rep', 'District Representative',),
        (50, 'qualified', 'Qualified',),
        (55, 'validated', 'Validated',),
        (60, 'finished', 'Finished',),
        (70, 'scratched', 'Scratched',),
        (80, 'disqualified', 'Disqualified',),
        (90, 'published', 'Published',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    # FKs
    performer = models.ForeignKey(
        'Performer',
        related_name='contestants',
        on_delete=models.CASCADE,
    )

    contest = models.ForeignKey(
        'Contest',
        related_name='contestants',
        on_delete=models.CASCADE,
    )

    # Internals
    class Meta:
        unique_together = (
            ('performer', 'contest',),
        )

    class JSONAPIMeta:
        resource_name = "contestant"

    def __unicode__(self):
        return self.nomen

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: encoding.smart_text(x), [
                    self.performer,
                    self.contest,
                ]
            )
        )
        super(Contestant, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        if request.user.is_authenticated():
            return any([
                True,
                # self.contest.session.convention.drcj == request.user.person,
                # self.contest.session.assignments.filter(
                #     person__user=request.user,
                # ),
            ])
        return False

    # Methods

    # Transitions
    @transition(field=status, source='*', target=STATUS.disqualified)
    def process(self, *args, **kwargs):
        return

    @transition(field=status, source='*', target=STATUS.scratched)
    def scratch(self, *args, **kwargs):
        return

    @transition(field=status, source='*', target=STATUS.disqualified)
    def disqualify(self, *args, **kwargs):
        return

    @transition(field=status, source='*', target=STATUS.finished)
    def finish(self, *args, **kwargs):
        return

    @transition(field=status, source='*', target=STATUS.published)
    def publish(self, *args, **kwargs):
        return


class ContestantScore(Contestant):
    rank = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_points = models.IntegerField(
        null=True,
        blank=True,
    )

    prs_points = models.IntegerField(
        null=True,
        blank=True,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
    )

    total_points = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
    )

    prs_score = models.FloatField(
        null=True,
        blank=True,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
    )

    total_score = models.FloatField(
        null=True,
        blank=True,
    )

    class JSONAPIMeta:
        resource_name = "contestantscore"

    # Properties
    @property
    def official_result(self):
        if self.contest.is_qualifier:
            if self.contest.award.is_district_representative:
                if self.official_rank == 1:
                    return self.STATUS.rep
                if self.official_score < self.contest.award.minimum:
                    return self.STATUS.ineligible
                else:
                    return self.STATUS.eligible
            else:
                if self.contest.award.minimum:
                    if self.official_score < self.contest.award.minimum:
                        return self.STATUS.ineligible
                    elif self.official_score >= self.contest.award.threshold:
                        return self.STATUS.qualified
                    else:
                        return self.STATUS.eligible
                else:
                    return self.STATUS.eligible
        else:
            return self.official_rank

    # Methods
    def calculate(self, *args, **kwargs):
        self.mus_points = self.calculate_mus_points()
        self.prs_points = self.calculate_prs_points()
        self.sng_points = self.calculate_sng_points()
        self.total_points = self.calculate_total_points()
        self.mus_score = self.calculate_mus_score()
        self.prs_score = self.calculate_prs_score()
        self.sng_score = self.calculate_sng_score()
        self.total_score = self.calculate_total_score()
        self.rank = self.calculate_rank()

    def calculate_rank(self):
        return self.contest.ranking(self.calculate_total_points())

    def calculate_mus_points(self):
        return self.performer.performances.filter(
            songs__scores__kind=self.contest.session.assignments.model.KIND.official,
            songs__scores__category=self.contest.session.assignments.model.CATEGORY.music,
            round__num__lte=self.contest.award.num_rounds,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_prs_points(self):
        return self.performer.performances.filter(
            songs__scores__kind=self.contest.session.assignments.model.KIND.official,
            songs__scores__category=self.contest.session.assignments.model.CATEGORY.presentation,
            round__num__lte=self.contest.award.num_rounds,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_sng_points(self):
        return self.performer.performances.filter(
            songs__scores__kind=self.contest.session.assignments.model.KIND.official,
            songs__scores__category=self.contest.session.assignments.model.CATEGORY.singing,
            round__num__lte=self.contest.award.num_rounds,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_total_points(self):
        return self.performer.performances.filter(
            songs__scores__kind=self.contest.session.assignments.model.KIND.official,
            round__num__lte=self.contest.award.num_rounds,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_mus_score(self):
        return self.performer.performances.filter(
            songs__scores__kind=self.contest.session.assignments.model.KIND.official,
            songs__scores__category=self.contest.session.assignments.model.CATEGORY.music,
            round__num__lte=self.contest.award.num_rounds,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_prs_score(self):
        return self.performer.performances.filter(
            songs__scores__kind=self.contest.session.assignments.model.KIND.official,
            songs__scores__category=self.contest.session.assignments.model.CATEGORY.presentation,
            round__num__lte=self.contest.award.num_rounds,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_sng_score(self):
        return self.performer.performances.filter(
            songs__scores__kind=self.contest.session.assignments.model.KIND.official,
            songs__scores__category=self.contest.session.assignments.model.CATEGORY.singing,
            round__num__lte=self.contest.award.num_rounds,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_total_score(self):
        return self.performer.performances.filter(
            songs__scores__kind=self.contest.session.assignments.model.KIND.official,
            round__num__lte=self.contest.award.num_rounds,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        if request.user.is_authenticated():
            return any([
                True
                # self.contest.award.organization.representative.user == request.user,
            ])
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        if request.user.is_authenticated():
            return any([
                # self.contest.award.organization.representative.user == request.user,
                True
            ])
        return False


class Convention(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        null=True,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (2, 'listed', 'Listed',),
        (4, 'opened', 'Opened',),
        (8, 'closed', 'Closed',),
        (10, 'validated', 'Validated',),
        (20, 'started', 'Started',),
        (30, 'finished', 'Finished',),
        (45, 'published', 'Published',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    LEVEL = Choices(
        (0, 'international', "International"),
        (1, 'district', "District"),
        (2, 'division', "Division"),
        (3, 'chapter', "Chapter"),
    )

    level = models.IntegerField(
        choices=LEVEL,
    )

    SEASON = Choices(
        (1, 'summer', 'Summer',),
        (2, 'midwinter', 'Midwinter',),
        (3, 'fall', 'Fall',),
        (4, 'spring', 'Spring',),
        (9, 'video', 'Video',),
    )

    season = models.IntegerField(
        choices=SEASON,
    )

    PANEL = Choices(
        (0, 'unknown', "Unknown"),
        (1, 'single', "Single"),
        (2, 'double', "Double"),
        (3, 'triple', "Triple"),
        (4, 'quadruple', "Quadruple"),
        (5, 'quintiple', "Quintiple"),
    )

    panel = models.IntegerField(
        choices=PANEL,
        default=PANEL.unknown,
    )

    RISERS = [
        (0, 0),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (12, 12),
        (13, 13),
    ]

    risers = ArrayField(
        base_field=models.IntegerField(null=True, blank=True),
        null=True,
        blank=True,
    )

    YEAR_CHOICES = []
    for r in reversed(range(1939, (datetime.datetime.now().year + 2))):
        YEAR_CHOICES.append((r, r))

    year = models.IntegerField(
        choices=YEAR_CHOICES,
    )

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    location = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    # FKs
    venue = models.ForeignKey(
        'Venue',
        related_name='conventions',
        help_text="""
            The venue for the convention.""",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # Internals
    class JSONAPIMeta:
        resource_name = "convention"

    def __unicode__(self):
        return self.nomen

    def save(self, *args, **kwargs):
        self.nomen = self.name
        super(Convention, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        if request.user.is_authenticated():
            return any([
                self.hosts.filter(
                    entity__memberships__officers__office__short_name='DRCJ',
                ),
            ])
        return False

    # Transitions
    @transition(field=status, source='*', target=STATUS.started)
    def start(self, *args, **kwargs):
        return

    @transition(field=status, source='*', target=STATUS.finished)
    def finish(self, *args, **kwargs):
        return


class Entity(MPTTModel, TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        null=True,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the resource.""",
        max_length=200,
    )

    STATUS = Choices(
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    LEVEL = Choices(
        (0, 'organization', 'Organization'),
        (1, 'district', 'District'),
        (2, 'division', 'Division'),
        (3, 'group', 'Group'),
    )

    level = models.IntegerField(
        choices=LEVEL,
    )

    KIND = Choices(
        ('International', [
            (1, 'bhs', "Barbershop Harmony Society"),
            (2, 'hi', "Harmony Incorporated"),
        ]),
        ('District', [
            (11, 'district', "District"),
            (12, 'noncomp', "Noncompetitive"),
            (13, 'affiliate', "Affiliate"),
        ]),
        ('Division', [
            (21, 'division', "Division"),
        ]),
        ('Group', [
            (31, 'quartet', "Quartet"),
            (32, 'chorus', "Chorus"),
            (33, 'vlq', "Very Large Quartet"),
        ]),
        # ('Leadership', [
        #     (14, 'cj', "Contest and Judging"),
        # ]),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of organization.""",
        choices=KIND,
    )

    AGE = Choices(
        (10, 'seniors', 'Seniors',),
        (20, 'collegiate', 'Collegiate',),
        (30, 'youth', 'Youth',),
    )

    age = models.IntegerField(
        choices=AGE,
        null=True,
        blank=True,
    )

    is_novice = models.BooleanField(
        default=False,
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

    code = models.CharField(
        help_text="""
            The chapter code.""",
        max_length=200,
        blank=True,
        null=True,
    )

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    end_date = models.DateField(
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

    phone = models.CharField(
        help_text="""
            The phone number of the resource.  Include country code.""",
        null=True,
        blank=True,
        default='',
        max_length=25,
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

    bhs_id = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
    )

    # FKs
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        on_delete=models.SET_NULL,
    )

    # Internals
    class Meta:
        verbose_name_plural = 'entities'

    class MPTTMeta:
        order_insertion_by = [
            'level',
            'kind',
            'name',
        ]

    class JSONAPIMeta:
        resource_name = "entity"

    def __unicode__(self):
        return self.nomen

    def save(self, *args, **kwargs):
        self.nomen = self.name
        super(Entity, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        if request.user.is_authenticated():
            return any([
                self.memberships.filter(
                    officers__office__short_name='DRCJ'
                )
            ])
        return False


class Host(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        null=True,
        editable=False,
    )

    STATUS = Choices(
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    # FKs
    convention = models.ForeignKey(
        'Convention',
        related_name='hosts',
        on_delete=models.CASCADE,
    )

    entity = TreeForeignKey(
        'Entity',
        related_name='hosts',
        on_delete=models.CASCADE,
    )

    # Internals
    class Meta:
        unique_together = (
            ('convention', 'entity',),
        )

    class JSONAPIMeta:
        resource_name = "host"

    def __unicode__(self):
        return self.nomen

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: encoding.smart_text(x), [
                    self.convention,
                    self.entity,
                ]
            )
        )
        super(Host, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        if request.user.is_authenticated():
            return any([
                True,
            ])
        return False


class Membership(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        null=True,
        editable=False,
    )

    STATUS = Choices(
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    PART = Choices(
        (1, 'tenor', 'Tenor'),
        (2, 'lead', 'Lead'),
        (3, 'baritone', 'Baritone'),
        (4, 'bass', 'Bass'),
        (5, 'director', 'Director'),
    )

    part = models.IntegerField(
        choices=PART,
        null=True,
        blank=True,
    )

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    # FKs
    entity = TreeForeignKey(
        'Entity',
        related_name='memberships',
        on_delete=models.CASCADE,
    )

    person = models.ForeignKey(
        'Person',
        related_name='memberships',
        on_delete=models.CASCADE,
    )

    # Internals
    class Meta:
        unique_together = (
            ('entity', 'person',),
        )

    class JSONAPIMeta:
        resource_name = "membership"

    def __unicode__(self):
        return self.nomen

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: encoding.smart_text(x), [
                    self.entity,
                    self.person,
                ]
            )
        )
        super(Membership, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


class Office(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        null=True,
        editable=False,
    )

    name = models.CharField(
        max_length=200,
    )

    STATUS = Choices(
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    KIND = Choices(
        (0, 'new', 'New',),
        (1, 'one', 'One',),
        (10, 'ten', 'Ten',),
        (20, 'twenty', 'Twenty',),
        (30, 'thirty', 'Thirty',),
    )

    kind = FSMIntegerField(
        choices=KIND,
        default=KIND.new,
    )

    short_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    long_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    # Methods
    def save(self, *args, **kwargs):
        self.nomen = self.name
        super(Office, self).save(*args, **kwargs)

    # Internals
    class JSONAPIMeta:
        resource_name = "office"

    def __unicode__(self):
        return self.nomen

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


class Officer(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        null=True,
        editable=False,
    )

    STATUS = Choices(
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    # FKs
    office = models.ForeignKey(
        'Office',
        related_name='officers',
        on_delete=models.CASCADE,
    )

    membership = models.ForeignKey(
        'Membership',
        related_name='officers',
        on_delete=models.CASCADE,
    )

    # Internals
    class JSONAPIMeta:
        resource_name = "officer"

    def __unicode__(self):
        return self.nomen

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: encoding.smart_text(x), [
                    self.office,
                    self.membership,
                ]
            )
        )
        super(Officer, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


class Performance(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        null=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (5, 'validated', 'Validated',),
        (10, 'started', 'Started',),
        (20, 'finished', 'Finished',),
        (30, 'entered', 'Entered',),
        (40, 'flagged', 'Flagged',),
        (60, 'cleared', 'Cleared',),
        (90, 'published', 'Published',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    num = models.IntegerField(
        null=True,
        blank=True,
    )

    actual_start = models.DateTimeField(
        help_text="""
            The actual performance window.""",
        null=True,
        blank=True,
    )

    actual_finish = models.DateTimeField(
        help_text="""
            The actual performance window.""",
        null=True,
        blank=True,
    )

    # FKs
    round = models.ForeignKey(
        'Round',
        related_name='performances',
        on_delete=models.CASCADE,
    )

    performer = models.ForeignKey(
        'Performer',
        related_name='performances',
        on_delete=models.CASCADE,
    )

    slot = models.OneToOneField(
        'Slot',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # Internals
    class JSONAPIMeta:
        resource_name = "performance"

    def __unicode__(self):
        return self.nomen

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: encoding.smart_text(x), [
                    self.round,
                    self.performer,
                ]
            )
        )
        super(Performance, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        if request.user.is_authenticated():
            return any([
                True,
                # self.round.session.assignments.filter(
                #     judge__user=request.user,
                #     category=self.round.session.assignments.model.category.ADMIN,
                # ),
                # self.performer.session.convention.drcj == request.user.person,
            ])
        return False

    # Transitions
    @transition(field=status, source='*', target=STATUS.started)
    def start(self, *args, **kwargs):
        return

    @transition(field=status, source='*', target=RETURN_VALUE(STATUS.cleared, STATUS.flagged))
    def verify(self, *args, **kwargs):
        self.performancescore.calculate()
        self.performancescore.save()
        config = api_apps.get_app_config('app')
        Song = config.get_model('Song')
        songs = Song.objects.filter(
            performance=self,
        )
        for song in songs:
            song.calculate()
            song.save()
        Score = config.get_model('Score')
        scores = Score.objects.filter(
            song__performance=self,
        )
        flags = []
        for score in scores:
            flags.append(score.verify())
        if any(flags):
            return self.STATUS.flagged
        return self.STATUS.cleared

    @transition(field=status, source='*', target=STATUS.published)
    def publish(self, *args, **kwargs):
        return


class PerformanceScore(Performance):
    rank = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_points = models.IntegerField(
        null=True,
        blank=True,
    )

    prs_points = models.IntegerField(
        null=True,
        blank=True,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
    )

    total_points = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
    )

    prs_score = models.FloatField(
        null=True,
        blank=True,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
    )

    total_score = models.FloatField(
        null=True,
        blank=True,
    )

    # Internals
    class JSONAPIMeta:
        resource_name = "performancescore"

    # Methods
    def calculate(self, *args, **kwargs):
        # self.rank = self.calculate_rank()
        self.mus_points = self.calculate_mus_points()
        self.prs_points = self.calculate_prs_points()
        self.sng_points = self.calculate_sng_points()
        self.total_points = self.calculate_total_points()
        self.mus_score = self.calculate_mus_score()
        self.prs_score = self.calculate_prs_score()
        self.sng_score = self.calculate_sng_score()
        self.total_score = self.calculate_total_score()

    def calculate_rank(self):
        return self.round.ranking(self.calculate_total_points())

    def calculate_mus_points(self):
        return self.songs.filter(
            scores__kind=self.round.session.assignments.model.KIND.official,
            scores__category=self.round.session.assignments.model.CATEGORY.music,
        ).aggregate(
            tot=models.Sum('scores__points')
        )['tot']

    def calculate_prs_points(self):
        return self.songs.filter(
            scores__kind=self.round.session.assignments.model.KIND.official,
            scores__category=self.round.session.assignments.model.CATEGORY.presentation,
        ).aggregate(
            tot=models.Sum('scores__points')
        )['tot']

    def calculate_sng_points(self):
        return self.songs.filter(
            scores__kind=self.round.session.assignments.model.KIND.official,
            scores__category=self.round.session.assignments.model.CATEGORY.singing,
        ).aggregate(
            tot=models.Sum('scores__points')
        )['tot']

    def calculate_total_points(self):
        return self.songs.filter(
            scores__kind=self.round.session.assignments.model.KIND.official,
        ).aggregate(
            tot=models.Sum('scores__points')
        )['tot']

    def calculate_mus_score(self):
        return self.songs.filter(
            scores__kind=self.round.session.assignments.model.KIND.official,
            scores__category=self.round.session.assignments.model.CATEGORY.music,
        ).aggregate(
            tot=models.Avg('scores__points')
        )['tot']

    def calculate_prs_score(self):
        return self.songs.filter(
            scores__kind=self.round.session.assignments.model.KIND.official,
            scores__category=self.round.session.assignments.model.CATEGORY.presentation,
        ).aggregate(
            tot=models.Avg('scores__points')
        )['tot']

    def calculate_sng_score(self):
        return self.songs.filter(
            scores__kind=self.round.session.assignments.model.KIND.official,
            scores__category=self.round.session.assignments.model.CATEGORY.singing,
        ).aggregate(
            tot=models.Avg('scores__points')
        )['tot']

    def calculate_total_score(self):
        return self.songs.filter(
            scores__kind=self.round.session.assignments.model.KIND.official,
        ).aggregate(
            tot=models.Avg('scores__points')
        )['tot']

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        if request.user.is_authenticated():
            # return any([
            #     self.round.session.assignments.filter(
            #         # judge__user=request.user,
            #         category=self.round.session.assignments.model.category.ADMIN,
            #     ),
            # ])
            return True
        return False


class Performer(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        null=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'registered', 'Registered',),
        (20, 'accepted', 'Accepted',),
        (30, 'declined', 'Declined',),
        (40, 'dropped', 'Dropped',),
        (50, 'validated', 'Validated',),
        (52, 'scratched', 'Scratched',),
        (55, 'disqualified', 'Disqualified',),
        (57, 'started', 'Started',),
        (60, 'finished', 'Finished',),
        (90, 'published', 'Published',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
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
        null=True,
        blank=True,
    )

    risers = models.IntegerField(
        help_text="""
            The number of risers select.""",
        null=True,
        blank=True,
    )

    is_evaluation = models.BooleanField(
        help_text="""
            Performer requests evaluation.""",
        default=True,
    )

    is_private = models.BooleanField(
        help_text="""
            Keep scores private.""",
        default=False,
    )

    seed = models.IntegerField(
        help_text="""
            The incoming rank based on prelim score.""",
        null=True,
        blank=True,
    )

    prelim = models.FloatField(
        help_text="""
            The incoming prelim score.""",
        null=True,
        blank=True,
    )

    bhs_id = models.IntegerField(
        null=True,
        blank=True,
    )

    # FKs
    session = models.ForeignKey(
        'Session',
        related_name='performers',
        on_delete=models.CASCADE,
    )

    entity = TreeForeignKey(
        'Entity',
        related_name='performers',
        on_delete=models.CASCADE,
    )

    tenor = models.ForeignKey(
        'Person',
        null=True,
        blank=True,
        related_name='performers_tenor',
        on_delete=models.SET_NULL,
    )

    lead = models.ForeignKey(
        'Person',
        null=True,
        blank=True,
        related_name='performers_lead',
        on_delete=models.SET_NULL,
    )

    baritone = models.ForeignKey(
        'Person',
        null=True,
        blank=True,
        related_name='performers_baritone',
        on_delete=models.SET_NULL,
    )

    bass = models.ForeignKey(
        'Person',
        null=True,
        blank=True,
        related_name='performers_bass',
        on_delete=models.SET_NULL,
    )

    director = models.ForeignKey(
        'Person',
        null=True,
        blank=True,
        related_name='performers_director',
        on_delete=models.SET_NULL,
    )

    codirector = models.ForeignKey(
        'Person',
        null=True,
        blank=True,
        related_name='performers_codirector',
        on_delete=models.SET_NULL,
    )

    # # Internals
    class Meta:
        unique_together = (
            ('entity', 'session',),
        )

    class JSONAPIMeta:
        resource_name = "performer"

    def __unicode__(self):
        return self.nomen

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: encoding.smart_text(x), [
                    self.entity,
                    self.session,
                ]
            )
        )
        super(Performer, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        if request.user.is_authenticated():
            return any([
                True,
                # self.group.roles.filter(
                #     status=self.group.roles.model.STATUS.active,
                #     person__user=request.user,
                # ),
                # self.session.assignments.filter(
                #     judge__user=request.user,
                #     category=self.session.assignments.model.CATEGORY.admin,
                # ),
                # self.session.convention.drcj == request.user.person,
            ])
        return False

    # Methods
    # Transitions
    @transition(field=status, source='*', target=STATUS.validated)
    def validate(self, *args, **kwargs):
        return

    @transition(field=status, source='*', target=STATUS.started)
    def start(self, *args, **kwargs):
        return

    @transition(field=status, source='*', target=STATUS.finished)
    def finish(self, *args, **kwargs):
        return


class PerformerScore(Performer):
    rank = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_points = models.IntegerField(
        null=True,
        blank=True,
    )

    prs_points = models.IntegerField(
        null=True,
        blank=True,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
    )

    total_points = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
    )

    prs_score = models.FloatField(
        null=True,
        blank=True,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
    )

    total_score = models.FloatField(
        null=True,
        blank=True,
    )

    csa_pdf = models.FileField(
        help_text="""
            The historical PDF CSA.""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    # Internals
    class JSONAPIMeta:
        resource_name = "performerscore"

    # Methods
    def calculate(self, *args, **kwargs):
        self.mus_points = self.calculate_mus_points()
        self.prs_points = self.calculate_prs_points()
        self.sng_points = self.calculate_sng_points()
        self.total_points = self.calculate_total_points()
        self.mus_score = self.calculate_mus_score()
        self.prs_score = self.calculate_prs_score()
        self.sng_score = self.calculate_sng_score()
        self.total_score = self.calculate_total_score()
        self.rank = self.calculate_rank()

    def calculate_pdf(self):
        for performance in self.performances.all():
            for song in performance.songs.all():
                song.calculate()
                song.save()
            performance.calculate()
            performance.save()
        self.calculate()
        self.save()
        return

    # def print_csa(self):
    #     performer = self
    #     contestants = performer.contestants.all()
    #     performances = performer.performances.order_by(
    #         'round__kind',
    #     )
    #     assignments = performer.session.assignments.exclude(
    #         category=Assignment.CATEGORY.admin,
    #     ).order_by(
    #         'category',
    #         'kind',
    #         'slot',
    #     )
    #     foo = get_template('csa.html')
    #     template = foo.render(context={
    #         'performer': performer,
    #         'performances': performances,
    #         'assignments': assignments,
    #         'contestants': contestants,
    #     })
    #     try:
    #         create_response = doc_api.create_doc({
    #             "test": True,
    #             "document_content": template,
    #             "name": "csa-{0}.pdf".format(id),
    #             "document_type": "pdf",
    #         })
    #         f = ContentFile(create_response)
    #         performer.csa_pdf.save(
    #             "{0}.pdf".format(id),
    #             f
    #         )
    #         performer.save()
    #         log.info("PDF created and saved to instance")
    #     except docraptor.rest.ApiException as error:
    #         log.error(error)
    #         log.error(error.message)
    #         log.error(error.response_body)
    #     return "Complete"

    def calculate_rank(self):
        try:
            return self.contestants.get(contest=self.session.primary).contestantscore.calculate_rank()
        except self.contestants.model.DoesNotExist:
            return None

    def calculate_mus_points(self):
        return self.performances.filter(
            songs__scores__kind=self.session.assignments.model.KIND.official,
            songs__scores__category=self.session.assignments.model.CATEGORY.music,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_prs_points(self):
        return self.performances.filter(
            songs__scores__kind=self.session.assignments.model.KIND.official,
            songs__scores__category=self.session.assignments.model.CATEGORY.presentation,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_sng_points(self):
        return self.performances.filter(
            songs__scores__kind=self.session.assignments.model.KIND.official,
            songs__scores__category=self.session.assignments.model.CATEGORY.singing,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_total_points(self):
        return self.performances.filter(
            songs__scores__kind=self.session.assignments.model.KIND.official,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_mus_score(self):
        return self.performances.filter(
            songs__scores__kind=self.session.assignments.model.KIND.official,
            songs__scores__category=self.session.assignments.model.CATEGORY.music,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_prs_score(self):
        return self.performances.filter(
            songs__scores__kind=self.session.assignments.model.KIND.official,
            songs__scores__category=self.session.assignments.model.CATEGORY.presentation,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_sng_score(self):
        return self.performances.filter(
            songs__scores__kind=self.session.assignments.model.KIND.official,
            songs__scores__category=self.session.assignments.model.CATEGORY.singing,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_total_score(self):
        return self.performances.filter(
            songs__scores__kind=self.session.assignments.model.KIND.official,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        if self.status == self.STATUS.published:
            return True
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        if request.user.is_authenticated():
            return any([
                True,
            ])
        return False


class Person(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        null=True,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the resource.""",
        max_length=200,
    )

    STATUS = Choices(
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New',),
        (1, 'active', 'Active',),
        # (2, 'inactive', 'Inactive',),
        (3, 'retired', 'Retired',),
        (5, 'deceased', 'Deceased',),
        (6, 'six', '(Six)',),
        (9, 'nine', '(Nine)',),
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    KIND = Choices(
        (0, 'new', 'New',),
        (10, 'member', 'Member',),
        (20, 'nonmember', 'Non-Member',),
        (30, 'associate', 'Associate',),
    )

    kind = models.IntegerField(
        choices=KIND,
        default=KIND.new,
    )

    bhs_status = models.IntegerField(
        blank=True,
        null=True,
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
    )

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    dues_thru = models.DateField(
        null=True,
        blank=True,
    )

    mon = models.IntegerField(
        null=True,
        blank=True,
    )

    spouse = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    location = models.CharField(
        help_text="""
            The geographical location of the resource.""",
        max_length=200,
        blank=True,
        default='',
    )

    website = models.URLField(
        help_text="""
            The website URL of the resource.""",
        blank=True,
        default='',
    )

    facebook = models.URLField(
        help_text="""
            The facebook URL of the resource.""",
        blank=True,
        default='',
    )

    twitter = models.CharField(
        help_text="""
            The twitter handle (in form @twitter_handle) of the resource.""",
        blank=True,
        default='',
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
        default='',
    )

    phone = models.CharField(
        help_text="""
            The phone number of the resource.  Include country code.""",
        null=True,
        blank=True,
        default='',
        max_length=25,
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

    bhs_id = models.IntegerField(
        null=True,
        blank=True,
        unique=True,
    )

    # Denormalizations
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

    common_name = models.CharField(
        max_length=255,
        blank=True,
        editable=False,
        default='',
    )

    full_name = models.CharField(
        max_length=255,
        blank=True,
        editable=False,
        default='',
    )

    formal_name = models.CharField(
        max_length=255,
        blank=True,
        editable=False,
        default='',
    )

    # FKs
    user = models.OneToOneField(
        'User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # Internals
    class JSONAPIMeta:
        resource_name = "person"

    def __unicode__(self):
        return self.nomen

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: encoding.smart_text(x),
                filter(
                    None, [
                        self.name,
                        self.bhs_id,
                    ]
                )
            )
        )
        super(Person, self).save(*args, **kwargs)

    def calculate_name(self):
        name = HumanName(self.name)
        if name.nickname:
            self.common_name = " ".join(filter(None, [
                "{0}".format(name.nickname),
                "{0}".format(name.last),
                "{0}".format(name.suffix),
            ]))
        else:
            self.common_name = '{0}'.format(self.name)
        self.formal_name = " ".join(filter(None, [
            '{0}'.format(name.first),
            '{0}'.format(name.last),
            '{0}'.format(name.suffix),
        ]))

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        if request.user.is_authenticated():
            return self.user == request.user
        return False


class Round(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        null=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        # (10, 'built', 'Built',),
        (10, 'drawn', 'Drawn',),
        (15, 'validated', 'Validated',),
        (20, 'started', 'Started',),
        (25, 'finished', 'Finished',),
        # (28, 'ranked', 'Ranked',),
        # (30, 'final', 'Final',),
        (50, 'published', 'Published',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
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

    num_songs = models.IntegerField(
        default=2,
    )

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    ann_pdf = models.FileField(
        help_text="""
            The announcement PDF.""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    # FKs
    session = models.ForeignKey(
        'Session',
        related_name='rounds',
        on_delete=models.CASCADE,
    )

    # Internals
    class Meta:
        unique_together = (
            ('session', 'kind',),
        )

    class JSONAPIMeta:
        resource_name = "round"

    def __unicode__(self):
        return self.nomen

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: encoding.smart_text(x), [
                    self.session,
                    self.get_kind_display(),
                ]
            )
        )
        super(Round, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False

    # Methods
    def ranking(self, point_total):
        if not point_total:
            return None
        performances = self.performances.all()
        points = [performance.performancescore.calculate_total_points() for performance in performances]
        points = sorted(points, reverse=True)
        ranking = Ranking(points, start=1)
        rank = ranking.rank(point_total)
        return rank

    # Transitions
    @transition(field=status, source='*', target=STATUS.drawn)
    def draw(self, *args, **kwargs):
        i = 1
        for performance in self.performances.order_by('?'):
            performance.slot = i
            performance.save()
            i += 1
        return

    @transition(field=status, source='*', target=STATUS.validated)
    def validate(self, *args, **kwargs):
        return

    @transition(field=status, source='*', target=STATUS.started)
    def start(self, *args, **kwargs):
        # if self.num == 1:
        #     # if the first round, start all performers
        #     for performer in self.session.performers.all():
        #         performer.start()
        #         performer.save()
        return

    @transition(field=status, source='*', target=STATUS.finished)
    def finish(self, *args, **kwargs):
        if self.kind == self.KIND.finals:
            # If the Finals, finish performers and return
            for performer in self.session.performers.filter(
                status=self.session.performers.model.STATUS.started
            ):
                performer.finish()
                performer.save()
            for contest in self.session.contests.all():
                for contestant in contest.contestants.all():
                    contestant.finish()
                    contestant.save()
                contest.finish()
                contest.save()
            self.session.finish()
            self.session.save()
            return
        # Hard-code the International Quartet Contest
        if all([
            self.session.convention.kind == self.session.convention.KIND.international,
            self.session.kind == self.session.KIND.quartet,
        ]):
            if self.kind == self.KIND.quarters:
                spots = 20
                next_round, created = self.session.rounds.get_or_create(
                    num=2,
                    kind=self.session.rounds.model.KIND.semis,
                )
            else:
                spots = 10
                next_round, created = self.session.rounds.get_or_create(
                    num=3,
                    kind=self.session.rounds.model.KIND.finals,
                )
            # Get all the primary contestants by random order
            contestants = self.session.primary.contestants.order_by('?')
            i = 1
            for contestant in contestants:
                # Advance the performer if the rank is GTE spots.
                if contestant.calculate_rank() <= spots:
                    next_round.performances.get_or_create(
                        performer=contestant.performer,
                        num=i,
                    )
                    i += 1
            return
        # Get the number of spots available
        spots = self.session.convention.organization.spots
        # Create performances accordingly
        next_round = self.session.rounds.create(
            num=2,
            kind=self.session.rounds.model.KIND.finals,
        )
        # Non-International Quartet Rounds
        # Instantiate the advancing list
        advancing = []
        # Only address multi-round contests; single-round awards do not proceed.
        for contest in self.session.contests.filter(num_rounds__gt=1):
            # Qualifiers have an absolute score cutoff
            if contest.is_qualifier:
                # Uses absolute cutoff.
                contestants = contest.contestants.filter(
                    total_score__gte=contest.award.advance,
                )
                for contestant in contestants:
                    advancing.append(contestant.performer)
            # Championships are relative.
            else:
                # Get the top scorer
                top = contest.contestants.filter(
                    rank=1,
                ).first()
                # Derive the accept threshold from that top score.
                accept = top.calculate_total_score() - 4.0
                contestants = contest.contestants.filter(
                    total_score__gte=accept,
                )
                for contestant in contestants:
                    advancing.append(contestant.performer)
        # Remove duplicates
        advancing = list(set(advancing))
        # Append up to spots available.
        diff = spots - len(advancing)
        if diff > 0:
            adds = self.performances.filter(
                performer__contestants__contest__num_rounds__gt=1,
            ).exclude(
                performer__in=advancing,
            ).order_by(
                '-total_points',
            )[:diff]
            for a in adds:
                advancing.append(a.performer)
        random.shuffle(advancing)
        i = 1
        for performer in advancing:
            next_round.performances.get_or_create(
                performer=performer,
                slot=i,
            )
            i += 1
        return

    @transition(field=status, source='*', target=STATUS.published)
    def publish(self, *args, **kwargs):
        if self.kind == self.KIND.finals:
            for performance in self.performances.all():
                performance.publish()
                performance.save()
        else:
            next_round = self.session.rounds.get(num=self.num + 1)
            next_round.validate()
            next_round.save()
            # TODO This makes me REALLY nervous...
            dnp = self.session.performers.exclude(
                performances__round=next_round,
            )
            for performer in dnp:
                for performance in performer.performances.all():
                    for song in performance.songs.all():
                        song.publish()
                        song.save()
                    performance.publish()
                    performance.save()
                performer.publish()
                performer.save()
            self.current = next_round
            self.save()
        return


class Score(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        null=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'validated', 'Validated',),
        # (20, 'entered', 'Entered',),
        (25, 'cleared', 'Cleared',),
        (30, 'flagged', 'Flagged',),
        (35, 'revised', 'Revised',),
        (40, 'confirmed', 'Confirmed',),
        # (50, 'final', 'Final',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    CATEGORY = Choices(
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

    points = models.IntegerField(
        help_text="""
            The number of points (0-100)""",
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

    original = models.IntegerField(
        help_text="""
            The original score (before revision).""",
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

    VIOLATION = Choices(
        (10, 'general', 'General'),
    )

    violation = FSMIntegerField(
        choices=VIOLATION,
        null=True,
        blank=True,
    )

    penalty = models.IntegerField(
        help_text="""
            The penalty (0-100)""",
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

    is_flagged = models.BooleanField(
        default=False,
    )

    # FKs
    song = models.ForeignKey(
        'Song',
        related_name='scores',
        on_delete=models.CASCADE,
    )

    person = models.ForeignKey(
        'Person',
        related_name='scores',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class JSONAPIMeta:
        resource_name = "score"

    def __unicode__(self):
        return self.nomen

    def save(self, *args, **kwargs):
        self.nomen = self.id.hex
        super(Score, self).save(*args, **kwargs)

    # Methods
    def verify(self):
        variance = False
        mus_avg = self.song.scores.filter(
            kind=self.song.scores.model.KIND.official,
            category=self.song.scores.model.CATEGORY.music,
        ).aggregate(
            avg=models.Avg('points')
        )['avg']
        if self.category == self.CATEGORY.music:
            if abs(self.points - mus_avg) > 5:
                log.info("Variance Music {0}".format(self))
                variance = True
        prs_avg = self.song.scores.filter(
            kind=self.song.scores.model.KIND.official,
            category=self.song.scores.model.CATEGORY.presentation,
        ).aggregate(
            avg=models.Avg('points')
        )['avg']
        if self.category == self.CATEGORY.presentation:
            if abs(self.points - prs_avg) > 5:
                log.info("Variance Presentation {0}".format(self))
                variance = True
        sng_avg = self.song.scores.filter(
            kind=self.song.scores.model.KIND.official,
            category=self.song.scores.model.CATEGORY.singing,
        ).aggregate(
            avg=models.Avg('points')
        )['avg']
        if self.category == self.CATEGORY.singing:
            if abs(self.points - sng_avg) > 5:
                log.info("Variance Singing {0}".format(self))
                variance = True
        ordered_asc = self.song.scores.filter(
            kind=self.song.scores.model.KIND.official,
        ).order_by('points')
        if ordered_asc[1].points - ordered_asc[0].points > 5 and ordered_asc[0].points == self.points:
            log.info("Variance Low {0}".format(self))
            variance = True
        ordered_dsc = self.song.scores.filter(
            kind=self.song.scores.model.KIND.official,
        ).order_by('-points')
        if ordered_dsc[0].points - ordered_dsc[1].points > 5 and ordered_dsc[0].points == self.points:
            log.info("Variance High {0}".format(self))
            variance = True
        if variance:
            self.original = self.points
            self.is_flagged = True
            self.save()
        return variance

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        if request.user.is_authenticated():
            return any([
                True,
                # self.song.performance.performer.session.assignments.filter(
                #     judge__user=request.user,
                #     category=self.song.performance.round.session.assignments.model.CATEGORY.admin,
                # ),
                # self.song.performance.performer.group.roles.filter(
                #     person__user=request.user,
                #     status=self.song.performance.performer.group.roles.model.STATUS.active,
                # ),
            ])
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        if request.user.is_authenticated():
            return any([
                True,
                # self.song.performance.performer.session.assignments.filter(
                #     judge__user=request.user,
                #     category=self.song.performance.round.session.assignments.model.CATEGORY.admin,
                # ),
                # self.song.performance.performer.group.roles.filter(
                #     person__user=request.user,
                #     status=self.song.performance.performer.group.roles.model.STATUS.active,
                # ),
            ])
        return False


class Session(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        null=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (2, 'listed', 'Listed',),
        (4, 'opened', 'Opened',),
        (8, 'closed', 'Closed',),
        (10, 'validated', 'Validated',),
        (20, 'started', 'Started',),
        # (25, 'ranked', 'Ranked',),
        (30, 'finished', 'Finished',),
        # (40, 'drafted', 'Drafted',),
        (45, 'published', 'Published',),
        # (50, 'final', 'Final',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    KIND = Choices(
        (1, 'quartet', 'Quartet',),
        (2, 'chorus', 'Chorus',),
        (10, 'seniors', 'Seniors',),
        (20, 'collegiate', 'Collegiate',),
        (30, 'youth', 'Youth',),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of session.  Generally this will be either quartet or chorus,
            with the exception being International and Midwinter which hold exclusive
            Youth and Senior sessions respectively.""",
        choices=KIND,
    )

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    num_rounds = models.IntegerField(
    )

    panel_size = models.IntegerField(
        null=True,
        blank=True,
    )

    is_prelims = models.BooleanField(
        default=False,
    )

    cursor = models.OneToOneField(
        'Performance',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    current = models.ForeignKey(
        'Round',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='current_session',
    )

    primary = models.ForeignKey(
        'Contest',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='primary_session',
    )

    scoresheet_pdf = models.FileField(
        help_text="""
            The historical PDF OSS.""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    # Denormalizations
    @property
    def completed_rounds(self):
        return self.rounds.filter(status=self.rounds.model.STATUS.finished).count()

    # FKs
    convention = models.ForeignKey(
        'Convention',
        related_name='sessions',
        on_delete=models.CASCADE,
    )

    # Internals
    class Meta:
        unique_together = (
            ('convention', 'kind',),
        )

    class JSONAPIMeta:
        resource_name = "session"

    def __unicode__(self):
        return self.nomen

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: encoding.smart_text(x), [
                    self.convention,
                    self.get_kind_display(),
                ]
            )
        )
        super(Session, self).save(*args, **kwargs)

    # Methods
    # def print_oss(self):
    #     payload = {
    #         'id': str(self.id),
    #     }
    #     Channel('print-oss').send(payload)

    # def print_oss(self):
    #     session = self
    #     performers = session.performers.exclude(
    #         rank=None,
    #     ).order_by(
    #         '-total_points',
    #         '-sng_points',
    #         '-mus_points',
    #         '-prs_points',
    #     )
    #     assignments = session.assignments.order_by(
    #         'category',
    #         'kind',
    #         'slot',
    #     )
    #     foo = get_template('oss.html')
    #     template = foo.render(context={
    #         'session': session,
    #         'performers': performers,
    #         'assignments': assignments,
    #     })
    #     try:
    #         create_response = doc_api.create_doc({
    #             "test": True,
    #             "document_content": template,
    #             "name": "oss-{0}.pdf".format(id),
    #             "document_type": "pdf",
    #         })
    #         f = ContentFile(create_response)
    #         session.scoresheet_pdf.save(
    #             "{0}.pdf".format(id),
    #             f
    #         )
    #         session.save()
    #         log.info("PDF created and saved to instance")
    #     except docraptor.rest.ApiException as error:
    #         log.exception(error)
    #         log.exception(error.message)
    #         log.exception(error.code)
    #         log.exception(error.response_body)
    #     return "Complete"

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        if request.user.is_authenticated():
            return any([
                True,
                # self.assignments.filter(
                #     judge__user=request.user,
                #     category=self.assignments.model.CATEGORY.admin,
                # ),
            ])
        return False

    # Transitions
    @transition(field=status, source='*', target=STATUS.opened)
    def open(self, *args, **kwargs):
        return

    @transition(field=status, source='*', target=STATUS.closed)
    def close(self, *args, **kwargs):
        return

    @transition(field=status, source='*', target=STATUS.validated)
    def validate(self, *args, **kwargs):
        return

    @transition(field=status, source='*', target=STATUS.started)
    def start(self, *args, **kwargs):
        return

    @transition(field=status, source='*', target=STATUS.finished)
    def finish(self, *args, **kwargs):
        session = self
        for performer in session.performers.all():
            for performance in performer.performances.all():
                for song in performance.songs.all():
                    song.calculate()
                    song.save()
                performance.calculate()
                performance.save()
            performer.calculate()
            performer.save()
        return

    @transition(field=status, source='*', target=STATUS.published)
    def publish(self, *args, **kwargs):
        return


class Slot(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        null=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    num = models.IntegerField(
    )

    location = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    photo = models.DateTimeField(
        null=True,
        blank=True,
    )

    arrive = models.DateTimeField(
        null=True,
        blank=True,
    )

    depart = models.DateTimeField(
        null=True,
        blank=True,
    )

    backstage = models.DateTimeField(
        null=True,
        blank=True,
    )

    onstage = models.DateTimeField(
        null=True,
        blank=True,
    )

    # FKs
    round = models.ForeignKey(
        'Round',
        related_name='slots',
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (
            ('round', 'num',),
        )

    class JSONAPIMeta:
        resource_name = "slot"

    def __unicode__(self):
        return self.nomen

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: encoding.smart_text(x), [
                    self.round,
                    self.num,
                ]
            )
        )
        super(Slot, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


class Song(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        null=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'validated', 'Validated',),
        # (20, 'entered', 'Entered',),
        # (30, 'flagged', 'Flagged',),
        # (35, 'validated', 'Validated',),
        (38, 'finished', 'Finished',),
        (40, 'confirmed', 'Confirmed',),
        (50, 'final', 'Final',),
        (90, 'published', 'Published',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    num = models.IntegerField(
    )

    # FKs
    performance = models.ForeignKey(
        'Performance',
        related_name='songs',
        on_delete=models.CASCADE,
    )

    submission = models.ForeignKey(
        'Submission',
        related_name='songs',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # Internals
    class Meta:
        unique_together = (
            ('performance', 'num',),
        )

    class JSONAPIMeta:
        resource_name = "song"

    def __unicode__(self):
        return self.nomen

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: encoding.smart_text(x), [
                    self.performance,
                    self.num,
                ]
            )
        )
        super(Song, self).save(*args, **kwargs)

    def calculate(self, *args, **kwargs):
        self.songscore.calculate()
        self.songscore.save()
        return

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False

    # Transitions
    @transition(field=status, source='*', target=STATUS.published)
    def publish(self, *args, **kwargs):
        return


class SongScore(Song):
    rank = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_points = models.IntegerField(
        null=True,
        blank=True,
    )

    prs_points = models.IntegerField(
        null=True,
        blank=True,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
    )

    total_points = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
    )

    prs_score = models.FloatField(
        null=True,
        blank=True,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
    )

    total_score = models.FloatField(
        null=True,
        blank=True,
    )

    # Internals
    class JSONAPIMeta:
        resource_name = "songscore"

    # Methods
    def calculate(self, *args, **kwargs):
        self.mus_points = self.calculate_mus_points()
        self.prs_points = self.calculate_prs_points()
        self.sng_points = self.calculate_sng_points()
        self.total_points = self.calculate_total_points()
        self.mus_score = self.calculate_mus_score()
        self.prs_score = self.calculate_prs_score()
        self.sng_score = self.calculate_sng_score()
        self.total_score = self.calculate_total_score()

    def calculate_mus_points(self):
        return self.scores.filter(
            kind=self.scores.model.KIND.official,
            category=self.scores.model.CATEGORY.music,
        ).aggregate(
            tot=models.Sum('points')
        )['tot']

    def calculate_prs_points(self):
        return self.scores.filter(
            kind=self.scores.model.KIND.official,
            category=self.scores.model.CATEGORY.presentation,
        ).aggregate(
            tot=models.Sum('points')
        )['tot']

    def calculate_sng_points(self):
        return self.scores.filter(
            kind=self.scores.model.KIND.official,
            category=self.scores.model.CATEGORY.singing,
        ).aggregate(
            tot=models.Sum('points')
        )['tot']

    def calculate_total_points(self):
        return self.scores.filter(
            kind=self.scores.model.KIND.official,
        ).aggregate(
            tot=models.Sum('points')
        )['tot']

    def calculate_mus_score(self):
        return self.scores.filter(
            kind=self.scores.model.KIND.official,
            category=self.scores.model.CATEGORY.music,
        ).aggregate(
            tot=models.Avg('points')
        )['tot']

    def calculate_prs_score(self):
        return self.scores.filter(
            kind=self.scores.model.KIND.official,
            category=self.scores.model.CATEGORY.presentation,
        ).aggregate(
            tot=models.Avg('points')
        )['tot']

    def calculate_sng_score(self):
        return self.scores.filter(
            kind=self.scores.model.KIND.official,
            category=self.scores.model.CATEGORY.singing,
        ).aggregate(
            tot=models.Avg('points')
        )['tot']

    def calculate_total_score(self):
        return self.scores.filter(
            kind=self.scores.model.KIND.official,
        ).aggregate(
            tot=models.Avg('points')
        )['tot']

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        if request.user.is_authenticated():
            # return any([
            #     self.performer.session.assignments.filter(
            #         # judge__user=request.user,
            #         category=self.round.session.assignments.model.category.ADMIN,
            #     ),
            #     self.performer.group.roles.filter(
            #         person__user=request.user,
            #         status=self.performer.roles.model.STATUS.active,
            #     ),
            # ])
            return True
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        if request.user.is_authenticated():
            # return any([
            #     self.performer.session.assignments.filter(
            #         # judge__user=request.user,
            #         category=self.round.session.assignments.model.category.ADMIN,
            #     ),
            #     self.performer.group.roles.filter(
            #         person__user=request.user,
            #         status=self.performer.roles.model.STATUS.active,
            #     ),
            # ])
            return True
        return False


class Submission(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        null=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'pre', 'Pre-Submitted',),
        (20, 'post', 'Post-Submitted',),
        (30, 'validated', 'Validated',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    title = models.CharField(
        help_text="""
            Title of the composition.
        """,
        max_length=200,
    )

    bhs_catalog = models.IntegerField(
        help_text="""
            The BHS Catalog Number.
        """,
        null=True,
        blank=True,
    )

    is_medley = models.BooleanField(
        default=False,
    )

    is_parody = models.BooleanField(
        default=False,
    )

    arrangers = models.TextField(
        help_text="""
            Names of the Arranger(s).
        """,
        null=True,
        blank=True,
    )

    composers = models.TextField(
        help_text="""
            Names of the Composer(s) and/or Lyricist(s).
        """,
        null=True,
        blank=True,
    )

    holders = models.TextField(
        help_text="""
            Names of the Copyright Holder(s).
        """,
        null=True,
        blank=True,
    )

    # FKs
    performer = models.ForeignKey(
        'Performer',
        related_name='submissions',
        on_delete=models.CASCADE,
    )

    catalog = models.ForeignKey(
        'Catalog',
        related_name='submissions',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # Internals
    class Meta:
        unique_together = (
            ('performer', 'title',),
        )

    class JSONAPIMeta:
        resource_name = "submission"

    def __unicode__(self):
        return self.nomen

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: encoding.smart_text(x), [
                    self.performer,
                    self.title,
                ]
            )
        )
        super(Submission, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        if request.user.is_authenticated():
            return any([
                True,
                # self.performer.session.assignments.filter(
                #     judge__user=request.user,
                #     category=self.round.session.assignments.model.category.ADMIN,
                # ),
                # self.performer.group.roles.filter(
                #     person__user=request.user,
                #     status=self.performer.roles.model.STATUS.active,
                # ),
                # self.performer.session.assignments.filter(
                #     judge__user=request.user,
                # ),
                # self.performer.session.convention.drcj == request.user.person,
            ])
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        if request.user.is_authenticated():
            return any([
                True,
                # self.performer.session.assignments.filter(
                #     judge__user=request.user,
                #     category=self.round.session.assignments.model.category.ADMIN,
                # ),
                # self.performer.group.roles.filter(
                #     person__user=request.user,
                #     status=self.performer.roles.model.STATUS.active,
                # )
                # self.performer.session.assignments.filter(
                #     judge__user=request.user,
                # ),
                # self.performer.session.convention.drcj == request.user.person,
            ])
        return False


class Venue(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        null=True,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the resource.""",
        max_length=200,
    )

    STATUS = Choices(
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    location = models.CharField(
        max_length=255,
    )

    city = models.CharField(
        max_length=255,
    )

    state = models.CharField(
        max_length=255,
    )

    airport = models.CharField(
        max_length=3,
        null=True,
        blank=True,
    )

    timezone = TimeZoneField(
        help_text="""
            The local timezone of the venue.""",
    )

    # Methods
    def __unicode__(self):
        return self.nomen

    def save(self, *args, **kwargs):
        self.nomen = self.name
        super(Venue, self).save(*args, **kwargs)

    # Internals
    class JSONAPIMeta:
        resource_name = "venue"

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


class User(AbstractBaseUser):
    USERNAME_FIELD = settings.USERNAME_FIELD
    REQUIRED_FIELDS = settings.REQUIRED_FIELDS

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    username = models.CharField(
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    objects = UserManager()

    @property
    def is_superuser(self):
        return self.is_staff

    class JSONAPIMeta:
        resource_name = "user"

    # Methods
    def __unicode__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        if request.user.is_authenticated():
            return self == request.user
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        if request.user.is_authenticated():
            return self == request.user
        return False
