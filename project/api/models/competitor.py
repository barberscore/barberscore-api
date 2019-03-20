
# Standard Library
import logging
import uuid
from builtins import round as rnd

# Third-Party
import pydf
import django_rq
from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel
from django.contrib.postgres.fields import ArrayField

# Django
from django.apps import apps
from django.contrib.contenttypes.fields import GenericRelation
from django.core.files.base import ContentFile
from django.db import models
from django.db.models import Avg
from django.db.models import Q
from django.db.models import Sum
from django.template.loader import render_to_string
from django.utils.text import slugify

# First-Party
from api.fields import UploadPath
from api.tasks import send_email

log = logging.getLogger(__name__)


class Competitor(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (-30, 'disqualified', 'Disqualified',),
        (-20, 'scratched', 'Scratched',),
        (-10, 'finished', 'Finished',),
        (0, 'new', 'New',),
        (10, 'started', 'Started',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    image = models.ImageField(
        upload_to=UploadPath(),
        null=True,
        blank=True,
    )

    is_private = models.BooleanField(
        help_text="""Copied from entry.""",
        default=False,
    )

    is_ranked = models.BooleanField(
        help_text="""If the competitor will be ranked in OSS.""",
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

    pos = models.IntegerField(
        help_text='Actual Participants-on-Stage',
        null=True,
        blank=True,
    )

    draw = models.IntegerField(
        null=True,
        blank=True,
    )

    legacy_group = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    # rank = models.IntegerField(
    #     null=True,
    #     blank=True,
    # )

    # mus_points = models.IntegerField(
    #     null=True,
    #     blank=True,
    # )

    # per_points = models.IntegerField(
    #     null=True,
    #     blank=True,
    # )

    # sng_points = models.IntegerField(
    #     null=True,
    #     blank=True,
    # )

    # tot_points = models.IntegerField(
    #     null=True,
    #     blank=True,
    # )

    # mus_score = models.FloatField(
    #     null=True,
    #     blank=True,
    # )

    # per_score = models.FloatField(
    #     null=True,
    #     blank=True,
    # )

    # sng_score = models.FloatField(
    #     null=True,
    #     blank=True,
    # )

    # tot_score = models.FloatField(
    #     null=True,
    #     blank=True,
    # )

    # mus_rank = models.IntegerField(
    #     null=True,
    #     blank=True,
    # )

    # per_rank = models.IntegerField(
    #     null=True,
    #     blank=True,
    # )

    # sng_rank = models.IntegerField(
    #     null=True,
    #     blank=True,
    # )

    # tot_rank = models.IntegerField(
    #     null=True,
    #     blank=True,
    # )

    csa = models.FileField(
        max_length=255,
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

    entry = models.OneToOneField(
        'Entry',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='competitors',
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
        return "{0} {1}".format(
            self.session,
            self.group,
        )

    # Competitor Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return any([
            self.status == self.STATUS.finished,
            self.session.convention.assignments.filter(
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
                self.session.convention.assignments.filter(
                    person__user=request.user,
                    status__gt=0,
                    category__lte=10,
                ),
                self.status != self.STATUS.finished,
            ]),
        ])

    # Competitor Methods
    def calculate(self):
        Score = apps.get_model('api.score')
        Panelist = apps.get_model('api.panelist')
        tot = Sum('points')
        mus = Sum('points', filter=Q(panelist__category=Panelist.CATEGORY.music))
        per = Sum('points', filter=Q(panelist__category=Panelist.CATEGORY.performance))
        sng = Sum('points', filter=Q(panelist__category=Panelist.CATEGORY.singing))
        officials = Score.objects.filter(
            song__appearance__round__session__competitors__in=self,
            song__appearance__num__gt=0,
            panelist__kind=Panelist.KIND.official,
        ).distinct(
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
        self.tot_points = tot['sum']
        self.tot_score = tot['avg']
        self.mus_points = mus['sum']
        self.mus_score = mus['avg']
        self.per_points = per['sum']
        self.per_score = per['avg']
        self.sng_points = sng['sum']
        self.sng_score = sng['avg']

    def get_csa(self):
        Panelist = apps.get_model('api.panelist')
        Member = apps.get_model('api.member')
        Song = apps.get_model('api.song')
        panelists = Panelist.objects.filter(
            kind=Panelist.KIND.official,
            round__session=self.session,
            category__gt=Panelist.CATEGORY.ca,
        ).distinct(
        ).order_by(
            'category',
            'person__last_name',
        )
        appearances = self.appearances.order_by(
            '-num',
        ).prefetch_related(
            'songs',
        )
        songs = Song.objects.select_related(
            'chart',
        ).filter(
            appearance__round__session__competitors__in=self,
        ).prefetch_related(
            'scores',
            'scores__panelist__person',
        ).order_by(
            '-appearance__round__num',
            'num',
        )
        context = {
            'competitor': self,
            'panelists': panelists,
            'appearances': appearances,
            'songs': songs,
        }
        rendered = render_to_string('csa.html', context)
        file = pydf.generate_pdf(rendered)
        content = ContentFile(file)
        return content

    def save_csa(self):
        content = self.get_csa()
        self.refresh_from_db()
        self.csa.save(
            "{0}-csa".format(
                slugify(self.group.name),
            ),
            content,
        )


    def queue_csa(self):
        officers = self.group.officers.filter(
            status__gt=0,
            person__email__isnull=False,
        )
        if not officers:
            raise RuntimeError("No officers for {0}".format(self.group))
        to = ["{0} <{1}>".format(officer.person.common_name.replace(",",""), officer.person.email) for officer in officers]
        cc = []
        if self.group.kind == self.group.KIND.quartet:
            members = self.group.members.filter(
                status__gt=0,
                person__email__isnull=False,
            ).exclude(
                person__officers__in=officers,
            ).distinct()
            for member in members:
                cc.append(
                    "{0} <{1}>".format(member.person.common_name.replace(",",""), member.person.email)
                )
        # Ensure uniqueness
        to = list(set(to))
        cc = list(set(cc))
        context = {'competitor': self}
        body = render_to_string('csa.txt', context)
        subject = "[Barberscore] {0} {1} {2} Session CSA".format(
            self.group.name,
            self.session.convention.name,
            self.session.get_kind_display(),
        )
        queue = django_rq.get_queue('high')
        result = queue.enqueue(
            send_email,
            subject=subject,
            body=body,
            to=to,
            cc=cc,
        )
        return result


    # Competitor Transition Conditions

    # Competitor Transitions
    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.new, STATUS.started, STATUS.finished],
        target=STATUS.started,
    )
    def start(self, *args, **kwargs):
        # Notification?
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.new, STATUS.started, STATUS.finished],
        target=STATUS.finished,
    )
    def finish(self, *args, **kwargs):
        # self.queue_csa()
        return

    @fsm_log_by
    @transition(
        field=status,
        source='*',
        target=STATUS.scratched,
    )
    def scratch(self, *args, **kwargs):
        self.tot_rank = None
        self.mus_rank = None
        self.per_rank = None
        self.sng_rank = None
        self.tot_points = None
        self.mus_points = None
        self.per_points = None
        self.sng_points = None
        self.tot_score = None
        self.mus_score = None
        self.per_score = None
        self.sng_score = None
        appearances = self.appearances.all()
        appearances.delete()
        return

    @fsm_log_by
    @transition(
        field=status,
        source='*',
        target=STATUS.disqualified,
    )
    def disqualify(self, *args, **kwargs):
        return
