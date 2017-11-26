# Standard Libary
import datetime
import logging
import random
import uuid

# Third-Party
from django_fsm import (
    FSMIntegerField,
    transition,
)
from django_fsm_log.decorators import fsm_log_by
from dry_rest_permissions.generics import (
    allow_staff_or_superuser,
    authenticated_users,
)
from model_utils import Choices
from model_utils.models import TimeStampedModel
from ranking import Ranking
from timezone_field import TimeZoneField

# Django
from django.apps import apps as api_apps
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.postgres.fields import (  # CIEmailField,
    ArrayField,
    FloatRangeField,
    IntegerRangeField,
)
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import (
    models,
)
from django.core.validators import validate_email
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import get_template
from django.utils.encoding import smart_text
from django.utils.functional import cached_property
from django.utils.timezone import now
from cloudinary.models import CloudinaryField

# Local
from .fields import (
    CloudinaryRenameField,
)

from .managers import (
    ChartManager,
    UserManager,
    PersonManager,
    EnrollmentManager,
    OrganizationManager,
    GroupManager,
    MemberManager,
)

from .tasks import (
    create_bbscores_report,
    create_drcj_report,
    create_admins_report,
    create_pdf,
    send_entry,
    send_session,
)

config = api_apps.get_app_config('api')

log = logging.getLogger(__name__)


class Appearance(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (2, 'published', 'Published',),
        (5, 'verified', 'Verified',),
        (10, 'started', 'Started',),
        (20, 'finished', 'Finished',),
        (30, 'confirmed', 'Confirmed',),
        (40, 'flagged', 'Flagged',),
        (50, 'scratched', 'Scratched',),
        (60, 'cleared', 'Cleared',),
        (90, 'announced', 'Announced',),
        (95, 'archived', 'Archived',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    num = models.IntegerField(
        null=True,
        blank=True,
    )

    draw = models.IntegerField(
        null=True,
        blank=True,
    )

    actual_start = models.DateTimeField(
        help_text="""
            The actual appearance window.""",
        null=True,
        blank=True,
    )

    actual_finish = models.DateTimeField(
        help_text="""
            The actual appearance window.""",
        null=True,
        blank=True,
    )

    # Privates
    rank = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_points = models.IntegerField(
        null=True,
        blank=True,
    )

    per_points = models.IntegerField(
        null=True,
        blank=True,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
    )

    tot_points = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
    )

    per_score = models.FloatField(
        null=True,
        blank=True,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
    )

    tot_score = models.FloatField(
        null=True,
        blank=True,
    )

    # FKs
    round = models.ForeignKey(
        'Round',
        related_name='appearances',
        on_delete=models.CASCADE,
    )

    entry = models.ForeignKey(
        'Entry',
        related_name='appearances',
        on_delete=models.CASCADE,
    )

    competitor = models.ForeignKey(
        'Competitor',
        related_name='appearances',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    slot = models.OneToOneField(
        'Slot',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # Internals
    class JSONAPIMeta:
        resource_name = "appearance"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: smart_text(x), [
                    self.round,
                    self.entry,
                ]
            )
        )
        super().save(*args, **kwargs)

    # Methods
    # def print_var(self):
    #     appearance = self
    #     song_one = appearance.songs.all().order_by('num').first()
    #     song_two = appearance.songs.all().order_by('num').last()
    #     scores_one = song_one.scores.all().order_by('panelist__num')
    #     scores_two = song_two.scores.all().order_by('panelist__num')
    #     scores_one_avg = scores_one.aggregate(a=models.Avg('points'))['a']
    #     scores_two_avg = scores_two.aggregate(a=models.Avg('points'))['a']
    #     tem = get_template('variance.html')
    #     template = tem.render(context={
    #         'appearance': appearance,
    #         'song_one': song_one,
    #         'song_two': song_two,
    #         'scores_one': scores_one,
    #         'scores_two': scores_two,
    #         'scores_one_avg': scores_one_avg,
    #         'scores_two_avg': scores_two_avg,
    #     })
    #     payload = {
    #         "test": True,
    #         "document_content": template,
    #         "name": "var-{0}.pdf".format(id),
    #         "document_type": "pdf",
    #     }
    #     response = create_pdf(payload)
    #     f = ContentFile(response)
    #     appearance.var_pdf.save(
    #         "{0}.pdf".format(id),
    #         f
    #     )
    #     appearance.save()
    #     return "Complete"

    def calculate(self, *args, **kwargs):
        self.rank = self.calculate_rank()
        self.mus_points = self.calculate_mus_points()
        self.per_points = self.calculate_per_points()
        self.sng_points = self.calculate_sng_points()
        self.tot_points = self.calculate_tot_points()
        self.mus_score = self.calculate_mus_score()
        self.per_score = self.calculate_per_score()
        self.sng_score = self.calculate_sng_score()
        self.tot_score = self.calculate_tot_score()

    def calculate_rank(self):
        return self.round.ranking(self.calculate_tot_points())

    def calculate_mus_points(self):
        return self.songs.filter(
            scores__kind=10,
            scores__category=30,
        ).aggregate(
            tot=models.Sum('scores__points')
        )['tot']

    def calculate_per_points(self):
        return self.songs.filter(
            scores__kind=10,
            scores__category=40,
        ).aggregate(
            tot=models.Sum('scores__points')
        )['tot']

    def calculate_sng_points(self):
        return self.songs.filter(
            scores__kind=10,
            scores__category=50,
        ).aggregate(
            tot=models.Sum('scores__points')
        )['tot']

    def calculate_tot_points(self):
        return self.songs.filter(
            scores__kind=10,
        ).aggregate(
            tot=models.Sum('scores__points')
        )['tot']

    def calculate_mus_score(self):
        return self.songs.filter(
            scores__kind=10,
            scores__category=30,
        ).aggregate(
            tot=models.Avg('scores__points')
        )['tot']

    def calculate_per_score(self):
        return self.songs.filter(
            scores__kind=10,
            scores__category=40,
        ).aggregate(
            tot=models.Avg('scores__points')
        )['tot']

    def calculate_sng_score(self):
        return self.songs.filter(
            scores__kind=10,
            scores__category=50,
        ).aggregate(
            tot=models.Avg('scores__points')
        )['tot']

    def calculate_tot_score(self):
        return self.songs.filter(
            scores__kind=10,
        ).aggregate(
            tot=models.Avg('scores__points')
        )['tot']

    # Appearance Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_scoring_manager,
            request.user.is_convention_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.round.session.convention.assignments.filter(
                person__user=request.user,
                category__lt=30,
                status__gt=0,
                kind=10,
            )
        ])

    # Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.started)
    def start(self, *args, **kwargs):
        panelists = self.round.panelists.filter(
            category__gt=20,
        )
        i = 1
        while i <= 2:  # Number songs constant
            song = self.songs.create(
                num=i
            )
            for panelist in panelists:
                song.scores.create(
                    category=panelist.category,
                    kind=panelist.kind,
                    panelist=panelist,
                )
            i += 1
        self.actual_start = now()
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.finished)
    def finish(self, *args, **kwargs):
        self.actual_finish = now()
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.confirmed)
    def confirm(self, *args, **kwargs):
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.announced)
    def announce(self, *args, **kwargs):
        return


class Assignment(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
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
        (10, 'official', 'Official'),
        (20, 'practice', 'Practice'),
        (30, 'composite', 'Composite'),
    )

    kind = models.IntegerField(
        choices=KIND,
    )

    CATEGORY = Choices(
        (5, 'drcj', 'DRCJ'),
        (10, 'admin', 'CA'),
        (30, 'music', 'Music'),
        (40, 'performance', 'Performance'),
        (50, 'singing', 'Singing'),
    )

    category = models.IntegerField(
        choices=CATEGORY,
        null=True,
        blank=True,
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

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = " ".join(filter(None, [
            "{0}".format(self.person),
            "{0}".format(self.convention),
            self.get_kind_display(),
        ]))
        super().save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_judge_manager,
            request.user.is_convention_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.convention.assignments.filter(
                person__user=request.user,
                category__lt=20,
                status__gt=0,
            )
        ])

    # Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, *args, **kwargs):
        """Activate the Assignment."""
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, *args, **kwargs):
        """Deactivate the Assignment."""
        return


