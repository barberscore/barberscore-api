
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
from django.contrib.postgres.fields import ArrayField, JSONField

# Django
from django.apps import apps
from django.contrib.contenttypes.fields import GenericRelation
from django.core.files.base import ContentFile
from django.db import models
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.db.models import Sum, Max, Avg

# First-Party
from api.fields import ImageUploadPath
from api.fields import FileUploadPath
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
        upload_to=ImageUploadPath(),
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

    draw = models.IntegerField(
        help_text='The initial draw',
        null=True,
        blank=True,
    )

    legacy_group = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    stats = JSONField(
        null=True,
        blank=True,
    )

    csa = models.FileField(
        upload_to=FileUploadPath(),
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
    def get_csa(self):
        Panelist = apps.get_model('api.panelist')
        Song = apps.get_model('api.song')
        Score = apps.get_model('api.score')

        # Appearancers Block
        scores = Score.objects.filter(
            song__appearance__competitor=self,
        ).aggregate(
            max=Max(
                'song__appearance__round__num',
                filter=Q(
                    song__appearance__round__num__gt=0,
                ),
            ),
            tot_points=Sum(
                'points',
                filter=Q(
                    panelist__kind=Panelist.KIND.official,
                )
            ),
            mus_points=Sum(
                'points',
                filter=Q(
                    panelist__kind=Panelist.KIND.official,
                    panelist__category=Panelist.CATEGORY.music,
                )
            ),
            per_points=Sum(
                'points',
                filter=Q(
                    panelist__kind=Panelist.KIND.official,
                    panelist__category=Panelist.CATEGORY.performance,
                )
            ),
            sng_points=Sum(
                'points',
                filter=Q(
                    panelist__kind=Panelist.KIND.official,
                    panelist__category=Panelist.CATEGORY.singing,
                )
            ),
            tot_score=Avg(
                'points',
                filter=Q(
                    panelist__kind=Panelist.KIND.official,
                )
            ),
            mus_score=Avg(
                'points',
                filter=Q(
                    panelist__kind=Panelist.KIND.official,
                    panelist__category=Panelist.CATEGORY.music,
                )
            ),
            per_score=Avg(
                'points',
                filter=Q(
                    panelist__kind=Panelist.KIND.official,
                    panelist__category=Panelist.CATEGORY.performance,
                )
            ),
            sng_score=Avg(
                'points',
                filter=Q(
                    panelist__kind=Panelist.KIND.official,
                    panelist__category=Panelist.CATEGORY.singing,
                )
            ),
        )
        appearances = self.appearances.filter(
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
        self.scores_patched = scores
        self.appearances_patched = appearances

        # Panelists
        panelists = Panelist.objects.filter(
            kind=Panelist.KIND.official,
            round__session=self.session,
            round__num=1,
            category__gt=10,
        ).order_by('num')


        # Score Block
        initials = [x.person.initials for x in panelists]
        songs = Song.objects.filter(
            appearance__round__session=self.session,
            appearance__competitor__group=self.group,
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
            appearance__competitor__group=self.group,
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
            'competitor': self,
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
        subject = "[Barberscore] {0} {1} {2} Session Notification".format(
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
        context = {'competitor': self}
        # self.queue_notification('emails/competitor_csa.txt', context)
        return

    @fsm_log_by
    @transition(
        field=status,
        source='*',
        target=STATUS.scratched,
    )
    def scratch(self, *args, **kwargs):
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
