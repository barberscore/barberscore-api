
# Standard Library
import uuid
import pydf
from builtins import round as rnd

from random import randint

# Third-Party
import django_rq
from django_fsm import FSMIntegerField
from django.core.files.base import ContentFile
from django_fsm import transition
from django_fsm import RETURN_VALUE
from django_fsm_log.decorators import fsm_log_by
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel
from django.contrib.postgres.fields import ArrayField, JSONField

# Django
from django.apps import apps
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg
from django.db.models import Q
from django.db.models import Sum
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.template.loader import render_to_string
from django.utils.text import slugify


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
        (25, 'variance', 'Variance',),
        (30, 'verified', 'Verified',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    num = models.IntegerField(
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

    is_private = models.BooleanField(
        help_text="""Copied from entry.""",
        default=False,
    )

    is_multi = models.BooleanField(
        help_text="""If the competitor is contesting a multi-round award.""",
        default=False,
    )

    participants = models.CharField(
        help_text='Director(s) or Members (listed TLBB)',
        max_length=255,
        blank=True,
        default='',
    )

    representing = models.CharField(
        help_text='Representing entity',
        max_length=255,
        blank=True,
        default='',
    )

    contesting = ArrayField(
        help_text='Award numbers contestanting',
        base_field=models.IntegerField(
            null=True,
            blank=True,
        ),
        null=True,
        blank=True,
    )

    legacy_num = models.IntegerField(
        null=True,
        blank=True,
    )

    # Privates
    stats = JSONField(
        null=True,
        blank=True,
    )

    variance_report = models.FileField(
        max_length=255,
        null=True,
        blank=True,
    )

    run_points = models.IntegerField(
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
        on_delete=models.CASCADE,
    )

    group = models.ForeignKey(
        'Group',
        related_name='appearances',
        on_delete=models.CASCADE,
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
    def clean(self):
        if self.group.kind != self.round.session.kind:
            raise ValidationError(
                {'group': 'Group kind must match session'}
            )

    class Meta:
        ordering = [
            '-round__num',
            'num',
        ]
        unique_together = (
            ('round', 'competitor'),
            ('round', 'num'),
            ('round', 'group'),
        )

    class JSONAPIMeta:
        resource_name = "appearance"

    def __str__(self):
        return "{0} {1}".format(
            str(self.group),
            str(self.round),
        )

    # Methods
    def get_variance(self):
        Score = apps.get_model('api.score')
        Panelist = apps.get_model('api.panelist')
        songs = self.songs.order_by('num')
        scores = Score.objects.filter(
            panelist__kind=Panelist.KIND.official,
            song__in=songs,
        ).order_by(
            'category',
            'panelist__person__last_name',
            'song__num',
        )
        panelists = self.round.panelists.filter(
            kind=Panelist.KIND.official,
            category__gt=Panelist.CATEGORY.ca,
        ).order_by(
            'category',
            'person__last_name',
        )
        variances = []
        for song in songs:
            variances.extend(song.dixons)
            variances.extend(song.asterisks)
        variances = list(set(variances))
        off_points = scores.aggregate(sum=Sum('points'))['sum']
        context = {
            'appearance': self,
            'songs': songs,
            'scores': scores,
            'panelists': panelists,
            'variances': variances,
            'off_points': off_points,
        }
        rendered = render_to_string('variance.html', context)
        pdf = pydf.generate_pdf(rendered, enable_smart_shrinking=False)
        content = ContentFile(pdf)
        return content


    def mock(self):
        # Mock Appearance
        Chart = apps.get_model('api.chart')
        prelim = None
        if self.group.kind == self.group.KIND.chorus:
            pos = self.group.members.filter(
                status=self.group.members.model.STATUS.active,
            ).count()
            self.pos = pos
        if not prelim:
            average = self.group.competitors.filter(
                status=self.group.competitors.model.STATUS.finished,
            ).aggregate(avg=Avg('tot_score'))['avg']
            if average:
                prelim = average
            else:
                prelim = randint(65, 80)
        songs = self.songs.all()
        for song in songs:
            song.chart = Chart.objects.filter(
                status=Chart.STATUS.active
            ).order_by("?").first()
            song.save()
            scores = song.scores.all()
            for score in scores:
                d = randint(-4, 4)
                score.points = prelim + d
                score.save()
        if self.status == self.STATUS.new:
            raise RuntimeError("Out of state")
        if self.status == self.STATUS.built:
            self.start()
            self.finish()
            self.verify()
            return
        if self.status == self.STATUS.started:
            self.finish()
            self.verify()
            return
        if self.status == self.STATUS.finished:
            self.verify()
            return


    def calculate(self):
        Score = apps.get_model('api.score')
        Panelist = apps.get_model('api.panelist')
        tot = Sum('points')
        mus = Sum('points', filter=Q(panelist__category=Panelist.CATEGORY.music))
        per = Sum('points', filter=Q(panelist__category=Panelist.CATEGORY.performance))
        sng = Sum('points', filter=Q(panelist__category=Panelist.CATEGORY.singing))
        officials = Score.objects.filter(
            song__appearance=self,
            panelist__kind=Panelist.KIND.official,
        ).annotate(
            tot=tot,
            mus=mus,
            per=per,
            sng=sng,
        )
        tot = officials.aggregate(
            sum=Sum('points'),
            avg=Avg('points'),
        )
        mus = officials.filter(
            panelist__category=Panelist.CATEGORY.music,
        ).aggregate(
            sum=Sum('points'),
            avg=Avg('points'),
        )
        per = officials.filter(
            panelist__category=Panelist.CATEGORY.performance,
        ).aggregate(
            sum=Sum('points'),
            avg=Avg('points'),
        )
        sng = officials.filter(
            panelist__category=Panelist.CATEGORY.singing,
        ).aggregate(
            sum=Sum('points'),
            avg=Avg('points'),
        )

    def check_variance(self):
        variance = False
        for song in self.songs.all():
            song.calculate()
            asterisks = song.get_asterisks()
            if asterisks:
                song.asterisks = asterisks
                variance = True
            dixons = song.get_dixons()
            if dixons:
                song.dixons = dixons
                variance = True
            song.save()
        return variance


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
        try:
            if self.group.kind == self.group.KIND.chorus and not self.pos:
                is_pos = False
            else:
                is_pos = True
        except AttributeError:
            is_pos = False
        return all([
            is_pos,
            not self.songs.filter(scores__points__isnull=True),
        ])

    # Appearance Transitions
    @fsm_log_by
    @transition(field=status, source=[STATUS.new], target=STATUS.built)
    def build(self, *args, **kwargs):
        Grid = apps.get_model('api.grid')
        Panelist = apps.get_model('api.panelist')
        grid, _ = Grid.objects.get_or_create(
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
    @transition(field=status, source=[STATUS.started, STATUS.verified], target=STATUS.finished)
    def finish(self, *args, **kwargs):
        self.actual_finish = now()
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.finished, STATUS.verified, STATUS.variance],
        target=RETURN_VALUE(STATUS.variance, STATUS.verified,),
        conditions=[can_verify],
    )
    def verify(self, *args, **kwargs):
        if self.status == self.STATUS.finished:
            variance = self.check_variance()
            if variance:
                content = self.get_variance()
                self.variance_report.save(
                    "{0}-variance-report".format(
                        slugify(self.group.name),
                    ),
                    content,
                )
        else:
            variance = None
        for song in self.songs.all():
            song.calculate()
            song.save()
        self.calculate()
        # self.competitor.calculate()
        # self.competitor.save()
        # django_rq.enqueue(
        #     self.competitor.save_csa,
        # )
        return self.STATUS.variance if variance else self.STATUS.verified