class Award(TimeStampedModel):
    """
    Award Model.

    The specific award conferred by an Organization.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
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
        (32, 'chorus', "Chorus"),
        (41, 'quartet', "Quartet"),
    )

    kind = models.IntegerField(
        choices=KIND,
    )

    LEVEL = Choices(
        (10, 'championship', "Championship"),
        (20, 'award', "Award"),
        (30, 'qualifier', "Qualifier"),
        (40, 'sentinel', "Sentinel"),
    )

    level = models.IntegerField(
        choices=LEVEL,
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
        null=True,
        blank=True,
    )

    is_primary = models.BooleanField(
        help_text="""Primary (v. Secondary).""",
        default=False,
    )

    is_invitational = models.BooleanField(
        help_text="""Invite-only (v. Open).""",
        default=False,
    )

    is_manual = models.BooleanField(
        help_text="""Manual (v. Automatic).""",
        default=False,
    )

    rounds = models.IntegerField(
        help_text="""Number of rounds to determine the championship""",
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

    description = models.TextField(
        help_text="""
            The Public description of the award.""",
        blank=True,
        max_length=1000,
    )

    notes = models.TextField(
        help_text="""
            Private Notes (for internal use only).""",
        blank=True,
    )

    footnote = models.CharField(
        help_text="""
            The text to present on the OSS""",
        blank=True,
        max_length=255,
    )

    is_improved = models.BooleanField(
        help_text="""Designates 'Most-Improved'.  Implies manual.""",
        default=False,
    )

    is_multi = models.BooleanField(
        help_text="""Award spans conventions; must be determined manually.""",
        default=False,
    )

    is_rep_qualifies = models.BooleanField(
        help_text="""Boolean; true means the district rep qualifies.""",
        default=False,
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

    # FKs
    organization = models.ForeignKey(
        'Organization',
        related_name='awards',
        on_delete=models.CASCADE,
    )

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        on_delete=models.SET_NULL,
    )

    # Internals
    class JSONAPIMeta:
        resource_name = "award"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = self.name
        super().save(*args, **kwargs)

    # Award Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_convention_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            False,
        ])

    # Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, *args, **kwargs):
        """Activate the Award."""
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, *args, **kwargs):
        """Deactivate the Award."""
        return


class Chart(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
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

    title = models.CharField(
        max_length=255,
    )

    arrangers = models.CharField(
        max_length=255,
    )

    composers = models.CharField(
        max_length=255,
    )

    lyricists = models.CharField(
        max_length=255,
    )

    holders = models.TextField(
        blank=True,
    )

    description = models.TextField(
        help_text="""
            Fun or interesting facts to share about the chart (ie, 'from Disney's Lion King, first sung by Elton John'.)""",
        blank=True,
        max_length=1000,
    )

    notes = models.TextField(
        help_text="""
            Private Notes (for internal use only).""",
        blank=True,
    )

    img = CloudinaryRenameField(
        'image',
        null=True,
        blank=True,
    )

    objects = ChartManager()

    # Internals
    class Meta:
        unique_together = (
            ('title', 'arrangers',)
        )

    class JSONAPIMeta:
        resource_name = "chart"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = " ".join(filter(None, [
            self.title,
            "[{0}]".format(self.arrangers),
        ]))
        super().save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_chart_manager,
            request.user.is_group_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            request.user.is_chart_manager,
        ])

    # Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, *args, **kwargs):
        """Activate the Award."""
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, *args, **kwargs):
        """Deactivate the Award."""
        return


class Contest(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    STATUS = Choices(
        (-10, 'excluded', 'Excluded',),
        (0, 'new', 'New',),
        (10, 'included', 'Included',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    # Private
    champion = models.ForeignKey(
        'Entry',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
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

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = " ".join(filter(None, [
            self.award.name,
            self.session.nomen,
        ]))
        super().save(*args, **kwargs)

    # Contest Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_convention_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.session.convention.assignments.filter(
                person__user=request.user,
                category__lte=10,
                kind=10,
            )
        ])

    # Methods
    def ranking(self, point_total):
        if not point_total:
            return None
        contestants = self.contestants.filter(status__gt=0)
        points = [contestant.calculate_tot_points() for contestant in contestants]
        points = sorted(points, reverse=True)
        ranking = Ranking(points, start=1)
        rank = ranking.rank(point_total)
        return rank

    def calculate(self, *args, **kwargs):
        if self.contest.is_qualifier:
            champion = None
        else:
            try:
                champion = self.contest.contestants.get(rank=1).entry
            except self.contest.contestants.model.DoesNotExist:
                champion = None
            except self.contest.contestants.model.MultipleObjectsReturned:
                champion = self.contest.contestants.filter(rank=1).order_by(
                    '-sng_points',
                    '-mus_points',
                    '-per_points',
                ).first().entry
        self.champion = champion

    # Transitions
    @fsm_log_by
    @transition(field=status, source=[STATUS.new, STATUS.excluded], target=STATUS.included)
    def include(self, *args, **kwargs):
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.new, STATUS.included], target=STATUS.excluded)
    def exclude(self, *args, **kwargs):
        return


class Contestant(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    STATUS = Choices(
        (-10, 'excluded', 'Excluded',),
        (0, 'new', 'New',),
        (10, 'included', 'Included',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    # Privates
    rank = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_points = models.IntegerField(
        null=True,
        blank=True,
    )

    per_points = models.IntegerField(
        null=True,
        blank=True,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
    )

    tot_points = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
    )

    per_score = models.FloatField(
        null=True,
        blank=True,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
    )

    tot_score = models.FloatField(
        null=True,
        blank=True,
    )

    # FKs
    entry = models.ForeignKey(
        'Entry',
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
            ('entry', 'contest',),
        )

    class JSONAPIMeta:
        resource_name = "contestant"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: smart_text(x), [
                    self.entry,
                    self.contest,
                ]
            )
        )
        super().save(*args, **kwargs)

    # Methods
    def calculate(self, *args, **kwargs):
        self.mus_points = self.calculate_mus_points()
        self.per_points = self.calculate_per_points()
        self.sng_points = self.calculate_sng_points()
        self.tot_points = self.calculate_tot_points()
        self.mus_score = self.calculate_mus_score()
        self.per_score = self.calculate_per_score()
        self.sng_score = self.calculate_sng_score()
        self.tot_score = self.calculate_tot_score()
        self.rank = self.calculate_rank()

    def calculate_rank(self):
        return self.contest.ranking(self.calculate_tot_points())

    def calculate_mus_points(self):
        return self.entry.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=30,
            round__num__lte=self.contest.award.rounds,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_per_points(self):
        return self.entry.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=40,
            round__num__lte=self.contest.award.rounds,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_sng_points(self):
        return self.entry.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=50,
            round__num__lte=self.contest.award.rounds,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_tot_points(self):
        return self.entry.appearances.filter(
            songs__scores__kind=10,
            round__num__lte=self.contest.award.rounds,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_mus_score(self):
        return self.entry.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=30,
            round__num__lte=self.contest.award.rounds,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_per_score(self):
        return self.entry.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=40,
            round__num__lte=self.contest.award.rounds,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_sng_score(self):
        return self.entry.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=50,
            round__num__lte=self.contest.award.rounds,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_tot_score(self):
        return self.entry.appearances.filter(
            songs__scores__kind=10,
            round__num__lte=self.contest.award.rounds,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_convention_manager,
            request.user.is_group_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.contest.session.convention.assignments.filter(
                person__user=request.user,
                category__lte=10,
                kind=10,
            ),
            self.entry.group.members.filter(
                person__user=request.user,
                is_admin=True,
                status__gt=0,
            ),
        ])

    # Methods

    # Contestant Transitions
    @fsm_log_by
    @transition(field=status, source=[STATUS.new, STATUS.excluded], target=STATUS.included)
    def include(self, *args, **kwargs):
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.new, STATUS.included], target=STATUS.excluded)
    def exclude(self, *args, **kwargs):
        return


