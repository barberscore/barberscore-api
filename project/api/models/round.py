
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
from django.db.models import Sum, Max, Avg, StdDev
# Django
from django.apps import apps
from django.contrib.contenttypes.fields import GenericRelation
from django.core.files.base import ContentFile
from django.db import models
from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.text import slugify

from api.tasks import send_email

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
        (27, 'verified', 'Verified',),
        (30, 'finished', 'Finished',),
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
        max_length=255,
        null=True,
        blank=True,
    )
    old_oss = models.FileField(
        max_length=255,
        null=True,
        blank=True,
    )
    sa = models.FileField(
        max_length=255,
        null=True,
        blank=True,
    )
    legacy_oss = models.FileField(
        max_length=255,
        null=True,
        blank=True,
    )

    legacy_sa = models.FileField(
        max_length=255,
        null=True,
        blank=True,
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
    def rank(self):
        # Get raw queryset
        appearances = self.appearances.filter(
            is_private=False,
            # competitor__status__gt=0,
        ).distinct()
        # Ranking algo
        tot_appearances = appearances.order_by(
            '-tot_points',
            '-sng_points',
            '-per_points',
            'group__name',
        )
        for index, appearance in enumerate(tot_appearances):
            appearance.tot_rank = index + 1
            appearance.save()
        # SNG only
        sng_appearances = appearances.order_by(
            '-sng_points',
            'group__name',
        )
        for index, appearance in enumerate(sng_appearances):
            appearance.sng_rank = index + 1
            appearance.save()
        # MUS only
        mus_appearances = appearances.order_by(
            '-mus_points',
            'group__name',
        )
        for index, appearance in enumerate(mus_appearances):
            appearance.mus_rank = index + 1
            appearance.save()
        # PER only
        per_appearances = appearances.order_by(
            '-per_points',
            'group__name',
        )
        for index, appearance in enumerate(per_appearances):
            appearance.per_rank = index + 1
            appearance.save()
        return

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
        Appearance = apps.get_model('api.appearance')
        Panelist = apps.get_model('api.panelist')
        Song = apps.get_model('api.song')
        Group = apps.get_model('api.group')

        # Score Block
        group_ids = self.appearances.filter(
            is_private=False,
        ).exclude(
            draw__gt=0,
        ).exclude(
            num=0,
        ).values_list('group', flat=True)
        groups = Group.objects.filter(
            id__in=group_ids,
        ).prefetch_related(
            'appearances__songs__scores',
            'appearances__songs__scores__panelist',
            'appearances__round__session',
            'appearances__round',
        ).annotate(
            max=Max(
                'appearances__round__num',
                filter=Q(
                    appearances__round__session=self.session,
                    appearances__num__gt=0,
                ),
            ),
            tot_points=Sum(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__round__session=self.session,
                    appearances__round__num__lte=self.num,
                    appearances__num__gt=0,
                ),
            ),
            sng_points=Sum(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__songs__scores__panelist__category=Panelist.CATEGORY.singing,
                    appearances__round__session=self.session,
                    appearances__round__num__lte=self.num,
                    appearances__num__gt=0,
                ),
            ),
            per_points=Sum(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__songs__scores__panelist__category=Panelist.CATEGORY.performance,
                    appearances__round__session=self.session,
                    appearances__round__num__lte=self.num,
                    appearances__num__gt=0,
                ),
            ),
            tot_score=Avg(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__round__session=self.session,
                    appearances__round__num__lte=self.num,
                    appearances__num__gt=0,
                ),
            ),
            mus_score=Avg(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__songs__scores__panelist__category=Panelist.CATEGORY.music,
                    appearances__round__session=self.session,
                    appearances__round__num__lte=self.num,
                    appearances__num__gt=0,
                ),
            ),
            per_score=Avg(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__songs__scores__panelist__category=Panelist.CATEGORY.performance,
                    appearances__round__session=self.session,
                    appearances__round__num__lte=self.num,
                    appearances__num__gt=0,
                ),
            ),
            sng_score=Avg(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__songs__scores__panelist__category=Panelist.CATEGORY.singing,
                    appearances__round__session=self.session,
                    appearances__round__num__lte=self.num,
                    appearances__num__gt=0,
                ),
            ),
        ).order_by(
            '-tot_points',
            '-sng_points',
            '-per_points',
        )

        # Monkeypatching
        for group in groups:
            # Populate the group block
            source = self.appearances.get(
                group=group,
            )
            group.contesting = source.contesting
            group.representing = source.representing
            group.participants = source.participants
            appearances = group.appearances.filter(
                group=group,
                round__session=self.session,
                num__gt=0,
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
            group.appearances_patched = appearances


        # Penalties Block
        array = Song.objects.filter(
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
        privates = self.appearances.filter(
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
            mt = self.appearances.get(
                draw=0,
            ).group.name
            advancers.append(('MT', mt))
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
            persons = [x.person.common_name for x in sections]
            names = ", ".join(persons)
            panelists.append((value, names))


        # Outcome Block
        items = self.outcomes.order_by(
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
        rendered = render_to_string('round/oss.html', context)
        file = pydf.generate_pdf(
            rendered,
            page_size='Letter',
            # page_size='Legal',
            orientation='Portrait',
            margin_top='5mm',
            margin_bottom='5mm',
        )
        content = ContentFile(file)
        return content

    def get_old_oss(self):
        # Competitor = apps.get_model('api.competitor')
        # Contest = apps.get_model('api.contest')
        Panelist = apps.get_model('api.panelist')
        # Contestant = apps.get_model('api.contestant')
        appearances = self.appearances.filter(
            Q(draw=0) | Q(draw__isnull=True),
            competitor__is_private=False,
        ).exclude(
            num=0,
        ).select_related(
            'competitor__group',
        ).prefetch_related(
            'round',
            'songs',
            'songs__chart',
            'songs__scores',
            'songs__scores__panelist',
            'songs__scores__panelist__person',
            'contenders',
            'contenders__outcome',
        ).order_by(
            '-competitor__tot_points',
            '-competitor__sng_points',
            '-competitor__per_points',
            'competitor__group__name',
        )
        comps = appearances.values_list('competitor__id', flat=True)
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
                competitor__id__in=comps,
            ).exclude(
                num=0,
            ).select_related(
                'competitor__group',
            ).prefetch_related(
                'round',
                'songs',
                'songs__chart',
                'songs__scores',
                'songs__scores__panelist',
                'songs__scores__panelist__person',
                'contenders',
                'contenders__outcome',
            ).order_by(
                '-tot_points',
                '-sng_points',
                '-per_points',
                'competitor__group__name',
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
            competitor__is_private=True,
        ).select_related(
            'competitor__group',
        ).order_by(
            'competitor__group__name',
        ).values_list('competitor__group__name', flat=True)
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
                            entry__competitor__tot_score__gte=threshold,
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
        rendered = render_to_string('round/old_oss.html', context)
        file = pydf.generate_pdf(
            rendered,
            page_size='Letter',
            orientation='Portrait',
            margin_top='5mm',
            margin_bottom='5mm',
        )
        content = ContentFile(file)
        return content

    def save_old_oss(self):
        content = self.get_old_oss()
        self.refresh_from_db()
        self.old_oss.save(
            "{0}-old-oss".format(
                slugify(self),
            ),
            content,
        )

    def get_sa(self):

        Panelist = apps.get_model('api.panelist')
        Score = apps.get_model('api.score')
        Group = apps.get_model('api.group')
        Person = apps.get_model('api.person')

        # Score Block
        group_ids = self.appearances.filter(
            is_private=False,
        ).exclude(
            draw__gt=0,
        ).exclude(
            num=0,
        ).values_list('group', flat=True)
        groups = Group.objects.filter(
            id__in=group_ids,
        ).prefetch_related(
            'appearances__songs__scores',
            'appearances__songs__scores__panelist',
            'appearances__round__session',
            'appearances__round',
        ).annotate(
            max=Max(
                'appearances__round__num',
                filter=Q(
                    appearances__round__session=self.session,
                    appearances__num__gt=0,
                ),
            ),
            tot_points=Sum(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__round__session=self.session,
                    appearances__round__num__lte=self.num,
                    appearances__num__gt=0,
                ),
            ),
            sng_points=Sum(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__songs__scores__panelist__category=Panelist.CATEGORY.singing,
                    appearances__round__session=self.session,
                    appearances__round__num__lte=self.num,
                    appearances__num__gt=0,
                ),
            ),
            per_points=Sum(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__songs__scores__panelist__category=Panelist.CATEGORY.performance,
                    appearances__round__session=self.session,
                    appearances__round__num__lte=self.num,
                    appearances__num__gt=0,
                ),
            ),
            tot_score=Avg(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__round__session=self.session,
                    appearances__round__num__lte=self.num,
                    appearances__num__gt=0,
                ),
            ),
            mus_score=Avg(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__songs__scores__panelist__category=Panelist.CATEGORY.music,
                    appearances__round__session=self.session,
                    appearances__round__num__lte=self.num,
                    appearances__num__gt=0,
                ),
            ),
            per_score=Avg(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__songs__scores__panelist__category=Panelist.CATEGORY.performance,
                    appearances__round__session=self.session,
                    appearances__round__num__lte=self.num,
                    appearances__num__gt=0,
                ),
            ),
            sng_score=Avg(
                'appearances__songs__scores__points',
                filter=Q(
                    appearances__songs__scores__panelist__kind=Panelist.KIND.official,
                    appearances__songs__scores__panelist__category=Panelist.CATEGORY.singing,
                    appearances__round__session=self.session,
                    appearances__round__num__lte=self.num,
                    appearances__num__gt=0,
                ),
            ),
        ).order_by(
            '-tot_points',
            '-sng_points',
            '-per_points',
        )

        # Pre-patching
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
        persons_performance = persons.filter(
            panelists__category=Panelist.CATEGORY.performance,
            panelists__round__session=self.session,
        ).order_by(
            'panelists__num',
        ).distinct()
        persons_singing = persons.filter(
            panelists__category=Panelist.CATEGORY.singing,
            panelists__round__session=self.session,
        ).order_by(
            'panelists__num',
        ).distinct()

        # Monkeypatching
        for group in groups:
            # Populate the group block
            source = self.appearances.get(
                group=group,
            )
            group.contesting = source.contesting
            group.representing = source.representing
            group.participants = source.participants
            full = []
            for person in persons_music:
                item = []
                scores = Score.objects.filter(
                    panelist__person=person,
                    panelist__round__session=self.session,
                    panelist__category=Panelist.CATEGORY.music,
                    song__appearance__group=group,
                ).order_by(
                    'panelist__round__kind',
                    'song__num',
                ).distinct()
                for score in scores:
                    item.append(score)
                full.append(item)
            group.music_patched = full
            full = []
            for person in persons_performance:
                item = []
                scores = Score.objects.filter(
                    panelist__person=person,
                    panelist__round__session=self.session,
                    panelist__category=Panelist.CATEGORY.performance,
                    song__appearance__group=group,
                ).order_by(
                    'panelist__round__kind',
                    'song__num',
                )
                for score in scores:
                    item.append(score)
                full.append(item)
            group.performance_patched = full
            full = []
            for person in persons_singing:
                item = []
                scores = Score.objects.filter(
                    panelist__person=person,
                    panelist__round__session=self.session,
                    panelist__category=Panelist.CATEGORY.singing,
                    song__appearance__group=group,
                ).order_by(
                    'panelist__round__kind',
                    'song__num',
                )
                for score in scores:
                    item.append(score)
                full.append(item)
            group.singing_patched = full
            appearances = group.appearances.filter(
                group=group,
                round__session=self.session,
                num__gt=0,
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
                appearance.songs_patched = songs
                appearance.round_patched = appearance.round.get_kind_display().replace('Semi-Finals', 'Semis ')
            group.appearances_patched = appearances
        # Panelist = apps.get_model('api.panelist')
        # panelists = self.panelists.filter(
        #     kind__in=[
        #         Panelist.KIND.official,
        #         Panelist.KIND.practice,
        #     ],
        #     category__gt=Panelist.CATEGORY.ca,
        # ).select_related(
        #     'person',
        # ).distinct(
        # ).order_by(
        #     'category',
        #     'kind',
        #     'person__last_name',
        #     'person__nick_name',
        #     'person__first_name',
        # )
        # mo_count = panelists.filter(
        #     category=Panelist.CATEGORY.music,
        #     kind=Panelist.KIND.official,
        # ).count()
        # po_count = panelists.filter(
        #     category=Panelist.CATEGORY.performance,
        #     kind=Panelist.KIND.official,
        # ).count()
        # so_count = panelists.filter(
        #     category=Panelist.CATEGORY.singing,
        #     kind=Panelist.KIND.official,
        # ).count()
        # mp_count = panelists.filter(
        #     category=Panelist.CATEGORY.music,
        #     kind=Panelist.KIND.practice,
        # ).count()
        # pp_count = panelists.filter(
        #     category=Panelist.CATEGORY.performance,
        #     kind=Panelist.KIND.practice,
        # ).count()
        # sp_count = panelists.filter(
        #     category=Panelist.CATEGORY.singing,
        #     kind=Panelist.KIND.practice,
        # ).count()
        # competitors = self.session.competitors.filter(
        #     Q(appearances__draw=0) | Q(appearances__draw__isnull=True),
        #     appearances__round=self,
        # ).select_related(
        #     'group',
        # ).prefetch_related(
        #     'appearances',
        #     'appearances__songs',
        #     'appearances__songs__scores',
        #     'appearances__songs__scores__panelist',
        #     'appearances__songs__scores__panelist__person',
        # ).order_by(
        #     '-tot_points',
        #     '-sng_points',
        #     '-mus_points',
        #     '-per_points',
        #     'group__name',
        # )
        context = {
            'round': self,
            'groups': groups,
            'persons': persons,
            'persons_music': persons_music,
            'persons_performance': persons_performance,
            'persons_singing': persons_singing,
        }
        rendered = render_to_string('sa.html', context)
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
        self.refresh_from_db()
        self.sa.save(
            "{0}-sa".format(
                slugify(self),
            ),
            content,
        )

    def get_csa(self):
        competitors = self.session.competitors.filter(
            Q(appearances__draw=0) | Q(appearances__draw__isnull=True),
            appearances__round=self,
        ).order_by(
            'group__name',
        )
        merger = PdfFileMerger()
        for competitor in competitors:
            try:
                file = ContentFile(competitor.csa.read())
            except ValueError:
                file = competitor.get_csa()
            merger.append(file, import_bookmarks=False)
        stream = BytesIO()
        merger.write(stream)
        data = stream.getvalue()
        content = ContentFile(data)
        return content

    def save_oss(self):
        content = self.get_oss()
        self.refresh_from_db()
        self.oss.save(
            "{0}-oss".format(
                slugify(self),
            ),
            content,
        )

    def get_sung(self):
        Song = apps.get_model('api.song')
        appearances = self.appearances.filter(
            draw__gt=0,
        ).order_by(
            'draw',
        )
        for appearance in appearances:
            songs = Song.objects.filter(
                appearance__competitor=appearance.competitor,
            ).distinct().order_by(
                'appearance__round__num',
                'num',
            )
            sungs = []
            for song in songs:
                try:
                    title = song.chart.nomen
                except AttributeError:
                    title = "Unknown (Not in Repertory)"
                row = "{0} Song {1}: {2}".format(
                    song.appearance.round.get_kind_display(),
                    song.num,
                    title,
                )
                sungs.append(row)
            appearance.sungs = sungs

        context = {
            'appearances': appearances,
            'round': self,
        }
        rendered = render_to_string('sung.html', context)
        file = pydf.generate_pdf(
            rendered,
            page_size='Letter',
            orientation='Portrait',
            margin_top='5mm',
            margin_bottom='5mm',
        )
        content = ContentFile(file)
        return content

    def queue_sa(self):
        panelists = self.panelists.filter(
            person__email__isnull=False,
        )
        if not panelists:
            raise RuntimeError("No panelists for {0}".format(self))
        to = ["{0} <{1}>".format(panelist.person.common_name, panelist.person.email) for panelist in panelists]
        context = {'round': self}
        body = render_to_string('sa.txt', context)
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
                self.status != self.STATUS.finished,
            ]),
        ])

    # Round Conditions
    def can_build(self):
        return True

    def can_verify(self):
        Appearance = apps.get_model('api.appearance')
        return all([
            not self.appearances.exclude(status=Appearance.STATUS.verified),
        ])

    def can_finish(self):
        return all([
            not self.outcomes.filter(
                name='MUST ENTER WINNER MANUALLY',
            ),
        ])

    # Round Transitions
    @fsm_log_by
    @transition(
        field=status,
        source='*',
        target=STATUS.new,
    )
    def reset(self, *args, **kwargs):
        Grid = apps.get_model('api.grid')
        panelists = self.panelists.all()
        appearances = self.appearances.all()
        outcomes = self.outcomes.all()
        competitors = self.session.competitors.filter(
            status=self.session.competitors.model.STATUS.started,
        )
        grids = Grid.objects.filter(
            appearance__in=appearances,
        )
        grids.update(appearance=None)
        competitors.update(
            mus_points=None,
            mus_rank=None,
            mus_score=None,
            per_points=None,
            per_rank=None,
            per_score=None,
            sng_points=None,
            sng_rank=None,
            sng_score=None,
            tot_points=None,
            tot_rank=None,
            tot_score=None,
        )
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
        Assignment = apps.get_model('api.assignment')
        # Create the panel (CAs and Judges)
        assignments = self.session.convention.assignments.filter(
            status=Assignment.STATUS.active,
            kind__in=[
                Assignment.KIND.official,
                Assignment.KIND.practice,
            ],
            category__gte=Assignment.CATEGORY.ca,
        ).order_by(
            'kind',
            'category',
            'person__last_name',
            'person__nick_name',
            'person__first_name',
        )
        for assignment in assignments:
            self.panelists.create(
                kind=assignment.kind,
                category=assignment.category,
                person=assignment.person,
            )
        # Create the Outcomes
        contests = self.session.contests.select_related(
            'award',
        ).filter(
            num__isnull=False,
            award__num_rounds=self.num,
        )
        for contest in contests:
            self.outcomes.create(
                num=contest.num,
                award=contest.award,
                level=contest.award.level,
                num_rounds=contest.award.num_rounds,
                threshold=contest.award.threshold,
                advance=contest.award.advance,
                minimum=contest.award.minimum,
                spots=contest.award.spots,
            )
        # Create the appearances
        Grid = apps.get_model('api.grid')
        # Determine prior rounds
        if self.num == 1:
            prior_round = None
        else:
            prior_round = self.session.rounds.get(num=self.num - 1)
        # If the first round, populate from competitors
        if not prior_round:
            competitors = self.session.competitors.select_related(
                'group',
            ).filter(
                draw__isnull=False,
            )
        # Otherwise, populate from prior round
        else:
            groups = prior_round.appearances.select_related(
                'group',
            ).filter(
                draw__isnull=False,
            ).values_list(
                'group',
                flat=True,
            )
            competitors = self.session.competitors.select_related(
                'group',
            ).filter(
                is_multi=True,
                group__in=groups,
            )
        for competitor in competitors:
            if not prior_round:
                draw = competitor.draw
                run_points = None
                run_score = None
            else:
                prior_appearance = prior_round.appearances.get(
                    group=competitor.group,
                )
                draw = prior_appearance.draw
                run_points = prior_appearance.run_points
                run_score = prior_appearance.run_score
            outcomes = self.outcomes.filter(
                num__in=competitor.contesting,
            )
            contesting = [x.num for x in outcomes]
            appearance = self.appearances.create(
                group=competitor.group,
                num=draw,
                is_multi=competitor.is_multi,
                is_private=competitor.is_private,
                participants=competitor.participants,
                representing=competitor.representing,
                run_points=run_points,
                run_score=run_score,
                contesting=contesting,
            )
        # Create the grids
        defaults = {
            'appearance': appearance,
        }
        Grid.objects.update_or_create(
            round=self,
            num=draw,
            defaults=defaults,
        )
        return


    @fsm_log_by
    @transition(field=status, source=[STATUS.built], target=STATUS.started)
    def start(self, *args, **kwargs):
        Panelist = apps.get_model('api.panelist')
        # Number the panelists
        officials = self.panelists.filter(
            kind=Panelist.KIND.official,
            category__gt=Panelist.CATEGORY.ca,
        ).order_by(
            'category',
            'person__last_name',
            'person__nick_name',
            'person__first_name',
        )
        i = 0
        for official in officials:
            i += 1
            official.num = i
            official.save()
        practices = self.panelists.filter(
            kind=Panelist.KIND.practice,
            category__gt=Panelist.CATEGORY.ca,
        ).order_by(
            'category',
            'person__last_name',
            'person__nick_name',
            'person__first_name',
        )
        i = 50
        for practice in practices:
            i += 1
            practice.num = i
            practice.save()
        # Build the appearances
        appearances = self.appearances.all()
        for appearance in appearances:
            appearance.build()
            appearance.save()
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.started, STATUS.verified], target=STATUS.verified, conditions=[can_verify,])
    def verify(self, *args, **kwargs):
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

        # Get all appearances eligible to advance
        multis = self.appearances.filter(
            is_multi=True,
        )
        # If spots are constricted, find those who advance
        if spots:
            # All those above 73.0 advance automatically, regardless of spots available
            automatics = multis.filter(
                run_score__gte=73.0,
            )
            # generate list of the advancers, as appearance IDs
            advancers = [x.id for x in automatics]
            # Figure out remaining spots
            cnt = automatics.count()
            diff = spots - cnt
            print(spots, cnt, diff)
            # If there are additionl remaining spots, add them up to available
            if diff > 0:
                adds = multis.exclude(
                    id__in=advancers,
                ).order_by(
                    '-run_points',
                )[:diff]
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
        mt = self.appearances.filter(
            draw=None,
            is_multi=True,
        ).order_by(
            '-run_points',
        ).first()
        if mt:
            mt.draw = 0
            mt.save()
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.verified], target=STATUS.finished, conditions=[can_finish])
    def finish(self, *args, **kwargs):
        # content = self.get_oss()
        # self.oss.save(
        #     slugify(
        #         '{0} oss'.format(self)
        #     ),
        #     content=content,
        # )
        # content = self.get_sa()
        # self.sa.save(
        #     slugify(
        #         '{0} sa'.format(self)
        #     ),
        #     content=content,
        # )
        finishers = self.appearances.filter(
            Q(draw=0) | Q(draw__isnull=True),
        ).values_list('group', flat=True)
        competitors = self.session.competitors.filter(
            group__id__in=finishers,
        )
        for competitor in competitors:
            competitor.finish()
            competitor.save()
        # panelists = self.panelists.all()
        # for panelist in panelists:
        #     panelist.queue_sa()
        # self.queue_sa()
        return
