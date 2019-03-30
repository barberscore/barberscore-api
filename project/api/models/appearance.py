
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
from django.db.models import Max
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.template.loader import render_to_string

from api.fields import FileUploadPath
from api.tasks import send_email

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
        (-30, 'disqualified', 'Disqualified',),
        (-20, 'scratched', 'Scratched',),
        (-10, 'completed', 'Completed',),
        (0, 'new', 'New',),
        (7, 'built', 'Built',),
        (10, 'started', 'Started',),
        (20, 'finished', 'Finished',),
        (25, 'variance', 'Variance',),
        (30, 'verified', 'Verified',),
        (40, 'advanced', 'Advanced',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    num = models.IntegerField(
        help_text="""The order of appearance for this round.""",
    )

    draw = models.IntegerField(
        help_text="""The draw for the next round.""",
        null=True,
        blank=True,
    )

    is_private = models.BooleanField(
        help_text="""Copied from entry.""",
        default=False,
    )

    is_single = models.BooleanField(
        help_text="""Single-round competitor""",
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

    actual_start = models.DateTimeField(
        help_text="""
            The actual appearance datetime.""",
        null=True,
        blank=True,
    )

    actual_finish = models.DateTimeField(
        help_text="""
            The actual appearance datetime.""",
        null=True,
        blank=True,
    )

    pos = models.IntegerField(
        help_text='Actual Participants-on-Stage',
        null=True,
        blank=True,
    )

    legacy_num = models.IntegerField(
        null=True,
        blank=True,
    )

    stats = JSONField(
        null=True,
        blank=True,
    )

    variance_report = models.FileField(
        upload_to=FileUploadPath(),
        blank=True,
    )

    csa = models.FileField(
        upload_to=FileUploadPath(),
        blank=True,
    )

    # Appearance FKs
    round = models.ForeignKey(
        'Round',
        related_name='appearances',
        on_delete=models.CASCADE,
    )

    group = models.ForeignKey(
        'Group',
        related_name='appearances',
        on_delete=models.CASCADE,
    )

    entry = models.ForeignKey(
        'Entry',
        related_name='appearances',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
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
            ('round', 'num'),
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

        # Songs Block
        songs = self.songs.annotate(
            tot_score=Avg(
                'scores__points',
                filter=Q(
                    scores__panelist__kind=Panelist.KIND.official,
                ),
            ),
        ).order_by('num')
        scores = Score.objects.filter(
            panelist__kind=Panelist.KIND.official,
            song__appearance=self,
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
        tot_points = scores.aggregate(sum=Sum('points'))['sum']
        context = {
            'appearance': self,
            'songs': songs,
            'scores': scores,
            'panelists': panelists,
            'variances': variances,
            'tot_points': tot_points,
        }
        rendered = render_to_string('reports/variance.html', context)
        pdf = pydf.generate_pdf(rendered, enable_smart_shrinking=False)
        content = ContentFile(pdf)
        return content

    def save_variance(self):
        content = self.get_variance()
        self.variance_report.save("variance_report", content)

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

    def check_variance(self):
        # Set flag
        variance = False
        # Run checks for all songs and save.
        for song in self.songs.all():
            asterisks = song.get_asterisks()
            if asterisks:
                song.asterisks = asterisks
                variance = True
            dixons = song.get_dixons()
            if dixons:
                song.dixons = dixons
                variance = True
            if variance:
                song.save()
        return variance

    def get_csa(self):
        if self.status != self.STATUS.completed:
            raise ValueError("Must be completed to generate CSA")
        Panelist = apps.get_model('api.panelist')
        Song = apps.get_model('api.song')
        Score = apps.get_model('api.score')

        # Appearancers Block
        group = self.group
        stats = Score.objects.select_related(
            'song__appearance__group',
            'song__appearance__round__session',
            'song__appearance__round',
            'panelist',
        ).filter(
            song__appearance__group=self.group,
            song__appearance__round__session=self.round.session,
            song__appearance__round__status=self.round.STATUS.finished,
            song__appearance__round__num__lte=self.round.num,
            panelist__kind=Panelist.KIND.official,
        ).aggregate(
            max=Max(
                'song__appearance__round__num',
            ),
            tot_points=Sum(
                'points',
            ),
            mus_points=Sum(
                'points',
                filter=Q(
                    panelist__category=Panelist.CATEGORY.music,
                )
            ),
            per_points=Sum(
                'points',
                filter=Q(
                    panelist__category=Panelist.CATEGORY.performance,
                )
            ),
            sng_points=Sum(
                'points',
                filter=Q(
                    panelist__category=Panelist.CATEGORY.singing,
                )
            ),
            tot_score=Avg(
                'points',
            ),
            mus_score=Avg(
                'points',
                filter=Q(
                    panelist__category=Panelist.CATEGORY.music,
                )
            ),
            per_score=Avg(
                'points',
                filter=Q(
                    panelist__category=Panelist.CATEGORY.performance,
                )
            ),
            sng_score=Avg(
                'points',
                filter=Q(
                    panelist__category=Panelist.CATEGORY.singing,
                )
            ),
        )
        appearances = Appearance.objects.select_related(
            'group',
            'round',
            'round__session',
        ).prefetch_related(
            'songs__scores',
            'songs__scores__panelist',
        ).filter(
            group=self.group,
            round__session=self.round.session,
            round__status=self.round.STATUS.finished,
            round__num__lte=self.round.num,
        ).annotate(
            tot_points=Sum(
                'songs__scores__points',
                filter=Q(
                    songs__scores__panelist__kind=Panelist.KIND.official,
                ),
            ),
            mus_points=Sum(
                'songs__scores__points',
                filter=Q(
                    songs__scores__panelist__kind=Panelist.KIND.official,
                    songs__scores__panelist__category=Panelist.CATEGORY.music,
                ),
            ),
            per_points=Sum(
                'songs__scores__points',
                filter=Q(
                    songs__scores__panelist__kind=Panelist.KIND.official,
                    songs__scores__panelist__category=Panelist.CATEGORY.performance,
                ),
            ),
            sng_points=Sum(
                'songs__scores__points',
                filter=Q(
                    songs__scores__panelist__kind=Panelist.KIND.official,
                    songs__scores__panelist__category=Panelist.CATEGORY.singing,
                ),
            ),
            tot_score=Avg(
                'songs__scores__points',
                filter=Q(
                    songs__scores__panelist__kind=Panelist.KIND.official,
                ),
            ),
            mus_score=Avg(
                'songs__scores__points',
                filter=Q(
                    songs__scores__panelist__kind=Panelist.KIND.official,
                    songs__scores__panelist__category=Panelist.CATEGORY.music,
                ),
            ),
            per_score=Avg(
                'songs__scores__points',
                filter=Q(
                    songs__scores__panelist__kind=Panelist.KIND.official,
                    songs__scores__panelist__category=Panelist.CATEGORY.performance,
                ),
            ),
            sng_score=Avg(
                'songs__scores__points',
                filter=Q(
                    songs__scores__panelist__kind=Panelist.KIND.official,
                    songs__scores__panelist__category=Panelist.CATEGORY.singing,
                ),
            ),
        )

        # Monkeypatch
        for key, value in stats.items():
            setattr(group, key, value)
        for appearance in appearances:
            songs = appearance.songs.prefetch_related(
                'scores',
                'scores__panelist',
            ).order_by(
                'num',
            ).annotate(
                tot_score=Avg(
                    'scores__points',
                    filter=Q(
                        scores__panelist__kind=Panelist.KIND.official,
                    ),
                ),
                mus_score=Avg(
                    'scores__points',
                    filter=Q(
                        scores__panelist__kind=Panelist.KIND.official,
                        scores__panelist__category=Panelist.CATEGORY.music,
                    ),
                ),
                per_score=Avg(
                    'scores__points',
                    filter=Q(
                        scores__panelist__kind=Panelist.KIND.official,
                        scores__panelist__category=Panelist.CATEGORY.performance,
                    ),
                ),
                sng_score=Avg(
                    'scores__points',
                    filter=Q(
                        scores__panelist__kind=Panelist.KIND.official,
                        scores__panelist__category=Panelist.CATEGORY.singing,
                    ),
                ),
                tot_points=Sum(
                    'scores__points',
                    filter=Q(
                        scores__panelist__kind=Panelist.KIND.official,
                    ),
                ),
                mus_points=Sum(
                    'scores__points',
                    filter=Q(
                        scores__panelist__kind=Panelist.KIND.official,
                        scores__panelist__category=Panelist.CATEGORY.music,
                    ),
                ),
                per_points=Sum(
                    'scores__points',
                    filter=Q(
                        scores__panelist__kind=Panelist.KIND.official,
                        scores__panelist__category=Panelist.CATEGORY.performance,
                    ),
                ),
                sng_points=Sum(
                    'scores__points',
                    filter=Q(
                        scores__panelist__kind=Panelist.KIND.official,
                        scores__panelist__category=Panelist.CATEGORY.singing,
                    ),
                ),
            )
            for song in songs:
                penalties_map = {
                    10: "†",
                    30: "‡",
                    40: "✠",
                    50: "✶",
                }
                items = " ".join([penalties_map[x] for x in song.penalties])
                song.penalties_patched = items
            appearance.songs_patched = songs
        group.appearances_patched = appearances

        # Panelists
        panelists = Panelist.objects.select_related(
            'person',
        ).filter(
            kind=Panelist.KIND.official,
            round__session=self.round.session,
            round__num=1,
            category__gt=10,
        ).order_by('num')


        # Score Block
        initials = [x.person.initials for x in panelists]
        songs = Song.objects.filter(
            appearance__round__session=self.round.session,
            appearance__group=self.group,
        ).order_by(
            'appearance__round__kind',
            'num',
        )
        for song in songs:
            scores = song.scores.filter(
                panelist__kind=Panelist.KIND.official,
            ).order_by('panelist__num')
            class_map = {
                Panelist.CATEGORY.music: 'warning',
                Panelist.CATEGORY.performance: 'success',
                Panelist.CATEGORY.singing: 'info',
            }
            items = []
            for score in scores:
                items.append((score.points, class_map[score.panelist.category]))
            song.scores_patched = items

        # Category Block
        categories = {
            'Music': [],
            'Performance': [],
            'Singing': [],
        }
        # panelists from above
        for panelist in panelists:
            item = categories[panelist.get_category_display()]
            item.append(panelist.person.common_name)

        # Penalties Block
        array = Song.objects.filter(
            appearance__round__session=self.round.session,
            appearance__group=self.group,
            penalties__len__gt=0,
        ).distinct().values_list('penalties', flat=True)
        penalties_map = {
            10: "† Score(s) penalized due to violation of Article IX.A.1 of the BHS Contest Rules.",
            30: "‡ Score(s) penalized due to violation of Article IX.A.2 of the BHS Contest Rules.",
            40: "✠ Score(s) penalized due to violation of Article IX.A.3 of the BHS Contest Rules.",
            50: "✶ Score(s) penalized due to violation of Article X.B of the BHS Contest Rules.",
        }
        penalties = sorted(list(set(penalties_map[x] for l in array for x in l)))

        context = {
            'appearance': self,
            'round': self.round,
            'group': group,
            'initials': initials,
            'songs': songs,
            'categories': categories,
            'penalties': penalties,
        }
        rendered = render_to_string('reports/csa.html', context)
        file = pydf.generate_pdf(rendered)
        content = ContentFile(file)
        return content

    def save_csa(self):
        content = self.get_csa()
        self.csa.save('csa', content)

    def queue_notification(self, template, context=None):
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
        body = render_to_string(template, context)
        subject = "[Barberscore] {0} Notification".format(
            self.group.name,
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
    @transition(
        field=status,
        source=[STATUS.new],
        target=STATUS.built,
    )
    def build(self, *args, **kwargs):
        """Sets up the Appearance."""
        # Grid = apps.get_model('api.grid')
        Panelist = apps.get_model('api.panelist')
        # grid, _ = Grid.objects.get_or_create(
        #     round=self.round,
        #     num=self.num,
        # )
        # grid.appearance = self
        # grid.save()
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
    @transition(
        field=status,
        source=[STATUS.built],
        target=STATUS.started,
    )
    def start(self, *args, **kwargs):
        """Indicates when they start singing."""
        self.actual_start = now()
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.started],
        target=STATUS.finished,
    )
    def finish(self, *args, **kwargs):
        """Indicates when they finish singing."""
        self.actual_finish = now()
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.finished, STATUS.variance],
        target=RETURN_VALUE(STATUS.variance, STATUS.verified,),
        conditions=[can_verify],
    )
    def verify(self, *args, **kwargs):
        # Checks for variance.  Returns Verified or Variance accordingly.
        if self.status == self.STATUS.finished:
            variance = self.check_variance()
            if variance:
                # Run variance report and save file.
                self.save_variance()
        # Variance is only checked once.
        else:
            variance = False
        return self.STATUS.variance if variance else self.STATUS.verified

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.verified],
        target=STATUS.completed,
    )
    def complete(self, *args, **kwargs):
        # Completes the Group.
        # Notify the group?
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[STATUS.verified],
        target=STATUS.advanced,
    )
    def advance(self, *args, **kwargs):
        # Advances the Group.
        # Notify the group?
        return

    @fsm_log_by
    @transition(
        field=status,
        source=[
            STATUS.new,
            STATUS.built,
        ],
        target=STATUS.scratched,
    )
    def scratch(self, *args, **kwargs):
        # Scratches the group.
        # Notify the group?
        return

    @fsm_log_by
    @transition(
        field=status,
        source='*',
        target=STATUS.disqualified,
    )
    def disqualify(self, *args, **kwargs):
        # Disqualify the group.
        # Notify the group?
        return