class Convention(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (2, 'published', 'Published',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    is_archived = models.BooleanField(
        default=False,
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
        (1, 'single', "Single"),
        (2, 'double', "Double"),
        (3, 'triple', "Triple"),
        (4, 'quadruple', "Quadruple"),
        (5, 'quintiple', "Quintiple"),
    )

    panel = models.IntegerField(
        choices=PANEL,
        null=True,
        blank=True,
    )

    YEAR_CHOICES = []
    for r in reversed(range(1939, (datetime.datetime.now().year + 2))):
        YEAR_CHOICES.append((r, r))

    year = models.IntegerField(
        choices=YEAR_CHOICES,
    )

    open_date = models.DateField(
        null=True,
        blank=True,
    )

    close_date = models.DateField(
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

    location = models.CharField(
        max_length=255,
        blank=True,
    )

    description = models.TextField(
        help_text="""
            A general description field; usually used for hotel and venue info.""",
        blank=True,
        max_length=1000,
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

    organization = models.ForeignKey(
        'Organization',
        related_name='conventions',
        help_text="""
            The owning organization for the convention.""",
        on_delete=models.CASCADE,
    )

    # Internals
    class JSONAPIMeta:
        resource_name = "convention"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def clean(self):
        pass

    def save(self, *args, **kwargs):
        self.nomen = self.name
        super().save(*args, **kwargs)

    # Convention Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_convention_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.organization.officers.filter(
                person__user=request.user,
                status__gt=0,
            ),
        ])

    # Convention Transition Conditions
    def can_publish_convention(self):
        if any([
            not self.open_date,
            not self.close_date,
            not self.start_date,
            not self.close_date,
        ]):
            return False
        return all([
            self.open_date,
            self.close_date,
            self.start_date,
            self.end_date,
            self.open_date < self.close_date,
            self.close_date < self.start_date,
            self.start_date < self.end_date,
            self.grantors.count() > 0,
            self.sessions.count() > 0,
        ])

    # Convention Transitions
    @fsm_log_by
    @transition(
        field=status,
        source='*',
        target=STATUS.published,
        conditions=[can_publish_convention],
    )
    def publish(self, *args, **kwargs):
        """Publish convention and related sessions."""
        grantors = self.grantors.all()
        sessions = self.sessions.all()
        for session in sessions:
            for grantor in grantors:
                awards = grantor.organization.awards.filter(
                    status=grantor.organization.awards.model.STATUS.active,
                    kind=session.kind,
                )
                for award in awards:
                    session.contests.create(
                        award=award,
                    )
        return


class Competitor(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    is_archived = models.BooleanField(
        default=False,
    )

    img = CloudinaryRenameField(
        'image',
        null=True,
        blank=True,
    )

    rank = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_points = models.IntegerField(
        null=True,
        blank=True,
    )

    per_points = models.IntegerField(
        null=True,
        blank=True,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
    )

    tot_points = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
    )

    per_score = models.FloatField(
        null=True,
        blank=True,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
    )

    tot_score = models.FloatField(
        null=True,
        blank=True,
    )

    # FKs
    session = models.ForeignKey(
        'Session',
        related_name='competitors',
        on_delete=models.CASCADE,
    )

    group = models.ForeignKey(
        'Group',
        related_name='competitors',
        on_delete=models.CASCADE,
    )

    # Internals
    class Meta:
        verbose_name_plural = 'competitors'
        unique_together = (
            ('group', 'session',),
        )

    class JSONAPIMeta:
        resource_name = "competitor"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def clean(self):
        pass

    def save(self, *args, **kwargs):
        self.nomen = "; ".join(
            map(
                lambda x: smart_text(x), [
                    self.group,
                    self.session,
                ]
            )
        )
        super().save(*args, **kwargs)

    # Methods
    def calculate(self, *args, **kwargs):
        self.mus_points = self.calculate_mus_points()
        self.per_points = self.calculate_per_points()
        self.sng_points = self.calculate_sng_points()
        self.tot_points = self.calculate_tot_points()
        self.mus_score = self.calculate_mus_score()
        self.per_score = self.calculate_per_score()
        self.sng_score = self.calculate_sng_score()
        self.tot_score = self.calculate_tot_score()
        self.rank = self.calculate_rank()

    def calculate_pdf(self):
        for appearance in self.appearances.all():
            for song in appearance.songs.all():
                song.calculate()
                song.save()
            appearance.calculate()
            appearance.save()
        self.calculate()
        self.save()
        return

    # def print_csa(self):
    #     entry = self
    #     contestants = entry.contestants.filter(status__gt=0)
    #     appearances = entry.appearances.order_by(
    #         'round__kind',
    #     )
    #     assignments = entry.session.convention.assignments.filter(
    #         category__gt=20,
    #     ).order_by(
    #         'category',
    #         'kind',
    #         'nomen',
    #     )
    #     tem = get_template('csa.html')
    #     template = tem.render(context={
    #         'entry': entry,
    #         'appearances': appearances,
    #         'assignments': assignments,
    #         'contestants': contestants,
    #     })
    #     payload = {
    #         "test": True,
    #         "document_content": template,
    #         "name": "csa-{0}.pdf".format(id),
    #         "document_type": "pdf",
    #     }
    #     response = create_pdf(payload)
    #     f = ContentFile(response)
    #     entry.csa_pdf.save(
    #         "{0}.pdf".format(id),
    #         f
    #     )
    #     entry.save()
    #     return "Complete"

    def calculate_rank(self):
        try:
            primary = self.session.contests.first()
            return self.contestants.get(contest=primary).calculate_rank()
        except self.contestants.model.DoesNotExist:
            return None

    def calculate_mus_points(self):
        return self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=30,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_per_points(self):
        return self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=40,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_sng_points(self):
        return self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=50,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_tot_points(self):
        return self.appearances.filter(
            songs__scores__kind=10,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_mus_score(self):
        return self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=30,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_per_score(self):
        return self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=40,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_sng_score(self):
        return self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=50,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_tot_score(self):
        return self.appearances.filter(
            songs__scores__kind=10,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_group_manager,
            request.user.is_session_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.session.convention.assignments.filter(
                person__user=request.user,
                category__lt=10,
                kind=10,
            ),
        ])

    # Competitor Methods

    # Competitor Transition Conditions

    # Competitor Transitions


class Enrollment(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    STATUS = Choices(
        (-20, 'legacy', 'Legacy',),
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'exempt', 'Exempt',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    MEM_STATUS = Choices(
        (10, 'active', 'Active',),
        (20, 'active_internal', 'Active Internal',),
        (30, 'active_licensed', 'Active Licensed',),
        (40, 'cancelled', 'Cancelled',),
        (50, 'closed', 'Closed',),
        (60, 'closed_merged', 'Closed Merged',),
        (70, 'closed_revoked', 'Closed Revoked',),
        (80, 'closed_voluntary', 'Closed Voluntary',),
        (90, 'expelled', 'Expelled',),
        (100, 'expired', 'Expired',),
        (105, 'expired_licensed', 'Expired Licensed',),
        (110, 'lapsed', 'Lapsed',),
        (120, 'not_approved', 'Not Approved',),
        (130, 'pending', 'Pending',),
        (140, 'pending_voluntary', 'Pending Voluntary',),
        (150, 'suspended', 'Suspended',),
        (160, 'suspended_membership', 'Suspended Membership',),
    )

    mem_status = models.IntegerField(
        choices=MEM_STATUS,
        null=True,
        blank=True,
    )

    SUB_STATUS = Choices(
        (10, 'active', 'Active',),
        (20, 'expired', 'Expired',),
        (30, 'pending', 'Pending',),
        (40, 'lapsedRenew', 'Lapsed',),
        (50, 'cancelled', 'Cancelled',),
        (60, 'swapped', 'Swapped',),
    )

    sub_status = models.IntegerField(
        choices=SUB_STATUS,
        null=True,
        blank=True,
    )

    MEM_CODE = Choices(
        (10, 'RG', 'RG Regular'),
        (20, 'R5', 'R5 Regular 50 Year'),
        (30, 'SN', 'SN Senior'),
        (40, 'S5', 'S5 Senior 50 Year'),
        (50, 'SL', 'SL Senior Legacy'),
        (60, 'Y1', 'Y1 Youth Initial'),
        (70, 'Y2', 'Y2 Youth Subsequent'),
        (80, 'LF', 'LF Lifetime Regular'),
        (90, 'L5', 'L5 Lifetime 50 Year'),
        (100, 'LY', 'LY Lifetime Youth'),
        (110, 'LS', 'LS Lifetime Senior'),
        (120, 'AS', 'AS Associate'),
    )

    mem_code = models.IntegerField(
        choices=MEM_CODE,
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

    bhs_pk = models.UUIDField(
        null=True,
        blank=True,
        unique=True,
        db_index=True,
    )

    # FKs
    organization = models.ForeignKey(
        'Organization',
        on_delete=models.CASCADE,
    )

    person = models.ForeignKey(
        'Person',
        on_delete=models.CASCADE,
    )

    # Internals
    objects = EnrollmentManager()

    class Meta:
        default_related_name = 'enrollments'
        unique_together = (
            ('organization', 'person',),
        )

    class JSONAPIMeta:
        resource_name = "enrollment"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def clean(self):
        pass

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: smart_text(x), [
                    self.organization,
                    self.person,
                ]
            )
        )
        super().save(*args, **kwargs)

    # Enrollment Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return False

    # Enrollment Transitions


class Entry(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (5, 'invited', 'Invited',),
        (7, 'withdrawn', 'Withdrawn',),
        (10, 'submitted', 'Submitted',),
        (20, 'approved', 'Approved',),
        (52, 'scratched', 'Scratched',),
        (55, 'disqualified', 'Disqualified',),
        (57, 'final', 'Final',),
        (95, 'archived', 'Archived',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    is_archived = models.BooleanField(
        default=False,
    )

    img = CloudinaryRenameField(
        'image',
        null=True,
        blank=True,
    )

    is_evaluation = models.BooleanField(
        help_text="""
            Entry requests evaluation.""",
        default=True,
    )

    is_private = models.BooleanField(
        help_text="""
            Keep scores private.""",
        default=False,
    )

    draw = models.IntegerField(
        help_text="""
            The draw for the initial round only.""",
        null=True,
        blank=True,
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

    directors = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )

    # Privates
    rank = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_points = models.IntegerField(
        null=True,
        blank=True,
    )

    per_points = models.IntegerField(
        null=True,
        blank=True,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
    )

    tot_points = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
    )

    per_score = models.FloatField(
        null=True,
        blank=True,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
    )

    tot_score = models.FloatField(
        null=True,
        blank=True,
    )

    # FKs
    session = models.ForeignKey(
        'Session',
        related_name='entries',
        on_delete=models.CASCADE,
    )

    group = models.ForeignKey(
        'Group',
        related_name='entries',
        on_delete=models.CASCADE,
    )

    # Internals
    class Meta:
        verbose_name_plural = 'entries'
        unique_together = (
            ('group', 'session',),
        )

    class JSONAPIMeta:
        resource_name = "entry"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def clean(self):
        if self.is_private and self.contestants.exists():
            raise ValidationError(
                {'is_private': 'You may not compete for an award and remain private.'}
            )

    def save(self, *args, **kwargs):
        self.nomen = "; ".join(
            map(
                lambda x: smart_text(x), [
                    self.group,
                    self.session,
                ]
            )
        )
        super().save(*args, **kwargs)

    # Methods
    def calculate(self, *args, **kwargs):
        self.mus_points = self.calculate_mus_points()
        self.per_points = self.calculate_per_points()
        self.sng_points = self.calculate_sng_points()
        self.tot_points = self.calculate_tot_points()
        self.mus_score = self.calculate_mus_score()
        self.per_score = self.calculate_per_score()
        self.sng_score = self.calculate_sng_score()
        self.tot_score = self.calculate_tot_score()
        self.rank = self.calculate_rank()

    def calculate_pdf(self):
        for appearance in self.appearances.all():
            for song in appearance.songs.all():
                song.calculate()
                song.save()
            appearance.calculate()
            appearance.save()
        self.calculate()
        self.save()
        return

    # def print_csa(self):
    #     entry = self
    #     contestants = entry.contestants.filter(status__gt=0)
    #     appearances = entry.appearances.order_by(
    #         'round__kind',
    #     )
    #     assignments = entry.session.convention.assignments.filter(
    #         category__gt=20,
    #     ).order_by(
    #         'category',
    #         'kind',
    #         'nomen',
    #     )
    #     tem = get_template('csa.html')
    #     template = tem.render(context={
    #         'entry': entry,
    #         'appearances': appearances,
    #         'assignments': assignments,
    #         'contestants': contestants,
    #     })
    #     payload = {
    #         "test": True,
    #         "document_content": template,
    #         "name": "csa-{0}.pdf".format(id),
    #         "document_type": "pdf",
    #     }
    #     response = create_pdf(payload)
    #     f = ContentFile(response)
    #     entry.csa_pdf.save(
    #         "{0}.pdf".format(id),
    #         f
    #     )
    #     entry.save()
    #     return "Complete"

    def calculate_rank(self):
        try:
            primary = self.session.contests.first()
            return self.contestants.get(contest=primary).calculate_rank()
        except self.contestants.model.DoesNotExist:
            return None

    def calculate_mus_points(self):
        return self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=30,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_per_points(self):
        return self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=40,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_sng_points(self):
        return self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=50,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_tot_points(self):
        return self.appearances.filter(
            songs__scores__kind=10,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

    def calculate_mus_score(self):
        return self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=30,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_per_score(self):
        return self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=40,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_sng_score(self):
        return self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=50,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def calculate_tot_score(self):
        return self.appearances.filter(
            songs__scores__kind=10,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_group_manager,
            request.user.is_session_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.session.convention.assignments.filter(
                person__user=request.user,
                category__lt=10,
                kind=10,
            ),
            all([
                self.group.members.filter(
                    person__user=request.user,
                    status__gt=0,
                    is_admin=True,
                ),
                self.status <= self.STATUS.approved,
            ]),
        ])

    # Methods

    # Entry Transition Conditions
    def can_invite_entry(self):
        return all([
            self.group.members.filter(is_admin=True),
            self.group.status == self.group.STATUS.active,
        ])

    def can_submit_entry(self):
        return all([
            any([
                self.group.status == self.group.STATUS.active,
                self.group.status == self.group.STATUS.new,
            ])
        ])

    # Entry Transitions
    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.new],
        target=STATUS.invited,
        conditions=[can_invite_entry],
    )
    def invite(self, *args, **kwargs):
        context = {'entry': self}
        send_entry.delay('entry_invite.txt', context)
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.invited, STATUS.submitted],
        target=STATUS.withdrawn,
        conditions=[],
    )
    def withdraw(self, *args, **kwargs):
        if self.session.status == self.session.STATUS.verified:
            remains = self.session.entries.filter(draw__gt=self.draw)
            self.draw = None
            self.save()
            for entry in remains:
                entry.draw = entry.draw - 1
                entry.save()
        contestants = self.contestants.filter(status__gt=0)
        for contestant in contestants:
            contestant.delete()
        context = {'entry': self}
        send_entry.delay('entry_withdraw.txt', context)
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.new, STATUS.invited],
        target=STATUS.submitted,
        conditions=[can_submit_entry],
    )
    def submit(self, *args, **kwargs):
        context = {'entry': self}
        send_entry.delay('entry_submit.txt', context)
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.new, STATUS.submitted, STATUS.withdrawn, STATUS.scratched],
        target=STATUS.approved,
        conditions=[],
    )
    def approve(self, *args, **kwargs):
        context = {'entry': self}
        send_entry.delay('entry_approve.txt', context)
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.approved],
        target=STATUS.scratched,
        conditions=[],
    )
    def scratch(self, *args, **kwargs):
        if self.session.status == self.session.STATUS.verified and self.draw:
            remains = self.session.entries.filter(draw__gt=self.draw)
            self.draw = None
            self.save()
            for entry in remains:
                entry.draw = entry.draw - 1
                entry.save()
        for contestant in self.contestants.filter(status__gt=0):
            contestant.delete()
        context = {'entry': self}
        send_entry.delay('entry_scratch.txt', context)
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.approved],
        target=STATUS.final,
        conditions=[],
    )
    def finalize(self, *args, **kwargs):
        # Finalize the Entry (locks to further edits)
        context = {'entry': self}
        send_entry.delay('entry_finalize.txt', context)
        return


