
# Standard Library
import logging
import random
import uuid
from io import BytesIO

# Third-Party
import pydf
from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel
from PyPDF2 import PdfFileMerger
from ranking import ORDINAL
from ranking import Ranking

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
        null=True,
        blank=True,
    )
    sa = models.FileField(
        null=True,
        blank=True,
    )
    csa = models.FileField(
        null=True,
        blank=True,
    )

    legacy_oss = models.FileField(
        null=True,
        blank=True,
    )

    legacy_sa = models.FileField(
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
        appearances = self.appearances.filter(
            competitor__is_private=False,
            competitor__status__gt=0,
        ).distinct().order_by('-tot_points')
        points = [x.tot_points for x in appearances]
        ranked = Ranking(points, strategy=ORDINAL, start=1)
        for appearance in appearances:
            appearance.tot_rank = ranked.rank(appearance.tot_points)
            appearance.save()
        appearances = self.appearances.filter(
            competitor__is_private=False,
            competitor__status__gt=0,
        ).distinct().order_by('-mus_points')
        points = [x.mus_points for x in appearances]
        ranked = Ranking(points, start=1)
        for appearance in appearances:
            appearance.mus_rank = ranked.rank(appearance.mus_points)
            appearance.save()
        appearances = self.appearances.filter(
            competitor__is_private=False,
            competitor__status__gt=0,
        ).distinct().order_by('-per_points')
        points = [x.per_points for x in appearances]
        ranked = Ranking(points, start=1)
        for appearance in appearances:
            appearance.per_rank = ranked.rank(appearance.per_points)
            appearance.save()
        appearances = self.appearances.filter(
            competitor__is_private=False,
            competitor__status__gt=0,
        ).distinct().order_by('-sng_points')
        points = [x.sng_points for x in appearances]
        ranked = Ranking(points, start=1)
        for appearance in appearances:
            appearance.sng_rank = ranked.rank(appearance.sng_points)
            appearance.save()
        # Songs ranked relative to Round
        Song = apps.get_model('api.song')
        songs = Song.objects.filter(
            appearance__round=self,
            appearance__competitor__is_private=False,
            appearance__competitor__status__gt=0,
        ).distinct().order_by('-tot_points')
        points = [x.tot_points for x in songs]
        ranked = Ranking(points, strategy=ORDINAL, start=1)
        for song in songs:
            song.tot_rank = ranked.rank(song.tot_points)
            song.save()
        songs = Song.objects.filter(
            appearance__round=self,
            appearance__competitor__is_private=False,
            appearance__competitor__status__gt=0,
        ).distinct().order_by('-mus_points')
        points = [x.mus_points for x in songs]
        ranked = Ranking(points, start=1)
        for song in songs:
            song.mus_rank = ranked.rank(song.mus_points)
            song.save()
        songs = Song.objects.filter(
            appearance__round=self,
            appearance__competitor__is_private=False,
            appearance__competitor__status__gt=0,
        ).distinct().order_by('-per_points')
        points = [x.per_points for x in songs]
        ranked = Ranking(points, start=1)
        for song in songs:
            song.per_rank = ranked.rank(song.per_points)
            song.save()
        songs = Song.objects.filter(
            appearance__round=self,
            appearance__competitor__is_private=False,
            appearance__competitor__status__gt=0,
        ).distinct().order_by('-sng_points')
        points = [x.sng_points for x in songs]
        ranked = Ranking(points, start=1)
        for song in songs:
            song.sng_rank = ranked.rank(song.sng_points)
            song.save()
        return

    def get_oss(self):
        Competitor = apps.get_model('api.competitor')
        Contest = apps.get_model('api.contest')
        Panelist = apps.get_model('api.panelist')
        Contestant = apps.get_model('api.contestant')
        competitors = Competitor.objects.filter(
            Q(appearances__draw=0) | Q(appearances__draw__isnull=True),
            appearances__num__gt=0,
            appearances__round=self,
            is_private=False,
        ).select_related(
            'group',
            'entry',
        ).prefetch_related(
            'entry__contestants',
            'entry__contestants__contest',
            'appearances',
            'appearances__round',
            'appearances__songs',
            'appearances__songs__chart',
            'appearances__songs__scores',
            'appearances__songs__scores__panelist',
            'appearances__songs__scores__panelist__person',
        ).order_by(
            '-tot_points',
            '-sng_points',
            '-per_points',
            'group__name',
        )
        # Eval Only
        privates = self.session.competitors.filter(
            appearances__round=self,
            is_private=True,
        ).select_related(
            'group',
            'entry',
        ).order_by(
            'group__name',
        )
        privates = privates.values_list('group__name', flat=True)
        if self.kind != self.KIND.finals:
            advancers = self.appearances.filter(
                draw__gt=0,
            ).select_related(
                'competitor__group',
            ).order_by(
                'draw',
            )
            mt = self.appearances.filter(
                draw=0,
            ).select_related(
                'competitor__group',
            ).order_by(
                'draw',
            ).first()
        else:
            advancers = None
            mt = None
        contests = self.session.contests.filter(
            num__isnull=False,
        ).select_related(
            'award',
            'group',
        ).distinct(
        ).order_by(
            'num',
        )
        # MonkeyPatch qualifiers
        for contest in contests:
            if self.num >= contest.award.rounds:
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
                            contest.detail = "(Result announced following Finals)"
                else:
                    contest.detail = "(Result determined post-contest)"
            else:
                contest.detail = "(Result not yet determined)"
        panelists = self.panelists.select_related(
            'person',
        ).filter(
            kind=Panelist.KIND.official,
            category__gte=Panelist.CATEGORY.ca,
        ).order_by(
            'category',
            'person__last_name',
            'person__first_name',
        )
        is_multi = all([
            self.session.rounds.count() > 1,
        ])
        context = {
            'round': self,
            'competitors': competitors,
            'privates': privates,
            'advancers': advancers,
            'mt': mt,
            'panelists': panelists,
            'contests': contests,
            'is_multi': is_multi,
        }
        rendered = render_to_string('oss.html', context)
        file = pydf.generate_pdf(
            rendered,
            page_size='Legal',
            orientation='Portrait',
            margin_top='5mm',
            margin_bottom='5mm',
        )
        content = ContentFile(file)
        return content

    def get_sa(self):
        Panelist = apps.get_model('api.panelist')
        panelists = self.panelists.filter(
            kind__in=[
                Panelist.KIND.official,
                Panelist.KIND.practice,
            ],
            category__gt=Panelist.CATEGORY.ca,
        ).select_related(
            'person',
        ).distinct(
        ).order_by(
            'category',
            'kind',
            'person__last_name',
            'person__nick_name',
            'person__first_name',
        )
        mo_count = panelists.filter(
            category=Panelist.CATEGORY.music,
            kind=Panelist.KIND.official,
        ).count()
        po_count = panelists.filter(
            category=Panelist.CATEGORY.performance,
            kind=Panelist.KIND.official,
        ).count()
        so_count = panelists.filter(
            category=Panelist.CATEGORY.singing,
            kind=Panelist.KIND.official,
        ).count()
        mp_count = panelists.filter(
            category=Panelist.CATEGORY.music,
            kind=Panelist.KIND.practice,
        ).count()
        pp_count = panelists.filter(
            category=Panelist.CATEGORY.performance,
            kind=Panelist.KIND.practice,
        ).count()
        sp_count = panelists.filter(
            category=Panelist.CATEGORY.singing,
            kind=Panelist.KIND.practice,
        ).count()
        competitors = self.session.competitors.filter(
            Q(appearances__draw=0) | Q(appearances__draw__isnull=True),
            appearances__round=self,
        ).select_related(
            'group',
        ).prefetch_related(
            'appearances',
            'appearances__songs',
            'appearances__songs__scores',
            'appearances__songs__scores__panelist',
            'appearances__songs__scores__panelist__person',
        ).order_by(
            '-tot_points',
            '-sng_points',
            '-mus_points',
            '-per_points',
            'group__name',
        )
        context = {
            'round': self,
            'panelists': panelists,
            'competitors': competitors,
            'mo_count': mo_count,
            'po_count': po_count,
            'so_count': so_count,
            'mp_count': mp_count,
            'pp_count': pp_count,
            'sp_count': sp_count,
        }
        rendered = render_to_string('sa.html', context)
        file = pydf.generate_pdf(
            rendered,
            page_size='Letter',
            orientation='Landscape',
        )
        content = ContentFile(file)
        return content

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
        Award = apps.get_model('api.award')
        return all([
            not self.appearances.exclude(status=self.appearances.model.STATUS.verified),
        ])

    def can_finish(self):
        return all([
            not self.appearances.exclude(status=self.appearances.model.STATUS.verified),
            not self.session.contests.filter(
                award__level=Award.LEVEL.manual,
                award__rounds=self.num,
                group__isnull=True,
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
        # Create the appearances
        Competitor = apps.get_model('api.competitor')
        Grid = apps.get_model('api.grid')
        competitors = self.session.competitors.filter(
            status__gt=0,
        )
        for competitor in competitors:
            if self.num == 1:
                num = competitor.entry.draw
            else:
                prior_round = self.session.rounds.get(num=self.num - 1)
                prior_appearance = prior_round.appearances.get(
                    competitor=competitor,
                )
                num = prior_appearance.draw
            appearance = self.appearances.create(
                competitor=competitor,
                num=num,
            )
            defaults = {
                'appearance': appearance,
            }
            grid, created = Grid.objects.update_or_create(
                round=self,
                num=num,
                defaults=defaults,
            )
        # MT
        # mt = self.session.competitors.filter(
        #     status=Competitor.STATUS.finished,
        # ).order_by(
        #     '-tot_points',
        #     '-sng_points',
        #     '-per_points',
        # ).first()
        # self.appearances.create(
        #     competitor=mt,
        #     num=0,
        # )
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
    @transition(field=status, source='*', target=STATUS.verified, conditions=[can_verify,])
    def verify(self, *args, **kwargs):
        Competitor = apps.get_model('api.competitor')
        Contestant = apps.get_model('api.contestant')
        # Run rankings.
        self.rank()
        self.session.rank()

        # No next round.
        if self.kind == self.KIND.finals:
            # Run relevant contests yet to be determined
            contests = self.session.contests.filter(
                num__isnull=False,
                group__isnull=True,
            )
            for contest in contests:
                contest.determine()
                contest.save()
            return

        # If not finals, only determine winners when no contestants
        # are in multi-round contests to avoid leaking standings.
        contests = self.session.contests.filter(
            num__isnull=False,
            award__rounds__lte=self.num,
            contestants__status=Contestant.STATUS.included,
            contestants__entry__competitor__is_multi=False,
        ).distinct()

        # for contest in contests:
        #     contest.determine()
        #     contest.save()

        # Get spots available
        spots = self.spots

        # Get all multi competitors.
        multis = self.session.competitors.filter(
            status__gt=0,
            is_multi=True,
        )
        if spots:
            # All those above 73.0 advance automatically
            automatics = multis.filter(
                tot_score__gte=73.0,
            )
            cnt = automatics.count()
            # create list of advancers
            advancers = [a.id for a in automatics]
            diff = spots - cnt
            if diff > 0:
                adds = multis.exclude(
                    id__in=advancers,
                ).order_by(
                    '-tot_points',
                    '-sng_points',
                    '-per_points',
                )[:diff]
                for a in adds:
                    advancers.append(a.id)
        else:
            advancers = [a.id for a in multis]

        # Reset draw
        self.appearances.update(draw=None)
        # Get advancers and draw
        appearances = self.appearances.filter(
            competitor__id__in=advancers,
        ).order_by('?')
        i = 1
        for appearance in appearances:
            appearance.draw = i
            appearance.save()
            i += 1
        # create MT
        mt = self.appearances.filter(
            draw=None,
            competitor__is_multi=True,
        ).order_by(
            '-tot_points',
            '-sng_points',
            '-per_points',
        ).first()
        mt.draw = 0
        mt.save()
        return

    @fsm_log_by
    @transition(field=status, source=[STATUS.verified], target=STATUS.finished)
    def finish(self, *args, **kwargs):
        content = self.get_oss()
        self.oss.save(
            slugify(
                '{0} oss'.format(self)
            ),
            content=content,
        )
        content = self.get_sa()
        self.sa.save(
            slugify(
                '{0} sa'.format(self)
            ),
            content=content,
        )
        finishers = self.appearances.filter(
            draw=None,
        )
        for finisher in finishers:
            finisher.competitor.finish()
            finisher.competitor.save()
        return
