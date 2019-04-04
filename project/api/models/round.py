
# Standard Library
import logging
import random
import uuid
from io import BytesIO
import django_rq
# Third-Party
import pydf
import maya
from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel
from PyPDF2 import PdfFileMerger
from django.db.models import Sum, Max, Avg, StdDev, Count, Q
# Django
from django.apps import apps
from django.contrib.contenttypes.fields import GenericRelation
from django.core.files.base import ContentFile
from django.db import models
from django.db.models import Q, F, Window
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.text import slugify
from django.db.models.functions import DenseRank

from api.tasks import send_email
from api.fields import FileUploadPath

log = logging.getLogger(__name__)


class Round(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'built', 'Built',),
        (20, 'started', 'Started',),
        (25, 'finished', 'Finished',),
        (27, 'verified', 'Verified',),
        (30, 'published', 'Published',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
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
        default=0,
    )

    spots = models.IntegerField(
        null=True,
        blank=True,
    )

    date = models.DateField(
        null=True,
        blank=True,
    )

    footnotes = models.TextField(
        help_text="""
            Freeform text field; will print on OSS.""",
        blank=True,
    )

    oss = models.FileField(
        upload_to=FileUploadPath(),
        blank=True,
        default='',
    )
    legacy_oss = models.FileField(
        upload_to=FileUploadPath(),
        blank=True,
        default='',
    )
    sa = models.FileField(
        upload_to=FileUploadPath(),
        blank=True,
        default='',
    )

    # FKs
    session = models.ForeignKey(
        'Session',
        related_name='rounds',
        on_delete=models.CASCADE,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='rounds',
    )

    # Internals
    class Meta:
        unique_together = (
            ('session', 'kind',),
        )
        get_latest_by = [
            'num',
        ]

    class JSONAPIMeta:
        resource_name = "round"

    def __str__(self):
        return "{0} {1} {2}".format(
            self.session.convention.name,
            self.session.get_kind_display(),
            self.get_kind_display(),
        )

    # Methods
    def create_grids(self, onstage, duration, start, finish):
        venue = self.session.convention.venue
        timezone = venue.timezone.zone
        if not venue:
            return ValueError("Must have venue selected.")
        maya_object = maya.when(onstage, timezone=timezone)
        while start <= finish:
            onstage = maya_object.datetime()
            defaults = {
                'onstage': onstage,
                'venue': venue,
            }
            self.grids.update_or_create(
                num=start,
                defaults=defaults,
            )
            start += 1
            maya_object = maya_object.add(minutes=duration)
        return


    def get_oss(self):
        Group = apps.get_model('api.group')
        Panelist = apps.get_model('api.panelist')
        Song = apps.get_model('api.song')

        # Score Block
        group_ids = self.appearances.filter(
            is_private=False,
        ).exclude(
            # Don't include advancers on OSS
            draw__gt=0,
        ).exclude(
            # Don't include mic testers on OSS
            num__lte=0,
        ).values_list('group__id', flat=True)
        groups = Group.objects.filter(
            id__in=group_ids,
        ).prefetch_related(
            'appearances',
            'appearances__songs__scores',
            'appearances__songs__scores__panelist',
            'appearances__round__session',
        ).annotate(
            max_round=Max(
                'appearances__round__num',
                filter=Q(
                    appearances__num__gt=0,
                    appearances__round__session=self.session,
                ),
            ),
            tot_points=Sum(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__round__session=self.session,
                ),
            ),
            sng_points=Sum(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__songs__scores__panelist__category=Panelist.CATEGORY.singing,
                    appearances__round__session=self.session,
                ),
            ),
            per_points=Sum(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__songs__scores__panelist__category=Panelist.CATEGORY.performance,
                    appearances__round__session=self.session,
                ),
            ),
            tot_score=Avg(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__round__session=self.session,
                ),
            ),
            mus_score=Avg(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__songs__scores__panelist__category=Panelist.CATEGORY.music,
                    appearances__round__session=self.session,
                ),
            ),
            per_score=Avg(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__songs__scores__panelist__category=Panelist.CATEGORY.performance,
                    appearances__round__session=self.session,
                ),
            ),
            sng_score=Avg(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__songs__scores__panelist__category=Panelist.CATEGORY.singing,
                    appearances__round__session=self.session,
                ),
            ),
        ).order_by(
            '-tot_points',
            '-sng_points',
            '-per_points',
        )

        # Monkeypatching
        for group in groups:
            appearances = group.appearances.filter(
                num__gt=0,
                round__session=self.session,
            ).prefetch_related(
                'songs__scores',
                'songs__scores__panelist',
            ).order_by(
                'round__kind',
            ).annotate(
                tot_points=Sum(
                    'songs__scores__points',
                    filter=Q(
                        songs__scores__panelist__kind=Panelist.KIND.official,
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
            recent = appearances.get(round__num=self.num)
            contesting = recent.contenders.order_by(
                'outcome__num',
            ).values_list(
                'outcome__num',
                flat=True
            )
            group.contesting_patched = ", ".join([str(x) for x in contesting])
            group.pos_patched = recent.pos
            group.representing_patched = recent.representing
            group.participants_patched = recent.participants
            group.appearances_patched = appearances


        # Penalties Block
        array = Song.objects.select_related(
            'appearance__round',
            'appearance__group',
        ).filter(
            appearance__round=self,
            penalties__len__gt=0,
            appearance__is_private=False,
        ).distinct().values_list('penalties', flat=True)
        penalties_map = {
            10: "† Score(s) penalized due to violation of Article IX.A.1 of the BHS Contest Rules.",
            30: "‡ Score(s) penalized due to violation of Article IX.A.2 of the BHS Contest Rules.",
            40: "✠ Score(s) penalized due to violation of Article IX.A.3 of the BHS Contest Rules.",
            50: "✶ Score(s) penalized due to violation of Article X.B of the BHS Contest Rules.",
        }
        penalties = sorted(list(set(penalties_map[x] for l in array for x in l)))

        # Eval Only Block
        privates = self.appearances.prefetch_related(
            'group',
        ).filter(
            is_private=True,
        ).exclude(
            num=0,
        ).order_by(
            'group__name',
        ).values_list('group__name', flat=True)
        privates = list(privates)

        # Draw Block
        if self.kind != self.KIND.finals:
            # Get advancers
            advancers = self.appearances.filter(
                draw__gt=0,
            ).select_related(
                'group',
            ).order_by(
                'draw',
            ).values_list(
                'draw',
                'group__name',
            )
            advancers = list(advancers)
            try:
                mt = self.appearances.get(
                    draw=0,
                ).group.name
                advancers.append(('MT', mt))
            except self.appearances.model.DoesNotExist:
                pass
        else:
            advancers = None

        # Panelist Block
        panelists_raw = self.panelists.select_related(
            'person',
        ).filter(
            kind=Panelist.KIND.official,
            category__gte=Panelist.CATEGORY.ca,
        ).order_by(
            'num',
        )
        categories_map = {
            10: 'CA',
            30: 'MUS',
            40: 'PER',
            50: 'SNG',
        }
        panelists = []
        for key, value in categories_map.items():
            sections = panelists_raw.filter(
                category=key,
            ).select_related(
                'person',
            ).order_by(
                'num',
            )
            persons = [
                "{0} {1}".format(x.person.common_name, x.person.district) for x in sections
            ]
            names = ", ".join(persons)
            panelists.append((value, names))


        # Outcome Block
        items = self.outcomes.select_related(
            'award',
        ).order_by(
            'num',
        ).values_list(
            'num',
            'award__name',
            'name',
        )
        outcomes = []
        for item in items:
            outcomes.append(
                (
                    "{0} {1}".format(item[0], item[1]),
                    item[2],
                )
            )

        context = {
            'round': self,
            'groups': groups,
            'penalties': penalties,
            'privates': privates,
            'advancers': advancers,
            'panelists': panelists,
            'outcomes': outcomes,
        }
        rendered = render_to_string('reports/oss.html', context)

        if groups.count() > 8 and self.kind == self.KIND.finals:
            page_size = 'Legal'
        else:
            page_size = 'Letter'

        file = pydf.generate_pdf(
            rendered,
            page_size=page_size,
            orientation='Portrait',
            margin_top='5mm',
            margin_bottom='5mm',
        )
        content = ContentFile(file)
        return content

    def save_oss(self):
        content = self.get_oss()
        self.oss.save("oss", content)


    def get_sa(self):
        Panelist = apps.get_model('api.panelist')
        Song = apps.get_model('api.song')
        Group = apps.get_model('api.group')
        Person = apps.get_model('api.person')

        # Score Block
        group_ids = self.appearances.exclude(
            # Don't include advancers on SA
            draw__gt=0,
        ).values_list('group__id', flat=True)
        groups = Group.objects.prefetch_related(
            'appearances',
            'appearances__songs__scores',
            'appearances__songs__scores__panelist',
            'appearances__round__session',
        ).filter(
            id__in=group_ids,
        ).annotate(
            tot_points=Sum(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__round__session=self.session,
                ),
            ),
            mus_points=Sum(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__songs__scores__panelist__category=Panelist.CATEGORY.music,
                    appearances__round__session=self.session,
                ),
            ),
            per_points=Sum(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__songs__scores__panelist__category=Panelist.CATEGORY.performance,
                    appearances__round__session=self.session,
                ),
            ),
            sng_points=Sum(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__songs__scores__panelist__category=Panelist.CATEGORY.singing,
                    appearances__round__session=self.session,
                ),
            ),
            tot_score=Avg(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__round__session=self.session,
                ),
            ),
            mus_score=Avg(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__songs__scores__panelist__category=Panelist.CATEGORY.music,
                    appearances__round__session=self.session,
                ),
            ),
            per_score=Avg(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__songs__scores__panelist__category=Panelist.CATEGORY.performance,
                    appearances__round__session=self.session,
                ),
            ),
            sng_score=Avg(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__songs__scores__panelist__category=Panelist.CATEGORY.singing,
                    appearances__round__session=self.session,
                ),
            ),
            tot_rank=Window(
                expression=DenseRank(),
                order_by=F('tot_points').desc(),
            ),
            mus_rank=Window(
                expression=DenseRank(),
                order_by=F('mus_points').desc(),
            ),
            per_rank=Window(
                expression=DenseRank(),
                order_by=F('per_points').desc(),
            ),
            sng_rank=Window(
                expression=DenseRank(),
                order_by=F('sng_points').desc(),
            ),
        ).order_by(
            '-tot_points',
            '-sng_points',
            '-per_points',
        )

        persons = Person.objects.filter(
            panelists__round__session=self.session,
            panelists__category__gt=10,
            panelists__kind__in=[
                Panelist.KIND.official,
                Panelist.KIND.practice,
            ],
        ).order_by(
            'panelists__num',
        ).distinct()

        persons_music = persons.filter(
            panelists__category=Panelist.CATEGORY.music,
            panelists__round__session=self.session,
        ).order_by(
            'panelists__num',
        ).distinct()
        mus_persons = []
        for p in persons_music:
            practice = bool(p.panelists.get(round=self).kind == Panelist.KIND.practice)
            mus_persons.append((p.common_name, practice))
        persons_performance = persons.filter(
            panelists__category=Panelist.CATEGORY.performance,
            panelists__round__session=self.session,
        ).order_by(
            'panelists__num',
        ).distinct()
        per_persons = []
        for p in persons_performance:
            practice = bool(p.panelists.get(round=self).kind == Panelist.KIND.practice)
            per_persons.append((p.common_name, practice))
        persons_singing = persons.filter(
            panelists__category=Panelist.CATEGORY.singing,
            panelists__round__session=self.session,
        ).order_by(
            'panelists__num',
        ).distinct()
        sng_persons = []
        for p in persons_singing:
            practice = bool(p.panelists.get(round=self).kind == Panelist.KIND.practice)
            sng_persons.append((p.common_name, practice))

        # Monkeypatching
        for group in groups:
            # Populate the group block
            appearances = group.appearances.filter(
                round__session=self.session,
            ).prefetch_related(
                'songs__scores',
                'songs__scores__panelist',
            ).annotate(
                tot_points=Sum(
                    'songs__scores__points',
                    filter=Q(
                        songs__scores__panelist__kind=Panelist.KIND.official,
                    ),
                ),
                sng_points=Sum(
                    'songs__scores__points',
                    filter=Q(
                        songs__scores__panelist__kind=Panelist.KIND.official,
                        songs__scores__panelist__category=Panelist.CATEGORY.singing,
                    ),
                ),
                per_points=Sum(
                    'songs__scores__points',
                    filter=Q(
                        songs__scores__panelist__kind=Panelist.KIND.official,
                        songs__scores__panelist__category=Panelist.CATEGORY.performance,
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
            ).order_by(
                'round__kind',
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
                    tot_dev=StdDev(
                        'scores__points',
                        filter=Q(
                            scores__panelist__kind=Panelist.KIND.official,
                        ),
                    ),
                    mus_dev=StdDev(
                        'scores__points',
                        filter=Q(
                            scores__panelist__kind=Panelist.KIND.official,
                            scores__panelist__category=Panelist.CATEGORY.music,
                        ),
                    ),
                    per_dev=StdDev(
                        'scores__points',
                        filter=Q(
                            scores__panelist__kind=Panelist.KIND.official,
                            scores__panelist__category=Panelist.CATEGORY.performance,
                        ),
                    ),
                    sng_dev=StdDev(
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
                for song in songs:
                    music_scores = song.scores.filter(
                        panelist__category=Panelist.CATEGORY.music,
                    ).order_by(
                        'panelist__num',
                    )
                    mus_scores = []
                    for m in music_scores:
                        diff = abs(m.points - m.song.mus_score) > 5
                        mus_scores.append((m.points, diff))
                    song.mus_scores = mus_scores
                    performance_scores = song.scores.filter(
                        panelist__category=Panelist.CATEGORY.performance,
                    ).order_by(
                        'panelist__num',
                    )
                    per_scores = []
                    for m in performance_scores:
                        diff = abs(m.points - m.song.per_score) > 5
                        per_scores.append((m.points, diff))
                    song.per_scores = per_scores
                    singing_scores = song.scores.filter(
                        panelist__category=Panelist.CATEGORY.singing,
                    ).order_by(
                        'panelist__num',
                    )
                    sng_scores = []
                    for m in singing_scores:
                        diff = abs(m.points - m.song.sng_score) > 5
                        sng_scores.append((m.points, diff))
                    song.sng_scores = sng_scores
                appearance.songs_patched = songs
            group.appearances_patched = appearances

        # Build stats
        stats = Song.objects.select_related(
            'appearance__round',
        ).prefetch_related(
            'scores__panelist__kind',
        ).filter(
            appearance__round=self,
        ).annotate(
            tot_dev=StdDev(
                'scores__points',
                filter=Q(
                    scores__panelist__kind=Panelist.KIND.official,
                ),
            ),
            mus_dev=StdDev(
                'scores__points',
                filter=Q(
                    scores__panelist__kind=Panelist.KIND.official,
                    scores__panelist__category=Panelist.CATEGORY.music,
                ),
            ),
            per_dev=StdDev(
                'scores__points',
                filter=Q(
                    scores__panelist__kind=Panelist.KIND.official,
                    scores__panelist__category=Panelist.CATEGORY.performance,
                ),
            ),
            sng_dev=StdDev(
                'scores__points',
                filter=Q(
                    scores__panelist__kind=Panelist.KIND.official,
                    scores__panelist__category=Panelist.CATEGORY.singing,
                ),
            ),
        ).aggregate(
            tot=Avg('tot_dev'),
            mus=Avg('mus_dev'),
            per=Avg('per_dev'),
            sng=Avg('sng_dev'),
        )

        context = {
            'round': self,
            'groups': groups,
            'persons': persons,
            'persons_music': mus_persons,
            'persons_performance': per_persons,
            'persons_singing': sng_persons,
            'stats': stats,
        }
        rendered = render_to_string('reports/sa.html', context)
        file = pydf.generate_pdf(
            rendered,
            page_size='Letter',
            orientation='Landscape',
            margin_top='5mm',
            margin_bottom='5mm',
        )
        content = ContentFile(file)
        return content

    def save_sa(self):
        content = self.get_sa()
        self.sa.save('sa', content)


    def get_legacy_oss(self):
        # Contest = apps.get_model('api.contest')
        Panelist = apps.get_model('api.panelist')
        # Contestant = apps.get_model('api.contestant')
        appearances = self.appearances.filter(
            Q(draw=0) | Q(draw__isnull=True),
            is_private=False,
        ).exclude(
            num=0,
        ).select_related(
            'group',
        ).prefetch_related(
            'round',
            'songs',
            'songs__chart',
            'songs__scores',
            'songs__scores__panelist',
            'songs__scores__panelist__person',
        ).order_by(
            '-tot_points',
            '-sng_points',
            '-per_points',
            'group__name',
        )
        comps = appearances.values_list('group__id', flat=True)
        # MonkeyPatch running total
        for appearance in appearances:
            if not appearance.run_points:
                appearance.calc_total = appearance.tot_points
            else:
                try:
                    appearance.calc_total = appearance.run_points + appearance.tot_points
                except TypeError:
                    appearance.calc_total = None
        rounds = self.session.rounds.filter(kind__gt=self.kind)
        for rnd in rounds:
            aps = rnd.appearances.filter(
                id__in=comps,
            ).exclude(
                num=0,
            ).select_related(
                'group',
            ).prefetch_related(
                'round',
                'songs',
                'songs__chart',
                'songs__scores',
                'songs__scores__panelist',
                'songs__scores__panelist__person',
            ).order_by(
                '-tot_points',
                '-sng_points',
                '-per_points',
                'group__name',
            )
            for appearance in aps:
                if not appearance.run_points:
                    appearance.calc_total = appearance.tot_points
                else:
                    try:
                        appearance.calc_total = appearance.run_points + appearance.tot_points
                    except TypeError:
                        appearance.calc_total = None
            rnd.aps = aps
        # Eval Only
        privates = self.appearances.filter(
            is_private=True,
        ).select_related(
            'group',
        ).order_by(
            'group__name',
        ).values_list('group__name', flat=True)
        privates = list(privates)
        contests = self.session.contests.filter(
            num__isnull=False,
        ).select_related(
            'award',
            'group',
        ).distinct(
        ).order_by(
            'num',
        )
        # # MonkeyPatch qualifiers
        for contest in contests:
            if contest.award.level != contest.award.LEVEL.deferred:
                if contest.award.level == contest.award.LEVEL.qualifier:
                    threshold = contest.award.threshold
                    if threshold:
                        qualifiers = contest.contestants.filter(
                            status__gt=0,
                            entry__tot_score__gte=threshold,
                            entry__is_private=False,
                        ).distinct(
                        ).order_by(
                            'entry__group__name',
                        ).values_list(
                            'entry__group__name',
                            flat=True,
                        )
                        if qualifiers:
                            contest.detail = ", ".join(
                                qualifiers.values_list('entry__group__name', flat=True)
                            )
                        else:
                            contest.detail = "(No qualifiers)"
                else:
                    if contest.group:
                        contest.detail = str(contest.group.name)
                    else:
                        contest.detail = "(No recipient)"
            else:
                contest.detail = "(Result determined post-contest)"
        panelists = self.panelists.filter(
            kind=Panelist.KIND.official,
            category__gte=Panelist.CATEGORY.ca,
        ).distinct(
            'category',
            'person__last_name',
            'person__first_name',
        ).order_by(
            'category',
            'person__last_name',
            'person__first_name',
        )
        outcomes = self.outcomes.order_by('num')
        advancers = self.appearances.filter(
            draw__gt=0,
        ).order_by('draw')
        mt = self.appearances.filter(draw=0).first()
        adds_add = len(advancers)
        context = {
            'round': self,
            'appearances': appearances,
            'rounds': rounds,
            'privates': privates,
            'panelists': panelists,
            'contests': contests,
            'outcomes': outcomes,
            'advancers': advancers,
            'adds_add': adds_add,
            'mt': mt,
        }
        rendered = render_to_string('reports/legacy_oss.html', context)
        file = pydf.generate_pdf(
            rendered,
            page_size='Letter',
            orientation='Portrait',
            margin_top='5mm',
            margin_bottom='5mm',
        )
        content = ContentFile(file)
        return content

    def save_legacy_oss(self):
        content = self.get_legacy_oss()
        self.legacy_oss.save('legacy_oss', content)


    def get_titles(self):
        Song = apps.get_model('api.song')
        appearances = self.appearances.filter(
            draw__gt=0,
        ).order_by(
            'draw',
        )
        for appearance in appearances:
            songs = Song.objects.filter(
                appearance__group=appearance.group,
                appearance__round__session=self.session,
            ).distinct().order_by(
                'appearance__round__num',
                'num',
            )
            titles = []
            for song in songs:
                try:
                    title = song.chart.title
                except AttributeError:
                    title = "Unknown (Not in Repertory)"
                row = "{0} Song {1}: {2}".format(
                    song.appearance.round.get_kind_display(),
                    song.num,
                    title,
                )
                titles.append(row)
            appearance.titles_patched = titles

        context = {
            'appearances': appearances,
            'round': self,
        }
        rendered = render_to_string('reports/titles.html', context)
        file = pydf.generate_pdf(
            rendered,
            page_size='Letter',
            orientation='Portrait',
            margin_top='5mm',
            margin_bottom='5mm',
        )
        content = ContentFile(file)
        return content

    def get_announcements(self):
        Panelist = apps.get_model('api.panelist')
        Group = apps.get_model('api.group')
        Appearance = apps.get_model('api.appearance')
        appearances = self.appearances.filter(
            draw__gt=0,
        ).order_by(
            'draw',
        )
        group_ids = appearances.values_list('group__id', flat=True)
        mt = self.appearances.filter(
            draw=0,
        ).first()
        outcomes = self.outcomes.order_by(
            '-num',
        )
        if self.kind == self.KIND.finals:
            groups = Group.objects.filter(
                appearances__round__session=self.session,
            ).exclude(
                status__in=[
                    Appearance.STATUS.disqualified,
                    Appearance.STATUS.scratched,
                ],
            ).prefetch_related(
                'appearances__songs__scores',
                'appearances__songs__scores__panelist',
                'appearances__round__session',
            ).annotate(
                tot_points=Sum(
                    'appearances__songs__scores__points',
                    filter=Q(
                        appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                        appearances__round__session=self.session,
                    ),
                ),
                tot_score=Avg(
                    'appearances__songs__scores__points',
                    filter=Q(
                        appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                        appearances__round__session=self.session,
                    ),
                ),
            ).order_by(
                '-tot_points',
            )[:5]
        else:
            groups = None
        if groups:
            groups = reversed(groups)
        pos = self.appearances.aggregate(sum=Sum('pos'))['sum']
        context = {
            'round': self,
            'appearances': appearances,
            'mt': mt,
            'outcomes': outcomes,
            'groups': groups,
            'pos': pos,
        }
        rendered = render_to_string('reports/announcements.html', context)
        file = pydf.generate_pdf(
            rendered,
            page_size='Letter',
            orientation='Portrait',
            margin_top='5mm',
            margin_bottom='5mm',
        )
        content = ContentFile(file)
        return content


    def get_ca_emails(self):
        Panelist = apps.get_model('api.panelist')
        cas = self.panelists.filter(
            status=Panelist.STATUS.active,
            category=Panelist.CATEGORY.ca,
            person__email__isnull=False,
        )
        result = ["{0} <{1}>".format(
            ca.person.common_name,
            ca.person.email,
        ) for ca in cas]
        return result

    def queue_notification(self, template, context=None):
        panelists = self.panelists.filter(
            person__email__isnull=False,
        )
        if not panelists:
            raise RuntimeError("No panelists for {0}".format(self))
        to = ["{0} <{1}>".format(panelist.person.common_name, panelist.person.email) for panelist in panelists]
        body = render_to_string(template, context)
        subject = "[Barberscore] {0} {1} {2} SA".format(
            self.session.convention.name,
            self.session.get_kind_display(),
            self.get_kind_display(),
        )
        # Ensure uniqueness
        queue = django_rq.get_queue('high')
        result = queue.enqueue(
            send_email,
            subject=subject,
            body=body,
            to=to,
        )
        return result

    def mock(self):
        Appearance = apps.get_model('api.appearance')
        if self.status != self.STATUS.started:
            raise RuntimeError("Round not Started")
        appearances = self.appearances.exclude(
            status=Appearance.STATUS.verified,
        )
        for appearance in appearances:
            appearance.mock()
            appearance.save()
        return


    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.is_convention_manager,
            # request.user.is_session_manager,
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
                    category=self.session.convention.assignments.model.CATEGORY.ca,
                ),
                self.status != self.STATUS.published,
            ]),
        ])

    # Round Conditions
    def can_build(self):
        return True

    def can_finish(self):
        Appearance = apps.get_model('api.appearance')
        return all([
            not self.appearances.exclude(status=Appearance.STATUS.verified),
        ])

    def can_verify(self):
        return True
        # return all([
        #     not self.outcomes.filter(
        #         name='MUST ENTER WINNER MANUALLY',
        #     ),
        # ])

    def can_publish(self):
        return True

    # Round Transitions
    @fsm_log_by
    @transition(
        field=status,
        source='*',
        target=STATUS.new,
    )
    def reset(self, *args, **kwargs):
        panelists = self.panelists.all()
        appearances = self.appearances.all()
        outcomes = self.outcomes.all()
        panelists.delete()
        outcomes.delete()
        appearances.delete()
        return

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS.new,
        target=STATUS.built,
        conditions=[can_build],
    )
    def build(self, *args, **kwargs):
        # Reset for indempodence
        self.reset()

        # Instantiate prior round
        if self.num == 1:
            prior_round = None
        else:
            prior_round = self.session.rounds.get(num=self.num - 1)

        # Create Panelsists
        Assignment = apps.get_model('api.assignment')
        cas = self.session.convention.assignments.filter(
            status=Assignment.STATUS.active,
            kind__in=[
                Assignment.KIND.official,
                Assignment.KIND.practice,
            ],
            category=Assignment.CATEGORY.ca,
        ).order_by(
            'kind',
            'category',
            'person__last_name',
            'person__nick_name',
            'person__first_name',
        )
        for ca in cas:
            self.panelists.create(
                kind=ca.kind,
                category=ca.category,
                person=ca.person,
            )
        officials = self.session.convention.assignments.filter(
            status=Assignment.STATUS.active,
            kind=Assignment.KIND.official,
            category__gt=Assignment.CATEGORY.ca,
        ).order_by(
            'kind',
            'category',
            'person__last_name',
            'person__nick_name',
            'person__first_name',
        )
        i = 0
        for official in officials:
            i += 1
            self.panelists.create(
                num=i,
                kind=official.kind,
                category=official.category,
                person=official.person,
            )

        practices = self.session.convention.assignments.filter(
            status=Assignment.STATUS.active,
            kind=Assignment.KIND.practice,
            category__gt=Assignment.CATEGORY.ca,
        ).order_by(
            'kind',
            'category',
            'person__last_name',
            'person__nick_name',
            'person__first_name',
        )
        p = 50
        for practice in practices:
            p += 1
            self.panelists.create(
                num=p,
                kind=practice.kind,
                category=practice.category,
                person=practice.person,
            )

        # Create Outcomes
        # Create from contests if no prior round
        if not prior_round:
            contests = self.session.contests.select_related(
                'award',
            ).filter(
                status__gt=0,
            ).annotate(
                cnt=Count(
                    'contestants',
                    filter=Q(
                        contestants__status=10,
                    )
                ),
            ).exclude(
                cnt=0,
            ).order_by(
                'award__tree_sort',
            )
            i = 0
            for contest in contests:
                i += 1
                self.outcomes.create(
                    num=i,
                    award=contest.award,
                )
        else:
            prior_outcomes = prior_round.outcomes.exclude(
                award__is_single=True,
            )
            for prior_outcome in prior_outcomes:
                new_outcome = self.outcomes.create(
                    num=prior_outcome.num,
                    award=prior_outcome.award,
                )

        # Create Appearances
        Appearance = apps.get_model('api.appearance')
        Entry = apps.get_model('api.entry')
        # If the first round, populate from entries
        if not prior_round:
            entries = self.session.entries.filter(
                status=Entry.STATUS.approved,
            )
            z = 0
            for entry in entries:
                # TODO - MT hack
                if entry.is_mt:
                    entry.draw = z
                    z -= 1
                # Pull active contestants
                contestants = entry.contestants.filter(
                    status__gt=0,
                )
                # Set is_single=True if they are only in single-round contests
                is_single = not bool(
                    contestants.filter(
                        contest__award__is_single=False,
                    )
                )
                # Create and start group
                appearance = self.appearances.create(
                    entry=entry,
                    group=entry.group,
                    num=entry.draw,
                    is_single=is_single,
                    is_private=entry.is_private,
                    participants=entry.participants,
                    representing=entry.representing,
                )
                # Create contenders
                awards = contestants.values_list('contest__award', flat=True)
                outcomes = self.outcomes.filter(award__in=awards)
                for outcome in outcomes:
                    outcome.contenders.create(
                        appearance=appearance,
                    )
        # Otherwise, populate from prior round
        else:
            new_outcomes = self.outcomes.all()
            prior_appearances = prior_round.appearances.filter(
                status=Appearance.STATUS.advanced,
            )
            for prior_appearance in prior_appearances:
                appearance = self.appearances.create(
                    entry=prior_appearance.entry,
                    group=prior_appearance.group,
                    num=prior_appearance.draw,
                    is_single=prior_appearance.is_single,
                    is_private=prior_appearance.is_private,
                    participants=prior_appearance.participants,
                    representing=prior_appearance.representing,
                )
                for new_outcome in new_outcomes:
                    curry = bool(
                        prior_appearance.contenders.filter(outcome__award=new_outcome.award)
                    )
                    if curry:
                        new_outcome.contenders.create(
                            appearance=appearance,
                        )

            mts = prior_round.appearances.filter(
                draw__lte=0,
            )
            for mt in mts:
                appearance = self.appearances.create(
                    entry=mt.entry,
                    group=mt.group,
                    num=mt.draw,
                    is_single=mt.is_single,
                    is_private=mt.is_private,
                    participants=mt.participants,
                    representing=mt.representing,
                )


    @fsm_log_by
    @transition(field=status, source=[STATUS.built], target=STATUS.started)
    def start(self, *args, **kwargs):
        # Build the appearances
        appearances = self.appearances.all()
        for appearance in appearances:
            appearance.build()
            appearance.save()
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.started], target=STATUS.finished, conditions=[can_finish,])
    def finish(self, *args, **kwargs):
        Panelist = apps.get_model('api.panelist')
        # Run outcomes
        outcomes = self.outcomes.all()
        for outcome in outcomes:
            outcome.name = outcome.get_name()
            outcome.save()

        # If there is no next round simply return
        if self.kind == self.KIND.finals:
            return

        # Otherwise, get spots available
        spots = self.spots

        # Get all multi appearances and annotate average.
        multis = self.appearances.filter(
            is_single=False,
        ).annotate(
            avg=Avg(
                'songs__scores__points',
                filter=Q(
                    songs__scores__panelist__kind=Panelist.KIND.official,
                )
            ),
            tot_points=Sum(
                'songs__scores__points',
                filter=Q(
                    songs__scores__panelist__kind=Panelist.KIND.official,
                )
            ),
            sng_points=Sum(
                'songs__scores__points',
                filter=Q(
                    songs__scores__panelist__kind=Panelist.KIND.official,
                    songs__scores__panelist__category=Panelist.CATEGORY.singing,
                )
            ),
            per_points=Sum(
                'songs__scores__points',
                filter=Q(
                    songs__scores__panelist__kind=Panelist.KIND.official,
                    songs__scores__panelist__category=Panelist.CATEGORY.performance,
                )
            ),
        )
        # If spots are constricted, find those who advance
        if spots:
            # All those above 73.0 advance automatically, regardless of spots available
            automatics = multis.filter(
                avg__gte=73.0,
            )
            # generate list of the advancers, as appearance IDs
            advancers = [x.id for x in automatics]
            # Figure out remaining spots
            cnt = automatics.count()
            diff = spots - cnt
            # If there are additionl remaining spots, add them up to available
            if diff > 0:
                remains = multis.exclude(
                    id__in=advancers,
                ).order_by(
                    '-tot_points',
                    '-sng_points',
                    '-per_points',
                )
                adds = remains[:diff]
                try:
                    mt = remains[diff:diff+1]
                except IndexError:
                    mt = None
                for a in adds:
                    advancers.append(a.id)
        # Otherwise, advance all
        else:
            advancers = [a.id for a in multis]

        # Reset draw
        self.appearances.update(draw=None)

        # Randomize the advancers and set the initial draw
        appearances = self.appearances.filter(
            id__in=advancers,
        ).order_by('?')
        i = 1
        for appearance in appearances:
            appearance.draw = i
            appearance.save()
            i += 1
        # create Mic Tester at draw 0
        if mt:
            mt = self.appearances.get(id=mt)
            mt.draw = 0
            mt.save()
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.finished], target=STATUS.verified, conditions=[can_verify])
    def verify(self, *args, **kwargs):
        completed_appearances = self.appearances.exclude(
            draw__gt=0,
        )
        for appearance in completed_appearances:
            appearance.complete()
            appearance.save()
        advancing_appearances = self.appearances.filter(
            draw__gt=0,
        )
        for appearance in advancing_appearances:
            appearance.advance()
            appearance.save()
        # panelists = self.panelists.all()
        # for panelist in panelists:
        #     panelist.save_psa()
        # self.save_oss()
        # self.save_sa()
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.verified], target=STATUS.published, conditions=[can_publish])
    def publish(self, *args, **kwargs):
        # Publish results!
        return