class Grantor(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    # FKs
    convention = models.ForeignKey(
        'Convention',
        related_name='grantors',
        on_delete=models.CASCADE,
    )

    organization = models.ForeignKey(
        'Organization',
        related_name='grantors',
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (
            ('convention', 'organization',),
        )

    class JSONAPIMeta:
        resource_name = "grantor"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: smart_text(x), [
                    self.convention,
                    self.organization,
                ]
            )
        )
        super().save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return any([
            True,
        ])

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return any([
            True,
        ])

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_convention_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.round.session.convention.assignments.filter(
                person__user=request.user,
                category__lt=30,
                kind=10,
            ),
        ])


class Group(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the resource.
        """,
        max_length=255,
    )

    STATUS = Choices(
        (-20, 'legacy', 'Legacy',),
        (-10, 'inactive', 'Inactive',),
        (-5, 'aic', 'AIC',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'exempt', 'Exempt',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    KIND = Choices(
        (32, 'chorus', "Chorus"),
        (41, 'quartet', "Quartet"),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of group.
        """,
        choices=KIND,
    )

    short_name = models.CharField(
        help_text="""
            A short-form name for the resource.""",
        blank=True,
        max_length=255,
    )

    code = models.CharField(
        help_text="""
            The chapter code.""",
        max_length=255,
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

    location = models.CharField(
        help_text="""
            The geographical location of the resource.""",
        max_length=255,
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
        blank=True,
        max_length=25,
    )

    img = CloudinaryRenameField(
        'image',
        null=True,
        blank=True,
    )

    description = models.TextField(
        help_text="""
            A description of the group.  Max 1000 characters.""",
        blank=True,
        max_length=1000,
    )

    notes = models.TextField(
        help_text="""
            Notes (for internal use only).""",
        blank=True,
    )

    MEM_STATUS = Choices(
        (10, 'active', 'Active',),
        (20, 'active_internal', 'Active Internal',),
        (30, 'active_licensed', 'Active Licensed',),
        (40, 'cancelled', 'Cancelled',),
        (50, 'closed', 'Closed',),
        (60, 'closed_merged', 'Closed Merged',),
        (70, 'closed_revoked', 'Closed Revoked',),
        (80, 'closed_voluntary', 'Closed Voluntary',),
        (90, 'expelled', 'Expelled',),
        (100, 'expired', 'Expired',),
        (105, 'expired_licensed', 'Expired Licensed',),
        (110, 'lapsed', 'Lapsed',),
        (120, 'not_approved', 'Not Approved',),
        (130, 'pending', 'Pending',),
        (140, 'pending_voluntary', 'Pending Voluntary',),
        (150, 'suspended', 'Suspended',),
        (160, 'suspended_membership', 'Suspended Membership',),
    )

    mem_status = models.IntegerField(
        choices=MEM_STATUS,
        null=True,
        blank=True,
    )

    bhs_id = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
    )

    bhs_pk = models.UUIDField(
        null=True,
        blank=True,
        unique=True,
        db_index=True,
    )

    org_sort = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
        editable=False,
    )

    # FKs
    organization = models.ForeignKey(
        'Organization',
        null=True,
        blank=True,
        related_name='groups',
        db_index=True,
        on_delete=models.SET_NULL,
    )

    # Denormalizations
    international = models.TextField(
        help_text="""
            The denormalized international organization.""",
        blank=True,
        max_length=255,
    )

    district = models.TextField(
        help_text="""
            The denormalized district organization.""",
        blank=True,
        max_length=255,
    )

    division = models.TextField(
        help_text="""
            The denormalized division organization.""",
        blank=True,
        max_length=255,
    )

    chapter = models.TextField(
        help_text="""
            The denormalized chapter organization.""",
        blank=True,
        max_length=255,
    )

    # Internals
    objects = GroupManager()

    class Meta:
        verbose_name_plural = 'groups'

    class JSONAPIMeta:
        resource_name = "group"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def clean(self):
        if self.kind == self.KIND.quartet:
            if self.members.filter(
                status=self.members.model.STATUS.active,
            ).count() > 4:
                raise ValidationError(
                    {'kind': 'Quartets can not have more than four current members.'}
                )

    def save(self, *args, **kwargs):
        self.nomen = self.name
        super().save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_group_manager,
            request.user.is_group_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.members.filter(
                person__user=request.user,
                is_admin=True,
                status__gt=0,
            ),
            request.user.is_group_manager,
        ])

    # Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, *args, **kwargs):
        """Activate the Group."""
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, *args, **kwargs):
        """Deactivate the Group."""
        return


