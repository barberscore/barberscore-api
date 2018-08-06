# Standard Libary
import uuid

# Third-Party

from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel
from ranking import Ranking
from django.utils.functional import cached_property
from django_fsm_log.models import StateLog
from django.contrib.contenttypes.fields import GenericRelation

# Django
from django.db import models
from django.utils.timezone import now
from django.apps import apps

# First-Party
from api.tasks import create_variance_report


class Appearance(TimeStampedModel):
    """
    An appearance of a competitor on stage.

    The Appearance is meant to be a private resource.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (7, 'built', 'Built',),
        (10, 'started', 'Started',),
        (20, 'finished', 'Finished',),
        (30, 'verified', 'Verified',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
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

    pos = models.IntegerField(
        help_text='Actual Participants-on-Stage',
        null=True,
        blank=True,
    )

    legacy_group = models.CharField(
        max_length=255,
        blank=True,
        null=True,
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

    mus_rank = models.IntegerField(
        null=True,
        blank=True,
    )

    per_rank = models.IntegerField(
        null=True,
        blank=True,
    )

    sng_rank = models.IntegerField(
        null=True,
        blank=True,
    )

    tot_rank = models.IntegerField(
        null=True,
        blank=True,
    )

    all_points = models.IntegerField(
        null=True,
        blank=True,
    )

    variance_report = models.FileField(
        null=True,
        blank=True,
    )

    # Appearance FKs
    round = models.ForeignKey(
        'Round',
        related_name='appearances',
        on_delete=models.CASCADE,
    )

    competitor = models.ForeignKey(
        'Competitor',
        related_name='appearances',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='appearances',
    )

    @cached_property
    def round__kind(self):
        return self.round.kind

    # Appearance Internals
    class Meta:
        ordering = [
            '-round__num',
            'num',
        ]
        unique_together = (
            ('round', 'num',),
        )

    class JSONAPIMeta:
        resource_name = "appearance"

    def __str__(self):
        return "{0} {1}".format(
            str(self.competitor),
            str(self.round),
        )

    # Methods
    def calculate(self):
        self.mus_points = self.songs.filter(
            scores__kind=10,
            scores__category=30,
        ).aggregate(
            tot=models.Sum('scores__points')
        )['tot']
        self.per_points = self.songs.filter(
            scores__kind=10,
            scores__category=40,
        ).aggregate(
            tot=models.Sum('scores__points')
        )['tot']
        self.sng_points = self.songs.filter(
            scores__kind=10,
            scores__category=50,
        ).aggregate(
            tot=models.Sum('scores__points')
        )['tot']

        self.tot_points = self.songs.filter(
            scores__kind=10,
        ).aggregate(
            tot=models.Sum('scores__points')
        )['tot']
        self.mus_score = self.songs.filter(
            scores__kind=10,
            scores__category=30,
        ).aggregate(
            tot=models.Avg('scores__points')
        )['tot']
        self.per_score = self.songs.filter(
            scores__kind=10,
            scores__category=40,
        ).aggregate(
            tot=models.Avg('scores__points')
        )['tot']
        self.sng_score = self.songs.filter(
            scores__kind=10,
            scores__category=50,
        ).aggregate(
            tot=models.Avg('scores__points')
        )['tot']
        self.tot_score = self.songs.filter(
            scores__kind=10,
        ).aggregate(
            tot=models.Avg('scores__points')
        )['tot']
        self.all_points = self.songs.aggregate(
            tot=models.Sum('scores__points')
        )['tot']


    # Appearance Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return any([
            self.round.status == self.round.STATUS.finished,
            self.round.session.convention.assignments.filter(
                person__user=request.user,
                status__gt=0,
                category__lte=10,
            ),
        ])

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_round_manager,
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            all([
                self.round.session.convention.assignments.filter(
                    person__user=request.user,
                    status__gt=0,
                    category__lte=10,
                ),
                self.round.status != self.round.STATUS.finished,
            ]),
        ])

    # Appearance Conditions
    def can_verify(self):
        if self.competitor.group.kind == self.competitor.group.KIND.chorus and not self.pos:
            is_pos = False
        else:
            is_pos = True
        return all([
            is_pos,
        ])

    # Appearance Transitions
    @fsm_log_by
    @transition(field=status, source=[STATUS.new], target=STATUS.built)
    def build(self, *args, **kwargs):
        Grid = apps.get_model('api.grid')
        Panelist = apps.get_model('api.panelist')
        grid, created = Grid.objects.get_or_create(
            round=self.round,
            num=self.num,
        )
        grid.appearance = self
        grid.save()
        panelists = self.round.panelists.filter(
            category__gt=Panelist.CATEGORY.ca,
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
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.built], target=STATUS.started)
    def start(self, *args, **kwargs):
        self.actual_start = now()
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.started], target=STATUS.finished)
    def finish(self, *args, **kwargs):
        self.actual_finish = now()
        return

    @fsm_log_by
    @transition(field=status, source='*', target=STATUS.verified, conditions=[can_verify])
    def verify(self, *args, **kwargs):
        switch = False
        for song in self.songs.all():
            song.calculate()
            song.save()
            variance = song.check_variance()
            if variance:
                switch = True
        if switch:
            create_variance_report(self)
        else:
            self.variance_report = None
        self.calculate()
        self.competitor.calculate()
        self.competitor.save()
        return
