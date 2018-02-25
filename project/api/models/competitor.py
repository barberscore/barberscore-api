# Standard Libary
import logging
import uuid

# Third-Party
from cloudinary.models import CloudinaryField
from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel
from ranking import Ranking

# Django
from django.apps import apps as api_apps
from django.db import models
from django.utils.html import format_html
from django.utils.text import slugify

# First-Party
from api.fields import CloudinaryRenameField
from api.storages import CustomMediaCloudinaryStorage
from api.storages import CustomPDFCloudinaryStorage

config = api_apps.get_app_config('api')

log = logging.getLogger(__name__)


def upload_to(instance, filename):
    return 'competitor/{0}'.format(instance.id)


def upload_to_csa(instance, filename):
    return 'competitor/{0}/{1}-csa_report.pdf'.format(
        instance.id,
        slugify(instance.nomen),
    )


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
        (-20, 'finished', 'Finished',),
        (-10, 'missed', 'Missed',),
        (0, 'new', 'New',),
        (10, 'made', 'Made',),
        (20, 'started', 'Started',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    img = CloudinaryRenameField(
        'image',
        null=True,
        blank=True,
    )

    image = models.ImageField(
        upload_to=upload_to,
        blank=True,
        storage=CustomMediaCloudinaryStorage(),
    )

    is_ranked = models.BooleanField(
        help_text="""If the competitor will be ranked in OSS.""",
        default=False,
    )

    is_multi = models.BooleanField(
        help_text="""If the competitor is contesting a multi-round award.""",
        default=False,
    )

    draw = models.IntegerField(
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

    csa_report = CloudinaryField(
        null=True,
        blank=True,
        editable=False,
    )

    csa_report_new = models.FileField(
        upload_to=upload_to_csa,
        blank=True,
        max_length=255,
        storage=CustomPDFCloudinaryStorage(),
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

    entry = models.OneToOneField(
        'Entry',
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
        self.nomen = "{0}; {1}".format(
            self.group,
            self.session,
        )
        super().save(*args, **kwargs)

    # Competitor Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return request.user.is_scoring_manager

    @allow_staff_or_superuser
    @authenticated_users
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

    # Competitor Methods
    def calculate(self):
        self.mus_points = self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=30,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']
        self.per_points = self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=40,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']
        self.sng_points = self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=50,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']

        self.tot_points = self.appearances.filter(
            songs__scores__kind=10,
        ).aggregate(
            tot=models.Sum('songs__scores__points')
        )['tot']
        self.mus_score = self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=30,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']
        self.per_score = self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=40,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']
        self.sng_score = self.appearances.filter(
            songs__scores__kind=10,
            songs__scores__category=50,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']
        self.tot_score = self.appearances.filter(
            songs__scores__kind=10,
        ).aggregate(
            tot=models.Avg('songs__scores__points')
        )['tot']

    def ranking(self):
        points = list(self.session.competitors.filter(
            is_ranked=True,
        ).order_by('-tot_points').values_list('tot_points', flat=True))
        if self.is_ranked:
            ranked = Ranking(points, start=1)
            rank = ranked.rank(self.tot_points)
            self.rank = rank
        else:
            self.rank = None
        return

    # Competitor Transition Conditions

    # Competitor Transitions
    @fsm_log_by
    @transition(field=status, source=[STATUS.started, STATUS.missed], target=STATUS.made)
    def make(self, *args, **kwargs):
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.started, STATUS.made], target=STATUS.missed)
    def miss(self, *args, **kwargs):
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.new, STATUS.missed, STATUS.made], target=STATUS.started)
    def start(self, *args, **kwargs):
        next_round = self.session.rounds.filter(
            status=0,
        ).earliest()
        self.appearances.create(
            round=next_round,
            num=self.draw,
        )
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.new, STATUS.started, STATUS.missed, STATUS.finished], target=STATUS.finished)
    def finish(self, *args, **kwargs):
        create_csa_report(self)
        return