class Member(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    STATUS = Choices(
        (-20, 'legacy', 'Legacy',),
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'exempt', 'Exempt',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    MEM_STATUS = Choices(
        (10, 'active', 'Active',),
        (20, 'active_internal', 'Active Internal',),
        (30, 'active_licensed', 'Active Licensed',),
        (40, 'cancelled', 'Cancelled',),
        (50, 'closed', 'Closed',),
        (60, 'closed_merged', 'Closed Merged',),
        (70, 'closed_revoked', 'Closed Revoked',),
        (80, 'closed_voluntary', 'Closed Voluntary',),
        (90, 'expelled', 'Expelled',),
        (100, 'expired', 'Expired',),
        (105, 'expired_licensed', 'Expired Licensed',),
        (110, 'lapsed', 'Lapsed',),
        (120, 'not_approved', 'Not Approved',),
        (130, 'pending', 'Pending',),
        (140, 'pending_voluntary', 'Pending Voluntary',),
        (150, 'suspended', 'Suspended',),
        (160, 'suspended_membership', 'Suspended Membership',),
    )

    mem_status = models.IntegerField(
        choices=MEM_STATUS,
        null=True,
        blank=True,
    )

    SUB_STATUS = Choices(
        (10, 'active', 'Active',),
        (20, 'expired', 'Expired',),
        (30, 'pending', 'Pending',),
        (40, 'lapsedRenew', 'Lapsed',),
        (50, 'cancelled', 'Cancelled',),
        (60, 'swapped', 'Swapped',),
    )

    sub_status = models.IntegerField(
        choices=SUB_STATUS,
        null=True,
        blank=True,
    )

    MEM_CODE = Choices(
        (10, 'RG', 'RG Regular'),
        (20, 'R5', 'R5 Regular 50 Year'),
        (30, 'SN', 'SN Senior'),
        (40, 'S5', 'S5 Senior 50 Year'),
        (50, 'SL', 'SL Senior Legacy'),
        (60, 'Y1', 'Y1 Youth Initial'),
        (70, 'Y2', 'Y2 Youth Subsequent'),
        (80, 'LF', 'LF Lifetime Regular'),
        (90, 'L5', 'L5 Lifetime 50 Year'),
        (100, 'LY', 'LY Lifetime Youth'),
        (110, 'LS', 'LS Lifetime Senior'),
        (120, 'AS', 'AS Associate'),
    )

    mem_code = models.IntegerField(
        choices=MEM_CODE,
        null=True,
        blank=True,
    )

    PART = Choices(
        (-1, 'director', 'Director'),
        (1, 'tenor', 'Tenor'),
        (2, 'lead', 'Lead'),
        (3, 'baritone', 'Baritone'),
        (4, 'bass', 'Bass'),
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

    is_admin = models.BooleanField(
        default=False,
    )

    bhs_pk = models.UUIDField(
        null=True,
        blank=True,
        unique=True,
        db_index=True,
    )

    # FKs
    group = models.ForeignKey(
        'Group',
        related_name='members',
        on_delete=models.CASCADE,
    )

    person = models.ForeignKey(
        'Person',
        related_name='members',
        on_delete=models.CASCADE,
    )

    # Internals
    objects = MemberManager()

    class Meta:
        unique_together = (
            ('group', 'person',),
        )

    class JSONAPIMeta:
        resource_name = "member"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def clean(self):
        if self.is_admin:
            try:
                is_active = self.person.user.is_active
            except ObjectDoesNotExist:
                raise ValidationError(
                    {'is_admin': 'Admin must User account.'}
                )
            if not is_active:
                raise ValidationError(
                    {'is_admin': 'Admin User account must be active.'}
                )

    def save(self, *args, **kwargs):
        # self.nomen = " ".join(
        #     map(
        #         lambda x: smart_text(x), [
        #             self.person,
        #             self.group,
        #         ]
        #     )
        # )
        super().save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_group_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.group.members.filter(
                person__user=request.user,
                is_admin=True,
                status__gt=0,
            ),
        ])

    # Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, *args, **kwargs):
        """Activate the Member."""
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, *args, **kwargs):
        """Deactivate the Member."""
        return


