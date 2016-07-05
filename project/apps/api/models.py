# Future
from __future__ import division

# Standard Libary
import datetime
import logging
import os
import random
import uuid

# Third-Party
from channels import Channel
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
from phonenumber_field.modelfields import PhoneNumberField
from ranking import Ranking
from timezone_field import TimeZoneField

# Django
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.contrib.postgres.fields import (
    ArrayField,
    DateRangeField,
    DateTimeRangeField,
    FloatRangeField,
    IntegerRangeField,
)
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models

# Local
from .managers import (
    ScoreManager,
    UserManager,
)

# from django_fsm_log.decorators import fsm_log_by


# from django.core.exceptions import (
#     ValidationError,
# )


log = logging.getLogger(__name__)


def generate_image_filename(instance, filename):
    f, ext = os.path.splitext(filename)
    return '{0}{1}'.format(instance.id, ext)


class Award(TimeStampedModel):
    """
    Award Model.

    The specific award conferred by an organization.  Typically given once a year.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""Award Name (auto-generated).""",
        max_length=255,
        unique=True,
        editable=False,
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
        # (180, 'pb', 'Plateau B',),
        # (190, 'pi', 'Plateau I',),
        # (200, 'pii', 'Plateau II',),
        # (210, 'piii', 'Plateau III',),
        # (220, 'piv', 'Plateau IV',),
        # (230, 'small', 'Small',),
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
        help_text="""No secondary award critera.""",
        default=False,
    )

    is_improved = models.BooleanField(
        help_text="""Designates 'Most-Improved'.  Implies manual.""",
        default=False,
    )

    is_novice = models.BooleanField(
        default=False,
    )

    is_manual = models.BooleanField(
        help_text="""Award must be determined manually.""",
        default=False,
    )

    idiom = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    is_multi = models.BooleanField(
        help_text="""Award spans conventions; must be determined manually.""",
        default=False,
    )

    championship_rounds = models.IntegerField(
        help_text="""Number of rounds to determine the championship""",
    )

    is_qualification_required = models.BooleanField(
        help_text="""Boolean; true means qualification is required.""",
        default=False,
    )

    is_district_representative = models.BooleanField(
        help_text="""Boolean; true means the district rep qualifies.""",
        default=False,
    )

    qualifier_rounds = models.IntegerField(
        help_text="""Number of rounds to qualify for the award.""",
        null=True,
        blank=True,
    )

    threshold = models.FloatField(
        help_text="""The score threshold for automatic qualification (if any.)""",
        null=True,
        blank=True,
    )

    minimum = models.FloatField(
        help_text="""The minimum score required for qualification (if any.)""",
        null=True,
        blank=True,
    )

    advance = models.FloatField(
        help_text="""The score threshold to advance to next round (if any) in multi-round qualification.""",
        null=True,
        blank=True,
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

    # FKs
    organization = TreeForeignKey(
        'Organization',
        related_name='awards',
        on_delete=models.CASCADE,
    )

    # Denormalization
    LEVEL = Choices(
        (0, 'international', "International"),
        (1, 'district', "District"),
        (2, 'division', "Division"),
        (3, 'chapter', "Chapter"),
    )

    level = models.IntegerField(
        choices=LEVEL,
        editable=False,
    )

    # Internals
    class Meta:
        unique_together = (
            (
                'organization',
                'is_improved',
                'is_novice',
                'size',
                'scope',
                'idiom',
                'kind',
            ),
        )

    class JSONAPIMeta:
        resource_name = "award"

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.level = self.organization.level
        if self.is_improved:
            most_improved = 'Most-Improved'
        else:
            most_improved = None
        if self.is_novice:
            novice = 'Novice'
        else:
            novice = None
        self.name = " ".join(filter(None, [
            self.organization.name,
            most_improved,
            novice,
            self.get_size_display(),
            self.get_scope_display(),
            self.idiom,
            self.get_kind_display(),
        ]))
        super(Award, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


class Certification(TimeStampedModel):
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

    CATEGORY = Choices(
        (0, 'admin', 'Admin'),
        (1, 'music', 'Music'),
        (2, 'presentation', 'Presentation'),
        (3, 'singing', 'Singing'),
    )

    category = models.IntegerField(
        choices=CATEGORY,
    )

    date = DateRangeField(
        help_text="""
            The active dates of the resource.""",
        null=True,
        blank=True,
    )

    # FKs
    person = models.ForeignKey(
        'Person',
        related_name='certifications',
        on_delete=models.CASCADE,
    )

    # Internals
    class Meta:
        unique_together = (
            ('category', 'person',),
        )

    class JSONAPIMeta:
        resource_name = "certification"

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} - {1}".format(
            self.person,
            self.get_category_display(),
        )
        super(Certification, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


class Chapter(TimeStampedModel):
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
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'inactive', 'Inactive',),
        (30, 'affiliate', 'Affiliate',),
        (50, 'dup', 'Duplicate',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    code = models.CharField(
        help_text="""
            The chapter code.""",
        unique=True,
        max_length=200,
        blank=True,
        null=True,
    )

    # FKs
    organization = TreeForeignKey(
        'Organization',
        related_name='chapters',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # Legacy
    bhs_id = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
    )

    bhs_name = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_chapter_name = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_group_name = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_chapter_code = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_website = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_district = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_venue = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_address = models.CharField(
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

    bhs_zip = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_contact = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_phone = models.CharField(
        max_length=255,
        blank=True,
    )

    # Internals
    class JSONAPIMeta:
        resource_name = "chapter"

    def __unicode__(self):
        return u"{0}".format(self.name)

    # Permissions
    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


class Chart(TimeStampedModel):
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

    STATUS = Choices(
        (0, 'new', 'New'),
        (10, 'active', 'Active'),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    is_generic = models.BooleanField(
        default=False,
    )

    is_parody = models.BooleanField(
        default=False,
    )

    is_medley = models.BooleanField(
        default=False,
    )

    title = models.CharField(
        max_length=200,
    )

    arranger = models.CharField(
        blank=True,
        max_length=200,
    )

    composer = models.CharField(
        blank=True,
        max_length=200,
    )

    lyricist = models.CharField(
        blank=True,
        max_length=200,
    )

    # Legacy
    bhs_id = models.IntegerField(
        null=True,
        blank=True,
        unique=True,
    )

    bhs_marketplace = models.IntegerField(
        null=True,
        blank=True,
        unique=True,
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

    bhs_songname = models.CharField(
        blank=True,
        max_length=200,
    )

    bhs_copyright_date = models.CharField(
        blank=True,
        max_length=200,
    )

    bhs_copyright_owner = models.CharField(
        blank=True,
        max_length=200,
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

    # Internals
    class Meta:
        unique_together = (
            ('title', 'bhs_marketplace',),
        )

    class JSONAPIMeta:
        resource_name = "chart"

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        if self.bhs_marketplace:
            bhs_marketplace = "[{0}]".format(self.bhs_marketplace)
        else:
            bhs_marketplace = None
        self.name = " ".join(filter(None, [
            self.title,
            bhs_marketplace,
        ]))
        super(Chart, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


class Contest(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=200,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        # (20, 'started', 'Started',),
        # # (25, 'ranked', 'Ranked',),
        # (30, 'finished', 'Finished',),
        # (40, 'drafted', 'Drafted',),
        (10, 'opened', 'Opened',),
        (15, 'closed', 'Closed',),
        (35, 'validated', 'Validated',),
        (42, 'finished', 'Finished',),
        (45, 'published', 'Published',),
        # (50, 'final', 'Final',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    CYCLE_CHOICES = []
    for r in reversed(range(1939, (datetime.datetime.now().year + 2))):
        CYCLE_CHOICES.append((r, r))

    cycle = models.IntegerField(
        choices=CYCLE_CHOICES,
        editable=False,
    )

    is_qualifier = models.BooleanField(
        default=False,
    )

    num_rounds = models.IntegerField(
        null=True,
        blank=True,
    )

    # Denormalization
    champion = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        editable=False,
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

    champion = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        editable=False,
    )

    # Legacy
    stix_num = models.IntegerField(
        null=True,
        blank=True,
    )

    stix_name = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )

    # Internals
    class Meta:
        unique_together = (
            ('session', 'award',)
        )

    class JSONAPIMeta:
        resource_name = "contest"

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        if self.session.convention.season == self.session.convention.SEASON.spring:
            self.cycle = self.session.convention.year
        else:
            self.cycle = self.session.convention.year + 1
        if self.is_qualifier:
            suffix = "Qualifier"
        else:
            suffix = "Championship"
        self.name = " ".join(filter(None, [
            self.award.name,
            suffix,
            str(self.session.convention.year),
        ]))
        # if self.is_qualifier:
        #     champion = None
        # else:
        #     try:
        #         champion = self.contestants.get(rank=1).performer.group.name
        #     except self.contestants.model.DoesNotExist:
        #         champion = None
        #     except self.contestants.model.MultipleObjectsReturned:
        #         champion = self.contestants.filter(rank=1).order_by(
        #             '-sng_points',
        #             '-mus_points',
        #             '-prs_points',
        #         ).first().performer.group.name
        self.champion = None
        super(Contest, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False

    # Methods
    def ranking(self, point_total):
        if not point_total:
            return None
        contestants = self.contestants.all()
        points = [contestant.calculate_total_points() for contestant in contestants]
        points = sorted(points, reverse=True)
        ranking = Ranking(points, start=1)
        rank = ranking.rank(point_total)
        return rank

    # Transitions
    @transition(field=status, source='*', target=STATUS.finished)
    def finish(self, *args, **kwargs):
        return


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

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'eligible', 'Eligible',),
        (20, 'ineligible', 'Ineligible',),
        # (30, 'dnq', 'Did Not Qualify',),
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

    # Internals
    class Meta:
        unique_together = (
            ('performer', 'contest',),
        )

    class JSONAPIMeta:
        resource_name = "contestant"

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.contest.award.name,
            str(self.performer.session.convention.year),
            self.performer.name,
        ]))
        super(Contestant, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False

    # Methods
    def calculate_rank(self):
        return self.contest.ranking(self.calculate_total_points())

    def calculate_mus_points(self):
        return self.performer.performances.filter(
            songs__scores__kind=self.contest.session.judges.model.KIND.official,
            songs__scores__category=self.contest.session.judges.model.CATEGORY.music,
            round__num__lte=self.contest.num_rounds,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_prs_points(self):
        return self.performer.performances.filter(
            songs__scores__kind=self.contest.session.judges.model.KIND.official,
            songs__scores__category=self.contest.session.judges.model.CATEGORY.presentation,
            round__num__lte=self.contest.num_rounds,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_sng_points(self):
        return self.performer.performances.filter(
            songs__scores__kind=self.contest.session.judges.model.KIND.official,
            songs__scores__category=self.contest.session.judges.model.CATEGORY.singing,
            round__num__lte=self.contest.num_rounds,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_total_points(self):
        return self.performer.performances.filter(
            songs__scores__kind=self.contest.session.judges.model.KIND.official,
            round__num__lte=self.contest.num_rounds,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_mus_score(self):
        return self.performer.performances.filter(
            songs__scores__kind=self.contest.session.judges.model.KIND.official,
            songs__scores__category=self.contest.session.judges.model.CATEGORY.music,
            round__num__lte=self.contest.num_rounds,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_prs_score(self):
        return self.performer.performances.filter(
            songs__scores__kind=self.contest.session.judges.model.KIND.official,
            songs__scores__category=self.contest.session.judges.model.CATEGORY.presentation,
            round__num__lte=self.contest.num_rounds,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_sng_score(self):
        return self.performer.performances.filter(
            songs__scores__kind=self.contest.session.judges.model.KIND.official,
            songs__scores__category=self.contest.session.judges.model.CATEGORY.singing,
            round__num__lte=self.contest.num_rounds,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_total_score(self):
        return self.performer.performances.filter(
            songs__scores__kind=self.contest.session.judges.model.KIND.official,
            round__num__lte=self.contest.num_rounds,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

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


class Convention(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
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
        (10, 'international', 'International'),
        (20, 'district', 'District'),
        (30, 'division', 'Division'),
        (40, 'disdiv', 'District and Division'),
        (200, 'evgd1', "EVG Division I"),
        (210, 'evgd2', "EVG Division II"),
        (220, 'evgd3', "EVG Division III"),
        (230, 'evgd4', "EVG Division IV"),
        (240, 'evgd5', "EVG Division V"),
        (250, 'fwdaz', "FWD Arizona Division"),
        (260, 'fwdnenw', "FWD NE/NW Divisions"),
        (270, 'fwdsesw', "FWD SE/SW Divisions"),
        (280, 'lolp1', "LOL Division One/Packerland Divisions"),
        (290, 'lolnp', "LOL Northern Plains Division"),
        (300, 'lol10sw', "LOL 10,000 Lakes and Southwest Divisions"),
        # (310, 'madatl', "Atlantic Division"),  <- LEGACY
        # (320, 'madnw', "Northern and Western Divisions"), <- LEGACY
        (322, 'madnth', "MAD Northern Division"),
        (324, 'madcen', "MAD Central Division"),
        (330, 'madsth', "MAD Southern Division"),
        (340, 'nedsun', "NED Sunrise Division"),
        (342, 'nedwst', "NED Western Regional"),
        (344, 'nedest', "NED Eastern Regional"),
        (350, 'swdnenwsesw', "SWD NE/NW/SE/SW Divisions"),
    )

    kind = models.IntegerField(
        choices=KIND,
        null=True,
        blank=True,
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
        null=True,
        blank=True,
        # editable=False,
    )

    date = DateTimeRangeField(
        help_text="""
            The scheduled time frame for the convention.""",
        null=True,
        blank=True,
    )

    is_prelims = models.BooleanField(
        default=False,
    )

    # FKs
    venue = models.ForeignKey(
        'Venue',
        null=True,
        blank=True,
        related_name='conventions',
        help_text="""
            The venue for the convention.""",
        on_delete=models.SET_NULL,
    )

    organization = TreeForeignKey(
        'Organization',
        help_text="""
            The organization hosting the convention.""",
        related_name='conventions',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    drcj = models.ForeignKey(
        'Person',
        null=True,
        blank=True,
        related_name='conventions',
        help_text="""
            The person managing the convention.""",
        on_delete=models.CASCADE,
    )

    # Denormalization
    LEVEL = Choices(
        (0, 'international', "International"),
        (1, 'district', "District"),
        (2, 'division', "Division"),
        (3, 'chapter', "Chapter"),
    )

    level = models.IntegerField(
        choices=LEVEL,
        null=True,
        blank=True,
        editable=False,
    )

    # Legacy
    bhs_id = models.IntegerField(
        null=True,
        blank=True,
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

    # Internals
    class Meta:
        unique_together = (
            ('organization', 'season', 'year', 'kind',),
        )

    class JSONAPIMeta:
        resource_name = "convention"

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        if self.kind > self.KIND.disdiv:
            org = None
        else:
            org = str(self.organization.short_name)
        if self.season == self.SEASON.summer:
            season = None
        else:
            season = self.get_season_display()

        self.name = " ".join(filter(None, [
            org,
            str(self.get_kind_display()),
            season,
            u"Convention",
            str(self.year),
        ]))
        super(Convention, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False

    # Transitions
    @transition(field=status, source='*', target=STATUS.started)
    def start(self, *args, **kwargs):
        return

    @transition(field=status, source='*', target=STATUS.finished)
    def finish(self, *args, **kwargs):
        return


class Group(TimeStampedModel):
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
    )

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

    KIND = Choices(
        (1, 'quartet', 'Quartet'),
        (2, 'chorus', 'Chorus'),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of group; choices are Quartet or Chorus.""",
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

    phone = PhoneNumberField(
        help_text="""
            The phone number of the resource.  Include country code.""",
        blank=True,
        default='',
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

    # FKs
    chapter = models.ForeignKey(
        'Chapter',
        related_name='groups',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    organization = models.ForeignKey(
        'Organization',
        related_name='groups',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # Denormalizations
    chap_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        editable=False,
    )

    # Legacy
    bhs_id = models.IntegerField(
        unique=True,
        null=True,
        blank=True,
    )

    bhs_name = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_chapter_name = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_chapter_code = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_website = models.CharField(
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

    bhs_phone = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_expiration = models.CharField(
        max_length=255,
        blank=True,
    )

    # Internals
    class JSONAPIMeta:
        resource_name = "group"

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        if self.kind == self.KIND.chorus:
            try:
                self.chap_name = u"{0} {1} - {2} {3}".format(
                    self.chapter.code,
                    self.chapter.name,
                    self.name,
                    self.bhs_id,
                )
            except AttributeError:
                self.chap_name = u"{0} {1}".format(
                    self.name,
                    self.bhs_id,
                )
        else:
            self.chap_name = u"{0} {1}".format(
                self.name,
                self.bhs_id,
            )
        super(Group, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


class Judge(TimeStampedModel):
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

    STATUS = Choices(
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

    # FKs
    session = models.ForeignKey(
        'Session',
        related_name='judges',
        on_delete=models.CASCADE,
    )

    certification = models.ForeignKey(
        'Certification',
        related_name='judges',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    organization = TreeForeignKey(
        'Organization',
        related_name='judges',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # Denormalizations
    @property
    def designation(self):
        designation = u"{0[0]}{1:1d}".format(
            self.get_category_display(),
            self.slot,
        )
        return designation

    # Legacy
    bhs_panel_id = models.IntegerField(
        null=True,
        blank=True,
    )

    # Internals
    class Meta:
        unique_together = (
            ('session', 'category', 'kind', 'slot'),
        )

    class JSONAPIMeta:
        resource_name = "judge"

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        # Very hacky slot designator
        if not self.slot:
            try:
                self.slot = self.__class__.objects.filter(
                    session=self.session,
                    category=self.category,
                    kind=self.kind,
                ).aggregate(
                    max=models.Max('slot')
                )['max'] + 1
            except TypeError:
                if self.kind == self.KIND.practice:
                    self.slot = 6
                else:
                    self.slot = 1
        self.name = u"{0} {1} {2} {3}".format(
            self.session,
            self.get_kind_display(),
            self.get_category_display(),
            self.slot,
        )
        super(Judge, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


class Member(TimeStampedModel):
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

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'inactive', 'Inactive',),
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    # FKs
    chapter = models.ForeignKey(
        'Chapter',
        related_name='members',
        on_delete=models.CASCADE,
    )

    person = models.ForeignKey(
        'Person',
        related_name='members',
        on_delete=models.CASCADE,
    )

    # Internals
    class Meta:
        unique_together = (
            ('chapter', 'person',),
        )

    class JSONAPIMeta:
        resource_name = "member"

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.chapter.name,
            self.person.name,
        ]))
        super(Member, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


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

    LEVEL = Choices(
        (0, 'international', "International"),
        (1, 'district', "District/Affiliates"),
        (2, 'division', "Division"),
        (3, 'chapter', "Chapter"),
    )

    level = models.IntegerField(
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
        ('Chapter', [
            (60, 'chapter', "Chapter"),
        ]),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of organization.""",
        choices=KIND,
        null=True,
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

    code = models.CharField(
        help_text="""
            The chapter code.""",
        max_length=200,
        blank=True,
        null=True,
    )

    spots = models.IntegerField(
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

    # FKs
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        on_delete=models.SET_NULL,
    )

    representative = models.ForeignKey(
        'Person',
        related_name='organizations',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    # Legacy
    bhs_id = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
    )

    bhs_name = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_chapter_name = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_group_name = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_chapter_code = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_website = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_district = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_venue = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_address = models.CharField(
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

    bhs_zip = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_contact = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_phone = models.CharField(
        max_length=255,
        blank=True,
    )

    # Internals
    class Meta:
        unique_together = (
            ('level', 'kind', 'name')
        )

    class MPTTMeta:
        order_insertion_by = [
            'level',
            'kind',
            'name',
        ]

    class JSONAPIMeta:
        resource_name = "organization"

    def __unicode__(self):
        return u"{0}".format(self.name)

    # Permissions
    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


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

    STATUS = Choices(
        (0, 'new', 'New',),
        (5, 'validated', 'Validated',),
        (10, 'started', 'Started',),
        (20, 'finished', 'Finished',),
        (30, 'entered', 'Entered',),
        # (50, 'confirmed', 'Confirmed',),
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

    slot = models.ForeignKey(
        'Slot',
        unique=True,
        null=True,
        blank=True,
        related_name='performances',
        on_delete=models.SET_NULL,
    )

    # Denormalized
    rank = models.IntegerField(
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

    class Meta:
        ordering = [
            'round__kind',
        ]

    class JSONAPIMeta:
        resource_name = "performance"

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.round.session.convention.organization.name,
            str(self.round.session.convention.get_kind_display()),
            self.round.session.convention.get_season_display(),
            self.round.session.get_kind_display(),
            self.round.get_kind_display(),
            str(self.round.session.convention.year),
            "Performance",
            self.id.hex,
        ]))
        super(Performance, self).save(*args, **kwargs)

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

    # Permissions
    @staticmethod
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        if self.status >= self.STATUS.validated:
            return True
        else:
            return False

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False

    # Denormalizations
    def calculate_rank(self):
        return self.round.ranking(self.calculate_total_points())

    def calculate_mus_points(self):
        return self.songs.filter(
            scores__kind=self.round.session.judges.model.KIND.official,
            scores__category=self.round.session.judges.model.CATEGORY.music,
        ).aggregate(
            tot=models.Sum('scores__points')
        )['tot']

    def calculate_prs_points(self):
        return self.songs.filter(
            scores__kind=self.round.session.judges.model.KIND.official,
            scores__category=self.round.session.judges.model.CATEGORY.presentation,
        ).aggregate(
            tot=models.Sum('scores__points')
        )['tot']

    def calculate_sng_points(self):
        return self.songs.filter(
            scores__kind=self.round.session.judges.model.KIND.official,
            scores__category=self.round.session.judges.model.CATEGORY.singing,
        ).aggregate(
            tot=models.Sum('scores__points')
        )['tot']

    def calculate_total_points(self):
        return self.songs.filter(
            scores__kind=self.round.session.judges.model.KIND.official,
        ).aggregate(
            tot=models.Sum('scores__points')
        )['tot']

    def calculate_mus_score(self):
        return self.songs.filter(
            scores__kind=self.round.session.judges.model.KIND.official,
            scores__category=self.round.session.judges.model.CATEGORY.music,
        ).aggregate(
            tot=models.Avg('scores__points')
        )['tot']

    def calculate_prs_score(self):
        return self.songs.filter(
            scores__kind=self.round.session.judges.model.KIND.official,
            scores__category=self.round.session.judges.model.CATEGORY.presentation,
        ).aggregate(
            tot=models.Avg('scores__points')
        )['tot']

    def calculate_sng_score(self):
        return self.songs.filter(
            scores__kind=self.round.session.judges.model.KIND.official,
            scores__category=self.round.session.judges.model.CATEGORY.singing,
        ).aggregate(
            tot=models.Avg('scores__points')
        )['tot']

    def calculate_total_score(self):
        return self.songs.filter(
            scores__kind=self.round.session.judges.model.KIND.official,
        ).aggregate(
            tot=models.Avg('scores__points')
        )['tot']

    # Transitions
    # def scratch(self):
    #     i = self.slot
    #     self.slot = -1
    #     self.save()
    #     performances = self.round.performances.filter(
    #         slot__gt=i,
    #     ).order_by('slot')
    #     for performance in performances:
    #         performance.slot -= 1
    #         performance.save()
    #     self.performer.status = self.performer.STATUS.dropped
    #     self.performer.save()
    #     self.delete()
    #     return {'success': 'scratched'}

    # def build(self):
    #     i = 1
    #     while i <= 2:
    #         song, c = self.songs.get_or_create(
    #             performance=self,
    #             order=i,
    #         )
    #         for judge in self.round.session.judges.all():
    #             song.scores.get_or_create(
    #                 song=song,
    #                 judge=judge,
    #                 category=judge.category,
    #                 kind=judge.kind,
    #             )
    #         i += 1
    #     return

    @transition(field=status, source='*', target=STATUS.started)
    def start(self, *args, **kwargs):
        return

    @transition(field=status, source='*', target=STATUS.finished)
    def finish(self, *args, **kwargs):
        return

    @transition(field=status, source='*', target=STATUS.published)
    def publish(self, *args, **kwargs):
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

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'registered', 'Registered',),
        (20, 'accepted', 'Accepted',),
        (30, 'declined', 'Declined',),
        (40, 'dropped', 'Dropped',),
        # (45, 'evaluation', 'Evaluation',),
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

    notification = models.EmailField(
        null=True,
        blank=True,
    )

    # FKs
    session = models.ForeignKey(
        'Session',
        related_name='performers',
        on_delete=models.CASCADE,
    )

    group = models.ForeignKey(
        'Group',
        related_name='performers',
        on_delete=models.CASCADE,
    )

    tenor = models.ForeignKey(
        'Role',
        null=True,
        blank=True,
        related_name='performers_tenor',
        on_delete=models.SET_NULL,
    )

    lead = models.ForeignKey(
        'Role',
        null=True,
        blank=True,
        related_name='performers_lead',
        on_delete=models.SET_NULL,
    )

    baritone = models.ForeignKey(
        'Role',
        null=True,
        blank=True,
        related_name='performers_baritone',
        on_delete=models.SET_NULL,
    )

    bass = models.ForeignKey(
        'Role',
        null=True,
        blank=True,
        related_name='performers_bass',
        on_delete=models.SET_NULL,
    )

    director = models.ForeignKey(
        'Role',
        null=True,
        blank=True,
        related_name='performers_director',
        on_delete=models.SET_NULL,
    )

    codirector = models.ForeignKey(
        'Role',
        null=True,
        blank=True,
        related_name='performers_codirector',
        on_delete=models.SET_NULL,
    )

    representing = TreeForeignKey(
        'Organization',
        related_name='performers',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # Denormalized
    seed = models.IntegerField(
        help_text="""
            The incoming rank based on prelim score.""",
        null=True,
        blank=True,
        editable=False,
    )

    prelim = models.FloatField(
        help_text="""
            The incoming prelim score.""",
        null=True,
        blank=True,
    )

    rank = models.IntegerField(
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

    # Legacy
    bhs_id = models.IntegerField(
        null=True,
        blank=True,
    )

    # Internals
    class Meta:
        unique_together = (
            ('group', 'session',),
        )

    class JSONAPIMeta:
        resource_name = "performer"

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.session.convention.organization.name,
            str(self.session.convention.get_kind_display()),
            self.session.convention.get_season_display(),
            str(self.session.convention.year),
            self.session.get_kind_display(),
            "Performer",
            self.group.name,
            self.group.id.hex,
        ]))
        super(Performer, self).save(*args, **kwargs)

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

    # def clean(self):
    #     if self.singers.count() > 4:
    #         raise ValidationError('There can not be more than four persons in a quartet.')

    # Permissions
    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False

    # Methods
    def calculate_rank(self):
        try:
            return self.contestants.get(contest=self.session.primary).calculate_rank()
        except self.contestants.model.DoesNotExist:
            return None

    def calculate_mus_points(self):
        return self.performances.filter(
            songs__scores__kind=self.session.judges.model.KIND.official,
            songs__scores__category=self.session.judges.model.CATEGORY.music,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_prs_points(self):
        return self.performances.filter(
            songs__scores__kind=self.session.judges.model.KIND.official,
            songs__scores__category=self.session.judges.model.CATEGORY.presentation,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_sng_points(self):
        return self.performances.filter(
            songs__scores__kind=self.session.judges.model.KIND.official,
            songs__scores__category=self.session.judges.model.CATEGORY.singing,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_total_points(self):
        return self.performances.filter(
            songs__scores__kind=self.session.judges.model.KIND.official,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_mus_score(self):
        return self.performances.filter(
            songs__scores__kind=self.session.judges.model.KIND.official,
            songs__scores__category=self.session.judges.model.CATEGORY.music,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_prs_score(self):
        return self.performances.filter(
            songs__scores__kind=self.session.judges.model.KIND.official,
            songs__scores__category=self.session.judges.model.CATEGORY.presentation,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_sng_score(self):
        return self.performances.filter(
            songs__scores__kind=self.session.judges.model.KIND.official,
            songs__scores__category=self.session.judges.model.CATEGORY.singing,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_total_score(self):
        return self.performances.filter(
            songs__scores__kind=self.session.judges.model.KIND.official,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def notify_performer(self, subject, body):
        payload = {
            'subject': subject,
            'body': body,
            'to': [self.notification],
        }
        Channel('send-email').send(payload)

    # Transitions
    @transition(field=status, source='*', target=STATUS.validated)
    def validate(self, *args, **kwargs):
        return

    # @transition(field=status, source='*', target=STATUS.scratched)
    # def scratch(self, *args, **kwargs):
    #     performances = self.performances.exclude(
    #         status=self.performances.model.STATUS.final,
    #     )
    #     for performance in performances:
    #         i = performance.slot
    #         performance.slot = -1
    #         performance.save()
    #         others = performance.round.performances.filter(
    #             slot__gt=i,
    #         ).order_by('slot')
    #         for other in others:
    #             other.slot -= 1
    #             other.save()
    #         performance.delete()
    #     self.save()
    #     return {'success': 'scratched'}

    # @transition(field=status, source='*', target=STATUS.disqualified)
    # def disqualify(self, *args, **kwargs):
    #     performances = self.performances.exclude(
    #         status=self.performances.model.STATUS.final,
    #     )
    #     for performance in performances:
    #         i = performance.slot
    #         performance.slot = -1
    #         performance.save()
    #         others = performance.round.performances.filter(
    #             slot__gt=i,
    #         ).order_by('slot')
    #         for other in others:
    #             other.slot -= 1
    #             other.save()
    #     self.save()
    #     return {'success': 'disqualified'}

    @transition(field=status, source='*', target=STATUS.started)
    def start(self, *args, **kwargs):
        return

    @transition(field=status, source='*', target=STATUS.finished)
    def finish(self, *args, **kwargs):
        return


class Person(TimeStampedModel):
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
    )

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

    birth_date = models.DateField(
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

    phone = PhoneNumberField(
        help_text="""
            The phone number of the resource.  Include country code.""",
        blank=True,
        default='',
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

    # FKs
    organization = TreeForeignKey(
        'Organization',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    chapter = models.ForeignKey(
        'Chapter',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
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

    id_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        editable=False,
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

    # Legacy
    bhs_id = models.IntegerField(
        null=True,
        blank=True,
        unique=True,
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

    # Internals
    class JSONAPIMeta:
        resource_name = "person"

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        name = HumanName(self.name)
        if name.nickname:
            self.common_name = " ".join(filter(None, [
                u"{0}".format(name.nickname),
                u"{0}".format(name.last),
                u"{0}".format(name.suffix),
            ]))
        else:
            self.common_name = u'{0}'.format(self.name)
        self.id_name = " ".join(filter(None, [
            str(self.bhs_id),
            self.name,
        ]))
        self.formal_name = " ".join(filter(None, [
            u'{0}'.format(name.first),
            u'{0}'.format(name.last),
            u'{0}'.format(name.suffix),
        ]))
        super(Person, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


class Role(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        editable=False,
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

    PART = Choices(
        (1, 'tenor', 'Tenor'),
        (2, 'lead', 'Lead'),
        (3, 'baritone', 'Baritone'),
        (4, 'bass', 'Bass'),
        (5, 'director', 'Director'),
    )

    part = models.IntegerField(
        choices=PART,
    )

    date = DateRangeField(
        help_text="""
            Active Dates""",
        null=True,
        blank=True,
    )

    # FKs
    group = models.ForeignKey(
        'Group',
        related_name='roles',
        on_delete=models.CASCADE,
    )

    person = models.ForeignKey(
        'Person',
        related_name='roles',
        on_delete=models.CASCADE,
    )

    # Legacy
    bhs_id = models.IntegerField(
        null=True,
        blank=True,
    )

    bhs_file = models.FileField(
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    # Internals
    class JSONAPIMeta:
        resource_name = "role"

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.group.name,
            self.person.name,
            self.get_part_display(),
        ]))
        super(Role, self).save(*args, **kwargs)

    # def clean(self):
    #     if all([
    #         self.performer.group.kind == Group.KIND.chorus,
    #         self.part != self.PART.director,
    #     ]):
    #         raise ValidationError('Choruses do not have quartet singers.')
    #     if all([
    #         self.performer.group.kind == Group.KIND.quartet,
    #         self.part == self.PART.director,
    #     ]):
    #         raise ValidationError('Quartets do not have directors.')
        # if self.part:
        #     if [s['part'] for s in self.performer.singers.values(
        #         'part'
        #     )].count(self.part) > 1:
        #         raise ValidationError('There can not be more than one of the same part in a quartet.')

    # Permissions
    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


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

    date = DateTimeRangeField(
        help_text="""
            The active dates of the resource.""",
        null=True,
        blank=True,
    )

    # FKs
    session = models.ForeignKey(
        'Session',
        related_name='rounds',
        on_delete=models.CASCADE,
    )

    mt = models.ForeignKey(
        'Group',
        related_name='mic_tester',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # Legacy
    stix_name = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )

    # Internals
    class Meta:
        unique_together = (
            ('session', 'kind',),
        )

    class JSONAPIMeta:
        resource_name = "round"

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.session.convention.organization.name,
            str(self.session.convention.get_kind_display()),
            self.session.convention.get_season_display(),
            self.session.get_kind_display(),
            self.get_kind_display(),
            str(self.session.convention.year),
        ]))
        super(Round, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        if self.status >= 10:
            return True
        else:
            return False

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False

    # Methods
    def ranking(self, point_total):
        if not point_total:
            return None
        performances = self.performances.all()
        points = [performance.calculate_total_points() for performance in performances]
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

    name = models.CharField(
        max_length=255,
        unique=True,
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

    # FKs
    song = models.ForeignKey(
        'Song',
        related_name='scores',
        on_delete=models.CASCADE,
    )

    judge = models.ForeignKey(
        'Judge',
        related_name='scores',
        on_delete=models.CASCADE,
    )

    # Managers
    objects = ScoreManager()

    # Internals
    class JSONAPIMeta:
        resource_name = "score"

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.id.hex,
        ]))
        super(Score, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return False

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False

    # Transitions
    @transition(field=status, source='*', target=RETURN_VALUE(STATUS.cleared, STATUS.flagged))
    def ck(self, *args, **kwargs):
        if self.points < 0:
            return self.STATUS.cleared
        else:
            return self.STATUS.flagged


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
            Collegiate and Senior sessions respectively.""",
        choices=KIND,
    )

    date = DateTimeRangeField(
        help_text="""
            The active dates of the session.""",
        null=True,
        blank=True,
    )

    num_rounds = models.IntegerField(
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

    # Denormalizations
    @property
    def completed_rounds(self):
        return self.rounds.filter(status=self.rounds.model.STATUS.finished).count()

    # Legacy
    scoresheet_pdf = models.FileField(
        help_text="""
            The historical PDF OSS.""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    entry_form = models.FileField(
        help_text="""
            The cj20 entry form.""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    song_list = models.FileField(
        help_text="""
            The cj20 song list.""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

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
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.organization = self.convention.organization
        if self.convention.kind:
            kind = str(self.convention.get_kind_display())
        else:
            kind = None
        self.name = " ".join(filter(None, [
            self.convention.organization.name,
            kind,
            self.convention.get_season_display(),
            self.get_kind_display(),
            "Session",
            str(self.convention.year),
        ]))
        super(Session, self).save(*args, **kwargs)

    # Methods
    def print_oss(self):
        payload = {
            'pk': str(self.pk),
        }
        Channel('print-oss').send(payload)

    # Permissions
    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
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

    name = models.CharField(
        max_length=255,
        unique=True,
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
        default=1,
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
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.id.hex,
            self.round.name,
            str(self.num),
        ]))
        super(Slot, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


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
        blank=True,
        null=True,
    )

    is_parody = models.BooleanField(
        default=False,
    )

    # FKs
    submission = models.ForeignKey(
        'Submission',
        related_name='songs',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    chart = models.ForeignKey(
        'Chart',
        related_name='songs',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    performance = models.ForeignKey(
        'Performance',
        related_name='songs',
        on_delete=models.CASCADE,
    )

    # Denormalizations
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

    # Internals
    class Meta:
        unique_together = (
            ('performance', 'num',),
        )

    class JSONAPIMeta:
        resource_name = "song"

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.id.hex,
        ]))
        super(Song, self).save(*args, **kwargs)

    def calculate(self, *args, **kwargs):
        self.mus_points = self.calculate_mus_points()
        self.prs_points = self.calculate_prs_points()
        self.sng_points = self.calculate_sng_points()
        self.total_points = self.calculate_total_points()
        self.mus_score = self.calculate_mus_score()
        self.prs_score = self.calculate_prs_score()
        self.sng_score = self.calculate_sng_score()
        self.total_score = self.calculate_total_score()

    # Permissions
    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False

    # Denormalizations
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

    # Transitions
    @transition(field=status, source='*', target=STATUS.published)
    def publish(self, *args, **kwargs):
        return


class Submission(TimeStampedModel):
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

    # FKs
    performer = models.ForeignKey(
        'Performer',
        related_name='submissions',
        on_delete=models.CASCADE,
    )

    chart = models.ForeignKey(
        'Chart',
        related_name='submissions',
        on_delete=models.CASCADE,
    )

    # Internals
    class Meta:
        unique_together = (
            ('performer', 'chart',),
        )

    class JSONAPIMeta:
        resource_name = "submission"

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0}".format(
            self.id.hex,
        )
        super(Submission, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


class Venue(TimeStampedModel):
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

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'inactive', 'Inactive',),
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

    # Internals
    class JSONAPIMeta:
        resource_name = "venue"

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.location,
            " - ",
            "{0},".format(self.city),
            self.state,
        ]))
        super(Venue, self).save(*args, **kwargs)

    # Permissions
    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False


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

    # Internals
    class JSONAPIMeta:
        resource_name = "user"

    # Methods
    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