class Office(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    name = models.CharField(
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
        ('International', [
            (1, 'international', "International"),
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
            (32, 'chapter', "Chapter"),
            (41, 'quartet', "Quartet"),
        ]),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of office.""",
        choices=KIND,
        null=True,
        blank=True,
    )

    short_name = models.CharField(
        max_length=255,
        blank=True,
    )

    # Office Permissions
    is_convention_manager = models.BooleanField(
        default=False,
    )

    is_session_manager = models.BooleanField(
        default=False,
    )

    is_scoring_manager = models.BooleanField(
        default=False,
    )

    is_organization_manager = models.BooleanField(
        default=False,
    )

    is_group_manager = models.BooleanField(
        default=False,
    )

    is_person_manager = models.BooleanField(
        default=False,
    )

    is_award_manager = models.BooleanField(
        default=False,
    )

    is_judge_manager = models.BooleanField(
        default=False,
    )

    is_chart_manager = models.BooleanField(
        default=False,
    )

    # Office Methods
    def save(self, *args, **kwargs):
        self.nomen = self.name
        super().save(*args, **kwargs)

    # Internals
    class JSONAPIMeta:
        resource_name = "office"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    # Office Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    @authenticated_users
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
        editable=False,
    )

    STATUS = Choices(
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.active,
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

    person = models.ForeignKey(
        'Person',
        related_name='officers',
        on_delete=models.CASCADE,
    )

    organization = models.ForeignKey(
        'Organization',
        related_name='officers',
        on_delete=models.CASCADE,
    )

    # Internals
    class JSONAPIMeta:
        resource_name = "officer"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: smart_text(x), [
                    self.organization,
                    self.office,
                    self.person,
                ]
            )
        )
        super().save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return False

    # Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, *args, **kwargs):
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, *args, **kwargs):
        return


class Organization(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the resource.
        """,
        max_length=255,
    )

    STATUS = Choices(
        (-20, 'legacy', 'Legacy',),
        (-10, 'inactive', 'Inactive',),
        (-5, 'aic', 'AIC',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'exempt', 'Exempt',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    KIND = Choices(
        ('International', [
            (1, 'international', "International"),
        ]),
        ('District', [
            (11, 'district', "District"),
            (12, 'noncomp', "Noncompetitive"),
            (13, 'affiliate', "Affiliate"),
        ]),
        ('Division', [
            (21, 'division', "Division"),
        ]),
        ('Chapter', [
            (30, 'chapter', "Chapter"),
        ]),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of organization.
        """,
        choices=KIND,
    )

    code = models.CharField(
        help_text="""
            The organization code.""",
        max_length=255,
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

    location = models.CharField(
        help_text="""
            The geographical location of the resource.""",
        max_length=255,
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
        blank=True,
        max_length=25,
    )

    img = CloudinaryRenameField(
        'image',
        null=True,
        blank=True,
    )

    description = models.TextField(
        help_text="""
            A description of the organization.  Max 1000 characters.""",
        blank=True,
        max_length=1000,
    )

    notes = models.TextField(
        help_text="""
            Notes (for internal use only).""",
        blank=True,
    )

    MEM_STATUS = Choices(
        (10, 'active', 'Active',),
        (20, 'active_internal', 'Active Internal',),
        (30, 'active_licensed', 'Active Licensed',),
        (40, 'cancelled', 'Cancelled',),
        (50, 'closed', 'Closed',),
        (60, 'closed_merged', 'Closed Merged',),
        (70, 'closed_revoked', 'Closed Revoked',),
        (80, 'closed_voluntary', 'Closed Voluntary',),
        (90, 'expelled', 'Expelled',),
        (100, 'expired', 'Expired',),
        (105, 'expired_licensed', 'Expired Licensed',),
        (110, 'lapsed', 'Lapsed',),
        (120, 'not_approved', 'Not Approved',),
        (130, 'pending', 'Pending',),
        (140, 'pending_voluntary', 'Pending Voluntary',),
        (150, 'suspended', 'Suspended',),
        (160, 'suspended_membership', 'Suspended Membership',),
    )

    mem_status = models.IntegerField(
        choices=MEM_STATUS,
        editable=False,
        null=True,
        blank=True,
    )

    bhs_id = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
    )

    bhs_pk = models.UUIDField(
        null=True,
        blank=True,
        unique=True,
        db_index=True,
    )

    org_sort = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
        editable=False,
    )

    # FKs
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        on_delete=models.SET_NULL,
    )

    objects = OrganizationManager()

    # Internals
    class Meta:
        verbose_name_plural = 'organizations'
        ordering = [
            'org_sort',
        ]

    class JSONAPIMeta:
        resource_name = "organization"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = "{0} [{1}]".format(
            self.name,
            self.code,
        )
        super().save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_organization_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            request.user.is_organization_manager,
        ])

    # Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, *args, **kwargs):
        """Activate the Organization."""
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, *args, **kwargs):
        """Deactivate the Organization."""
        return


class Panelist(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
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

    num = models.IntegerField(
        blank=True,
        null=True,
    )

    KIND = Choices(
        (10, 'official', 'Official'),
        (20, 'practice', 'Practice'),
        (30, 'composite', 'Composite'),
    )

    kind = models.IntegerField(
        choices=KIND,
    )

    CATEGORY = Choices(
        (5, 'drcj', 'DRCJ'),
        (10, 'admin', 'CA'),
        (30, 'music', 'Music'),
        (40, 'performance', 'Performance'),
        (50, 'singing', 'Singing'),
    )

    category = models.IntegerField(
        choices=CATEGORY,
        null=True,
        blank=True,
    )

    # FKs
    round = models.ForeignKey(
        'Round',
        related_name='panelists',
        on_delete=models.CASCADE,
    )

    person = models.ForeignKey(
        'Person',
        related_name='panelists',
        on_delete=models.CASCADE,
    )

    # Internals
    class Meta:
        unique_together = (
            ('round', 'person',)
        )

    class JSONAPIMeta:
        resource_name = "panelist"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = " ".join(filter(None, [
            "{0}".format(self.round),
            "{0}".format(self.person),
            self.get_kind_display(),
        ]))
        super().save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_judge_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            True,
            request.user.is_judge_manager,
        ])


class Participant(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    STATUS = Choices(
        (-10, 'excluded', 'Excluded',),
        (0, 'new', 'New',),
        (10, 'included', 'Included',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    PART = Choices(
        (-1, 'director', 'Director'),
        (1, 'tenor', 'Tenor'),
        (2, 'lead', 'Lead'),
        (3, 'baritone', 'Baritone'),
        (4, 'bass', 'Bass'),
    )

    part = models.IntegerField(
        choices=PART,
        null=True,
        blank=True,
    )

    # FKs
    entry = models.ForeignKey(
        'Entry',
        related_name='participants',
        on_delete=models.CASCADE,
    )

    # member = models.ForeignKey(
    #     'Member',
    #     related_name='participants',
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True,
    # )

    person = models.ForeignKey(
        'Person',
        related_name='participants',
        on_delete=models.CASCADE,
    )

    # Internals
    class Meta:
        unique_together = (
            ('entry', 'person',),
        )

    class JSONAPIMeta:
        resource_name = "participant"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: smart_text(x), [
                    self.entry,
                    self.person,
                ]
            )
        )
        super().save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_convention_manager,
            request.user.is_group_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.entry.session.convention.assignments.filter(
                person__user=request.user,
                category__lte=10,
                kind=10,
            ),
            self.entry.group.members.filter(
                person__user=request.user,
                is_admin=True,
                status__gt=0,
            ),
        ])

    # Participant Transitions
    @fsm_log_by
    @transition(field=status, source=[STATUS.new, STATUS.excluded], target=STATUS.included)
    def include(self, *args, **kwargs):
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.new, STATUS.included], target=STATUS.excluded)
    def exclude(self, *args, **kwargs):
        return


class Person(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    first_name = models.CharField(
        help_text="""
            The first name of the person.""",
        max_length=255,
        blank=False,
    )

    middle_name = models.CharField(
        help_text="""
            The middle name of the person.""",
        max_length=255,
        blank=True,
    )

    last_name = models.CharField(
        help_text="""
            The last name of the person.""",
        max_length=255,
        blank=False,
    )

    nick_name = models.CharField(
        help_text="""
            The nickname of the person.""",
        max_length=255,
        blank=True,
    )

    STATUS = Choices(
        (-20, 'legacy', 'Legacy',),
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'exempt', 'Exempt',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
    )

    spouse = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )

    location = models.CharField(
        help_text="""
            The geographical location of the resource.""",
        max_length=255,
        blank=True,
        default='',
    )

    PART = Choices(
        (-1, 'director', 'Director'),
        (1, 'tenor', 'Tenor'),
        (2, 'lead', 'Lead'),
        (3, 'baritone', 'Baritone'),
        (4, 'bass', 'Bass'),
    )

    part = models.IntegerField(
        choices=PART,
        null=True,
        blank=True,
    )

    GENDER = Choices(
        (10, 'male', 'Male'),
        (20, 'female', 'Female'),
    )

    gender = models.IntegerField(
        choices=GENDER,
        null=True,
        blank=True,
    )

    is_deceased = models.BooleanField(
        default=False,
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
        default='',
    )

    email = models.EmailField(
        help_text="""
            The contact email of the resource.""",
        blank=False,
        unique=True,
    )

    phone = models.CharField(
        help_text="""
            The phone number of the resource.  Include country code.""",
        blank=True,
        max_length=25,
        default='',
    )

    address = models.TextField(
        help_text="""
            The complete address of the resource.""",
        blank=True,
        max_length=1000,
        default='',
    )

    home_phone = models.CharField(
        help_text="""
            The home phone number of the resource.  Include country code.""",
        blank=True,
        max_length=25,
        default='',
    )

    work_phone = models.CharField(
        help_text="""
            The work phone number of the resource.  Include country code.""",
        blank=True,
        max_length=25,
        default='',
    )

    cell_phone = models.CharField(
        help_text="""
            The cell phone number of the resource.  Include country code.""",
        blank=True,
        max_length=25,
        default='',
    )

    airports = ArrayField(
        base_field=models.CharField(
            blank=True,
            max_length=3,
        ),
        null=True,
        blank=True,
    )

    img = CloudinaryRenameField(
        'image',
        null=True,
        blank=True,
    )

    description = models.TextField(
        help_text="""
            A bio of the person.  Max 1000 characters.""",
        blank=True,
        max_length=1000,
        default='',
    )

    notes = models.TextField(
        help_text="""
            Notes (for internal use only).""",
        blank=True,
        default='',
    )

    bhs_id = models.IntegerField(
        null=True,
        blank=True,
        unique=True,
    )

    bhs_pk = models.UUIDField(
        null=True,
        blank=True,
        unique=True,
        db_index=True,
    )

    current_through = models.DateField(
        null=True,
        blank=True,
        editable=False,
    )

    @cached_property
    def full_name(self):
        if self.nick_name:
            nick = "({0})".format(self.nick_name)
        else:
            nick = ""
        full = "{0} {1} {2} {3}".format(
            self.first_name,
            self.middle_name,
            self.last_name,
            nick,
        )
        return " ".join(full.split())

    @cached_property
    def common_name(self):
        if self.nick_name:
            first = self.nick_name
        else:
            first = self.first_name
        return "{0} {1}".format(first, self.last_name)

    @cached_property
    def sort_name(self):
        return "{0}, {1}".format(self.last_name, self.first_name)

    # Person FKs
    user = models.OneToOneField(
        'User',
        related_name='person',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # Internals
    objects = PersonManager()

    class JSONAPIMeta:
        resource_name = "person"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def clean(self):
        pass
        # validate_email(self.email)
        # if hasattr(self, 'user') and not self.email:
        #     raise ValidationError(
        #         {'email': 'User account must have email.'}
        #     )
        # if not hasattr(self, 'user') and self.email:
        #     raise ValidationError(
        #         {'email': 'Person with email should have User account.'}
        #     )
        # if self.status == self.STATUS.exempt and (self.bhs_id or self.bhs_pk):
        #     raise ValidationError(
        #         {'status': 'Exempt users should not be in BHS or MC.'}
        #     )
        # if self.current_through:
        #     if self.status == self.STATUS.active and self.current_through < datetime.date.today():
        #         raise ValidationError(
        #             {'status': 'Active user beyond current_through date.'}
        #         )
        #     if self.status == self.STATUS.inactive and self.current_through > datetime.date.today():
        #         raise ValidationError(
        #             {'status': 'Inactive user within current_through date.'}
        #         )
        # else:
        #     if self.status == self.STATUS.active:
        #         raise ValidationError(
        #             {'status': 'Active status without current_through date.'}
        #         )

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: smart_text(x),
                filter(
                    None, [
                        self.full_name,
                        "[{0}]".format(self.bhs_id),
                    ]
                )
            )
        )
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.user == request.user,
        ])

    # Person transitions
    # @transition(field=status, source=[STATUS.new, STATUS.inactive], target=STATUS.active)
    # def activate(self, *args, **kwargs):
    #     """Activate the Person."""
    #     try:
    #         user = self.user
    #     except ObjectDoesNotExist:
    #         User.objects.create_user(
    #             email=self.email,
    #             person=self,
    #         )
    #         return
    #     user.is_active = True
    #     user.full_clean()
    #     user.save()
    #     return

    # @transition(field=status, source=[STATUS.new, STATUS.active], target=STATUS.inactive)
    # def deactivate(self, *args, **kwargs):
    #     self.user.is_active = False
    #     self.user.save()
    #     """Deactivate the Person."""
    #     return


class Repertory(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
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

    # FKs
    group = models.ForeignKey(
        'Group',
        related_name='repertories',
        on_delete=models.CASCADE,
    )

    chart = models.ForeignKey(
        'Chart',
        related_name='repertories',
        on_delete=models.CASCADE,
    )

    # Internals
    class Meta:
        verbose_name_plural = 'repertories'
        unique_together = (
            ('group', 'chart',),
        )

    class JSONAPIMeta:
        resource_name = "repertory"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: smart_text(x), [
                    self.group,
                    self.chart,
                ]
            )
        )
        super().save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return any([
            request.user.is_convention_manager,
            request.user.is_scoring_manager,
            request.user.is_group_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return any([
            self.group.members.filter(
                person__user=request.user,
                is_admin=True,
                status__gt=0,
            ),
            request.user.is_convention_manager,
            request.user.is_scoring_manager,
        ])

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_convention_manager,
            request.user.is_scoring_manager,
            request.user.is_group_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.group.members.filter(
                person__user=request.user,
                is_admin=True,
                status__gt=0,
            ),
            request.user.is_convention_manager,
            request.user.is_scoring_manager,
        ])

    # Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, *args, **kwargs):
        """Activate the Repertory."""
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, *args, **kwargs):
        """Deactivate the Repertory."""
        return


class Round(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (2, 'listed', 'Listed',),
        (4, 'opened', 'Opened',),
        (8, 'closed', 'Closed',),
        (10, 'verified', 'Verified',),
        (15, 'prepared', 'Prepared',),
        (20, 'started', 'Started',),
        # (25, 'ranked', 'Ranked',),
        (30, 'finished', 'Finished',),
        # (40, 'drafted', 'Drafted',),
        (50, 'announced', 'Announced',),
        # (50, 'final', 'Final',),
        (95, 'archived', 'Archived',),
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

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: smart_text(x), [
                    self.session,
                    self.get_kind_display(),
                ]
            )
        )
        super().save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_scoring_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.session.convention.assignments.filter(
                person__user=request.user,
                category__in=[
                    10,
                    20,
                ],
                kind=10,
            ),
        ])

    # Methods
    def ranking(self, point_total):
        if not point_total:
            return None
        appearances = self.appearances.all()
        points = [appearance.calculate_tot_points() for appearance in appearances]
        points = sorted(points, reverse=True)
        ranking = Ranking(points, start=1)
        rank = ranking.rank(point_total)
        return rank

    # def print_ann(self):
    #     primary = self.session.contests.get(is_primary=True)
    #     contests = self.session.contests.filter(is_primary=False)
    #     winners = []
    #     for contest in contests:
    #         winner = contest.contestants.get(rank=1)
    #         winners.append(winner)
    #     medalists = []
    #     contestants = primary.contestants.filter(
    #         status__gt=0,
    #     ).order_by('-rank')
    #     for contestant in contestants:
    #         medalists.append(contestant)
    #     medalists = medalists[-5:]
    #     tem = get_template('ann.html')
    #     template = tem.render(context={
    #         'primary': primary,
    #         'contests': contests,
    #         'winners': winners,
    #         'medalists': medalists,
    #     })
    #     create_response = create_pdf({
    #         "test": True,
    #         "document_content": template,
    #         "name": "announcements-{0}.pdf".format(id),
    #         "document_type": "pdf",
    #     })
    #     f = ContentFile(create_response)
    #     self.ann_pdf.save(
    #         "{0}.pdf".format(id),
    #         f
    #     )
    #     self.save()
    #     return "Complete"

    # Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.verified)
    def verify(self, *args, **kwargs):
        """Confirm panel and appearances."""
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.prepared)
    def prepare(self, *args, **kwargs):
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.started)
    def start(self, *args, **kwargs):
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.finished)
    def finish(self, *args, **kwargs):
        """Separate advancers and finishers."""
        # TODO This probably should not be hard-coded.
        if self.kind == self.KIND.finals:
            for appearance in self.appearances.all():
                appearance.draw = -1
                appearance.save()
            entries = self.session.entries.exclude(
                status=self.session.entries.model.STATUS.scratched,
            )
            for entry in entries:
                entry.calculate_pdf()
                entry.save()
            contests = self.session.contests.filter(status__gt=0)
            for contest in contests:
                for contestant in contest.contestants.filter(status__gt=0):
                    contestant.calculate()
                    contestant.save()
            self.print_ann()
            return
        if self.kind == self.KIND.quarters:
            spots = 20
        elif self.kind == self.KIND.semis:
            spots = 10
        else:
            raise RuntimeError('No round kind.')
        # Build list of advancing appearances to number of spots available
        ordered_entries = self.session.entries.annotate(
            tot=models.Sum('appearances__songs__scores__points')
        ).order_by('-tot')
        # Check for tie at cutoff
        if spots:
            cutoff = ordered_entries[spots - 1:spots][0].tot
            plus_one = ordered_entries[spots:spots + 1][0].tot
            while cutoff == plus_one:
                spots += 1
                cutoff = ordered_entries[spots - 1:spots][0].tot
                plus_one = ordered_entries[spots:spots + 1][0].tot

        # Get Advancers and finishers
        advancers = list(ordered_entries[:spots])
        cutdown = ordered_entries.filter(
            appearances__round=self,
        )
        finishers = list(cutdown[spots:])

        # Randomize Advancers
        random.shuffle(list(advancers))

        # Set Draw
        i = 1
        for entry in advancers:
            appearance = self.appearances.get(entry=entry)
            appearance.draw = i
            appearance.save()
            i += 1

        # Set draw on finishers to negative one.
        for entry in finishers:
            appearance = self.appearances.get(entry=entry)
            appearance.draw = -1
            appearance.save()

        # TODO Bypassing all this in favor of International-only

        # # Create appearances accordingly
        # # Instantiate the advancing list
        # advancing = []
        # # Only address multi-round contests; single-round awards do not proceed.
        # for contest in self.session.contests.filter(award__rounds__gt=1):
        #     # Qualifiers have an absolute score cutoff
        #     if not contest.award.parent:
        #         # Uses absolute cutoff.
        #         contestants = contest.contestants.filter(
        #             tot_score__gte=contest.award.advance,
        #         )
        #         for contestant in contestants:
        #             advancing.append(contestant.entry)
        #     # Championships are relative.
        #     else:
        #         # Get the top scorer
        #         top = contest.contestants.filter(
        #             rank=1,
        #         ).first()
        #         # Derive the approve threshold from that top score.
        #         approve = top.calculate_tot_score() - 4.0
        #         contestants = contest.contestants.filter(
        #             tot_score__gte=approve,
        #         )
        #         for contestant in contestants:
        #             advancing.append(contestant.entry)
        # # Remove duplicates
        # advancing = list(set(advancing))
        # # Append up to spots available.
        # diff = spots - len(advancing)
        # if diff > 0:
        #     adds = self.appearances.filter(
        #         entry__contestants__contest__award__rounds__gt=1,
        #     ).exclude(
        #         entry__in=advancing,
        #     ).order_by(
        #         '-tot_points',
        #     )[:diff]
        #     for a in adds:
        #         advancing.append(a.entry)
        # random.shuffle(advancing)
        # i = 1
        # for entry in advancing:
        #     next_round.appearances.get_or_create(
        #         entry=entry,
        #         num=i,
        #     )
        #     i += 1
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.announced)
    def announce(self, *args, **kwargs):
        if self.kind != self.KIND.finals:
            round = self.session.rounds.create(
                num=self.num + 1,
                kind=self.kind - 1,
            )
            for appearance in self.appearances.filter(draw__gt=0):
                round.appearances.create(
                    entry=appearance.entry,
                    num=appearance.draw,
                    status=appearance.STATUS.published,
                )
            for appearance in self.appearances.filter(draw__lte=0):
                e = appearance.entry
                e.complete()
                e.save()
            for assignment in self.session.convention.assignments.filter(
                status=Assignment.STATUS.active,
            ):
                round.panelists.create(
                    kind=assignment.kind,
                    category=assignment.category,
                    person=assignment.person,
                )
            round.verify()
            round.save()
            return


class Score(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'verified', 'Verified',),
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
        (30, 'music', 'Music'),
        (40, 'performance', 'Performance'),
        (50, 'singing', 'Singing'),
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

    num = models.IntegerField(
        null=True,
        blank=True,
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

    # person = models.ForeignKey(
    #     'Person',
    #     related_name='scores',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    # )

    panelist = models.ForeignKey(
        'Panelist',
        related_name='scores',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class JSONAPIMeta:
        resource_name = "score"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = str(self.pk)
        super().save(*args, **kwargs)

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
        per_avg = self.song.scores.filter(
            kind=self.song.scores.model.KIND.official,
            category=self.song.scores.model.CATEGORY.performance,
        ).aggregate(
            avg=models.Avg('points')
        )['avg']
        if self.category == self.CATEGORY.performance:
            if abs(self.points - per_avg) > 5:
                log.info("Variance Performance {0}".format(self))
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
    @authenticated_users
    def has_read_permission(request):
        return any([
            True,
            request.user.is_group_manager,
            request.user.is_scoring_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return any([
            # self.song.appearance.entry.entity.officers.filter(
            #     person=request.user,
            #     office__is_group_manager=True,
            #     status__gt=0,
            # ),
        ])

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_scoring_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.song.appearance.round.session.convention.assignments.filter(
                person__user=request.user,
                category__lt=30,
                kind=10,
            ),
        ])


class Session(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (4, 'opened', 'Opened',),
        (8, 'closed', 'Closed',),
        (10, 'verified', 'Verified',),
        (20, 'started', 'Started',),
        (30, 'finished', 'Finished',),
    )

    is_archived = models.BooleanField(
        default=False,
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    KIND = Choices(
        (32, 'chorus', "Chorus"),
        (41, 'quartet', "Quartet"),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of session.  Generally this will be either quartet or chorus.
        """,
        choices=KIND,
    )

    is_invitational = models.BooleanField(
        help_text="""Invite-only (v. Open).""",
        default=False,
    )

    bbscores_report = CloudinaryField(
        null=True,
        blank=True,
        editable=False,
    )

    drcj_report = CloudinaryField(
        null=True,
        blank=True,
        editable=False,
    )

    admins_report = CloudinaryField(
        null=True,
        blank=True,
        editable=False,
    )

    num_rounds = models.IntegerField(
    )

    # FKs
    convention = models.ForeignKey(
        'Convention',
        related_name='sessions',
        on_delete=models.CASCADE,
    )

    # Session Properties
    @property
    def open_date(self):
        return self.convention.open_date

    @property
    def close_date(self):
        return self.convention.close_date

    @property
    def start_date(self):
        return self.convention.start_date

    @property
    def end_date(self):
        return self.convention.end_date

    # Internals
    class JSONAPIMeta:
        resource_name = "session"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: smart_text(x), [
                    self.convention,
                    self.get_kind_display(),
                    'Session',
                ]
            )
        )
        super().save(*args, **kwargs)

    # Methods

    # Session Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return any([
            True,
        ])

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return any([
            True,
        ])

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_convention_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.convention.assignments.filter(
                person__user=request.user,
                category__lt=30,
                kind=10,
            ),
        ])

    # Session Conditions
    def can_open_session(self):
        Contest = config.get_model('Contest')
        return all([
            self.contests.count() > 0,
            self.contests.filter(status=Contest.STATUS.new).count() == 0,
        ])

    def can_close_session(self):
        Entry = config.get_model('Entry')
        return all([
            self.close_date < datetime.date.today(),
            self.entries.filter(status=Entry.STATUS.submitted).count() == 0,
        ])

    # Session Transitions
    @fsm_log_by
    @transition(
        field=status,
        source=STATUS.new,
        target=STATUS.opened,
        conditions=[can_open_session],
    )
    def open(self, *args, **kwargs):
        """Make session available for entry."""
        if not self.is_invitational:
            send_session(self, 'session_open.txt')
        return

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS.opened,
        target=STATUS.closed,
        conditions=[can_close_session]
    )
    def close(self, *args, **kwargs):
        """Make session unavailable and set initial draw."""
        # Remove orphaned entries
        entries = self.entries.filter(
            status=self.entries.model.STATUS.new,
        )
        for entry in entries:
            entry.delete()
        # Withdraw dangling invitations
        entries = self.entries.filter(
            status=self.entries.model.STATUS.invited,
        )
        for entry in entries:
            entry.withdraw()
            entry.save()
        # Set initial draw for all Approved entries.
        entries = self.entries.filter(
            status=self.entries.model.STATUS.approved,
        )
        i = 1
        for entry in entries:
            entry.draw = i
            entry.save()
            i += 1
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.closed, STATUS.verified],
        target=STATUS.verified,
        conditions=[],
    )
    def verify(self, *args, **kwargs):
        """Make draw public."""
        create_bbscores_report(self)
        create_drcj_report(self)
        create_admins_report(self)
        return

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS.verified,
        target=STATUS.started,
        conditions=[],
    )
    def start(self, *args, **kwargs):
        """Get round, seat panel, copy draw."""
        #  Create the export files
        create_bbscores_report(self)
        create_drcj_report(self)
        create_admins_report(self)
        # Get models for constants
        Assignment = config.get_model('Assignment')
        Slot = config.get_model('Slot')
        Entry = config.get_model('Entry')
        Appearance = config.get_model('Appearance')
        # Get the first round.
        round = self.rounds.get(
            num=1,
        )
        for entry in self.entries.filter(status=Entry.STATUS.approved):
            slot = Slot.objects.create(
                num=entry.draw,
                round=round,
            )
            round.appearances.create(
                entry=entry,
                slot=slot,
                num=entry.draw,
                status=Appearance.STATUS.published,
            )
            entry.finalize()
            entry.save()
        for entry in self.entries.filter(status=Entry.STATUS.new):
            entry.delete()
        for assignment in self.convention.assignments.filter(
            status=Assignment.STATUS.active,
        ):
            round.panelists.create(
                kind=assignment.kind,
                category=assignment.category,
                person=assignment.person,
            )
        round.verify()
        round.save()
        return

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS.started,
        target=STATUS.finished,
        conditions=[],
    )
    def finish(self, *args, **kwargs):
        return


class Slot(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
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

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: smart_text(x), [
                    self.round,
                    self.num,
                ]
            )
        )
        super().save(*args, **kwargs)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return any([
            True,
        ])

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return any([
            True,
        ])

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_convention_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.round.session.convention.assignments.filter(
                person__user=request.user,
                category__lt=30,
                kind=10,
            ),
        ])


class Song(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'verified', 'Verified',),
        # (20, 'entered', 'Entered',),
        # (30, 'flagged', 'Flagged',),
        # (35, 'verified', 'Verified',),
        (38, 'finished', 'Finished',),
        (40, 'confirmed', 'Confirmed',),
        (50, 'final', 'Final',),
        (90, 'announced', 'Announced',),
        (95, 'archived', 'Archived',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    num = models.IntegerField(
    )

    # Privates
    rank = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_points = models.IntegerField(
        null=True,
        blank=True,
    )

    per_points = models.IntegerField(
        null=True,
        blank=True,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
    )

    tot_points = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
    )

    per_score = models.FloatField(
        null=True,
        blank=True,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
    )

    tot_score = models.FloatField(
        null=True,
        blank=True,
    )

    # FKs
    appearance = models.ForeignKey(
        'Appearance',
        related_name='songs',
        on_delete=models.CASCADE,
    )

    chart = models.ForeignKey(
        'Chart',
        related_name='songs',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # Internals
    class Meta:
        unique_together = (
            ('appearance', 'num',),
        )

    class JSONAPIMeta:
        resource_name = "song"

    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = " ".join(
            map(
                lambda x: smart_text(x), [
                    self.appearance,
                    self.num,
                ]
            )
        )
        super().save(*args, **kwargs)

    # Methods
    def calculate(self, *args, **kwargs):
        self.mus_points = self.calculate_mus_points()
        self.per_points = self.calculate_per_points()
        self.sng_points = self.calculate_sng_points()
        self.tot_points = self.calculate_tot_points()
        self.mus_score = self.calculate_mus_score()
        self.per_score = self.calculate_per_score()
        self.sng_score = self.calculate_sng_score()
        self.tot_score = self.calculate_tot_score()

    def calculate_mus_points(self):
        return self.scores.filter(
            kind=10,
            category=30,
        ).aggregate(
            tot=models.Sum('points')
        )['tot']

    def calculate_per_points(self):
        return self.scores.filter(
            kind=10,
            category=40,
        ).aggregate(
            tot=models.Sum('points')
        )['tot']

    def calculate_sng_points(self):
        return self.scores.filter(
            kind=10,
            category=50,
        ).aggregate(
            tot=models.Sum('points')
        )['tot']

    def calculate_tot_points(self):
        return self.scores.filter(
            kind=10,
        ).aggregate(
            tot=models.Sum('points')
        )['tot']

    def calculate_mus_score(self):
        return self.scores.filter(
            kind=10,
            category=30,
        ).aggregate(
            tot=models.Avg('points')
        )['tot']

    def calculate_per_score(self):
        return self.scores.filter(
            kind=10,
            category=40,
        ).aggregate(
            tot=models.Avg('points')
        )['tot']

    def calculate_sng_score(self):
        return self.scores.filter(
            kind=10,
            category=50,
        ).aggregate(
            tot=models.Avg('points')
        )['tot']

    def calculate_tot_score(self):
        return self.scores.filter(
            kind=10,
        ).aggregate(
            tot=models.Avg('points')
        )['tot']

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return any([
            True,
        ])

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return any([
            True,
        ])

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_scoring_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            self.appearance.round.session.convention.assignments.filter(
                person__user=request.user,
                category__lt=30,
                kind=10,
            ),
        ])

    # Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.announced)
    def announce(self, *args, **kwargs):
        return


class Venue(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nomen = models.CharField(
        max_length=255,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the resource.""",
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

    location = models.CharField(
        max_length=255,
        blank=True,
    )

    city = models.CharField(
        max_length=255,
        blank=True,
    )

    state = models.CharField(
        max_length=255,
        blank=True,
    )

    airport = models.CharField(
        max_length=3,
        blank=True,
    )

    timezone = TimeZoneField(
        help_text="""
            The local timezone of the venue.""",
        blank=True,
    )

    # Methods
    def __str__(self):
        return self.nomen if self.nomen else str(self.pk)

    def save(self, *args, **kwargs):
        self.nomen = self.name
        super().save(*args, **kwargs)

    # Internals
    class JSONAPIMeta:
        resource_name = "venue"

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return any([
            True,
        ])

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return any([
            True,
        ])

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_convention_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            request.user.is_convention_manager,
        ])


class User(AbstractBaseUser):
    USERNAME_FIELD = settings.USERNAME_FIELD
    REQUIRED_FIELDS = settings.REQUIRED_FIELDS

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
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

    name = models.CharField(
        max_length=255,
        editable=True,
        blank=True,
    )

    email = models.EmailField(
        unique=True,
        editable=True,
    )

    auth0_id = models.CharField(
        max_length=100,
        unique=True,
        editable=False,
        null=True,
        blank=True,
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

    @cached_property
    def is_convention_manager(self):
        try:
            is_manager = bool(self.person.officers.filter(
                office__is_convention_manager=True,
                status__gt=0,
            ))
        except:
            is_manager = False
        return is_manager

    @cached_property
    def is_session_manager(self):
        try:
            is_manager = bool(self.person.officers.filter(
                office__is_session_manager=True,
                status__gt=0,
            ))
        except:
            is_manager = False
        return is_manager

    @cached_property
    def is_scoring_manager(self):
        try:
            is_manager = bool(self.person.officers.filter(
                office__is_scoring_manager=True,
                status__gt=0,
            ))
        except:
            is_manager = False
        return is_manager

    @cached_property
    def is_organization_manager(self):
        try:
            is_manager = bool(self.person.officers.filter(
                office__is_organization_manager=True,
                status__gt=0,
            ))
        except:
            is_manager = False
        return is_manager

    @cached_property
    def is_group_manager(self):
        try:
            is_manager = bool(self.person.members.filter(
                is_admin=True,
                status__gt=0,
            ))
        except:
            is_manager = False
        return is_manager

    @cached_property
    def is_person_manager(self):
        try:
            is_manager = bool(self.person.officers.filter(
                office__is_person_manager=True,
                status__gt=0,
            ))
        except:
            is_manager = False
        return is_manager

    @cached_property
    def is_award_manager(self):
        try:
            is_manager = bool(self.person.officers.filter(
                office__is_award_manager=True,
                status__gt=0,
            ))
        except:
            is_manager = False
        return is_manager

    @cached_property
    def is_judge_manager(self):
        try:
            is_manager = bool(self.person.officers.filter(
                office__is_judge_manager=True,
                status__gt=0,
            ))
        except:
            is_manager = False
        return is_manager

    @cached_property
    def is_chart_manager(self):
        try:
            is_manager = bool(self.person.officers.filter(
                office__is_chart_manager=True,
                status__gt=0,
            ))
        except:
            is_manager = False
        return is_manager

    class JSONAPIMeta:
        resource_name = "user"

    # User Internals
    def __str__(self):
        return self.name

    def clean(self):
        pass
        # if self.email != self.person.email:
        #     raise ValidationError(
        #         {'email': 'Email does not match person'}
        #     )
        # if self.name != self.person.full_name:
        #     raise ValidationError(
        #         {'name': 'Name does not match person'}
        #     )
        # if self.is_active and self.person.status <= 0:
        #     raise ValidationError(
        #         {'name': 'Should not be active.'}
        #     )
        # if not self.is_active and self.person.status > 0:
        #     raise ValidationError(
        #         {'is_active': 'Should be active.'}
        #     )

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    # User Permissions
    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return self == request.user

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return self == request.user

    # User Transitions
    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, *args, **kwargs):
        self.is_active = True
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, *args, **kwargs):
        self.is_active = False
        pass
