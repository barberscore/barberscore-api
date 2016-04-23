from __future__ import division

import os

import logging

import uuid

import datetime

from psycopg2.extras import DateTimeTZRange

import arrow

from django.utils import timezone

from django.db import (
    models,
)

from django.apps import apps

from django.contrib.postgres.fields import (
    DateRangeField,
    DateTimeRangeField,
    IntegerRangeField,
    FloatRangeField,
    ArrayField,
)

from django.core.validators import (
    RegexValidator,
    MaxValueValidator,
    MinValueValidator,
)

from django_fsm import (
    transition,
    FSMIntegerField,
)

# from django_fsm_log.decorators import fsm_log_by

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)

from django.core.exceptions import (
    ValidationError,
)

from model_utils.models import (
    TimeStampedModel,
)

from model_utils import Choices

from mptt.models import (
    MPTTModel,
    TreeForeignKey,
)

from timezone_field import TimeZoneField

from phonenumber_field.modelfields import PhoneNumberField

from nameparser import HumanName

from ranking import Ranking

from .managers import (
    UserManager,
)

log = logging.getLogger(__name__)


def generate_image_filename(instance, filename):
    f, ext = os.path.splitext(filename)
    return '{0}{1}'.format(instance.id, ext)


class Assistant(TimeStampedModel):
    """Panel Judge."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    CATEGORY = Choices(
        (10, 'aca', 'ACA'),
        (20, 'other', 'Other'),
    )

    category = models.IntegerField(
        choices=CATEGORY,
        null=True,
        blank=True,
    )

    KIND = Choices(
        (10, 'official', 'Official'),
        (20, 'practice', 'Practice'),
        (25, 'guest', 'Guest'),
        (30, 'composite', 'Composite'),
    )

    kind = models.IntegerField(
        choices=KIND,
    )

    session = models.ForeignKey(
        'Session',
        related_name='assistants',
    )

    person = models.ForeignKey(
        'Person',
        related_name='assistants',
    )

    organization = TreeForeignKey(
        'Organization',
        related_name='assistants',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.session.name,
            self.person.name,
        ]))
        super(Assistant, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('session', 'person',),
        )

    class JSONAPIMeta:
        resource_name = "assistant"


class Award(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'inactive', 'Inactive',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    KIND = Choices(
        (1, 'quartet', 'Quartet',),
        (2, 'chorus', 'Chorus',),
        (10, 'seniors', 'Seniors',),
        (20, 'collegiate', 'Collegiate',),
        (30, 'youth', 'Youth',),
    )

    kind = models.IntegerField(
        choices=KIND,
    )

    SEASON = Choices(
        (1, 'international', 'International',),
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
        # (180, 'pb', 'Plateau B',),
        # (190, 'pi', 'Plateau I',),
        # (200, 'pii', 'Plateau II',),
        # (210, 'piii', 'Plateau III',),
        # (220, 'piv', 'Plateau IV',),
        # (230, 'small', 'Small',),
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

    num_rounds = models.IntegerField(
    )

    is_primary = models.BooleanField(
        default=False,
    )

    is_improved = models.BooleanField(
        default=False,
    )

    is_novice = models.BooleanField(
        default=False,
    )

    is_manual = models.BooleanField(
        default=False,
    )

    idiom = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    cutoff = models.FloatField(
        null=True,
        blank=True,
    )

    minimum = models.FloatField(
        null=True,
        blank=True,
    )

    stix_num = models.IntegerField(
        null=True,
        blank=True,
    )

    stix_name = models.CharField(
        max_length=200,
        blank=True,
        default="",
    )

    organization = TreeForeignKey(
        'Organization',
        related_name='awards',
        on_delete=models.CASCADE,
    )

    # Denormalization
    LEVEL = Choices(
        (0, 'international', "International"),
        (1, 'district', "District/Affiliates"),
        (2, 'division', "Division"),
        (3, 'chapter', "Chapter"),
    )

    level = models.IntegerField(
        choices=LEVEL,
        editable=False,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.level = self.organization.level
        if self.is_improved:
            most_improved = 'Most-Improved'
        else:
            most_improved = None
        if self.is_novice:
            novice = 'Novice'
        else:
            novice = None
        self.name = " ".join(filter(None, [
            self.organization.name,
            most_improved,
            novice,
            self.get_size_display(),
            self.get_scope_display(),
            self.idiom,
            self.get_kind_display(),
        ]))
        super(Award, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            (
                'organization',
                'is_improved',
                'is_novice',
                'size',
                'scope',
                'idiom',
                'kind',
            ),
        )

    class JSONAPIMeta:
        resource_name = "award"


class Certification(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    CATEGORY = Choices(
        (0, 'admin', 'Admin'),
        (1, 'music', 'Music'),
        (2, 'presentation', 'Presentation'),
        (3, 'singing', 'Singing'),
    )

    category = models.IntegerField(
        choices=CATEGORY,
    )

    STATUS = Choices(
        (0, 'new', 'New'),
        (1, 'active', 'Active'),
        (2, 'candidate', 'Candidate'),
        (3, 'inactive', 'Inactive'),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    date = DateRangeField(
        help_text="""
            The active dates of the resource.""",
        null=True,
        blank=True,
    )

    person = models.ForeignKey(
        'Person',
        related_name='certifications',
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1}".format(
            self.person,
            " - ",
            self.get_category_display(),
        )
        super(Certification, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('category', 'person',),
        )

    class JSONAPIMeta:
        resource_name = "certification"


class Chapter(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the resource.""",
        max_length=200,
        blank=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'inactive', 'Inactive',),
        (30, 'affiliate', 'Affiliate',),
        (50, 'dup', 'Duplicate',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    code = models.CharField(
        help_text="""
            The chapter code.""",
        unique=True,
        max_length=200,
        blank=True,
        null=True,
    )

    organization = TreeForeignKey(
        'Organization',
        related_name='chapters',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    bhs_id = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
    )

    bhs_name = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_chapter_name = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_group_name = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_chapter_code = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_website = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_district = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_venue = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_address = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_city = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_state = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_zip = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_contact = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_phone = models.CharField(
        max_length=255,
        blank=True,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    class JSONAPIMeta:
        resource_name = "chapter"


class Chart(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New'),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    is_generic = models.BooleanField(
        default=False,
    )

    is_parody = models.BooleanField(
        default=False,
    )

    is_medley = models.BooleanField(
        default=False,
    )

    title = models.CharField(
        max_length=200,
    )

    arranger = models.CharField(
        blank=True,
        max_length=200,
    )

    composer = models.CharField(
        blank=True,
        max_length=200,
    )

    lyricist = models.CharField(
        blank=True,
        max_length=200,
    )

    bhs_id = models.IntegerField(
        null=True,
        blank=True,
        unique=True,
    )

    bhs_marketplace = models.IntegerField(
        null=True,
        blank=True,
        unique=True,
    )

    bhs_published = models.DateField(
        null=True,
        blank=True,
    )

    bhs_songname = models.CharField(
        blank=True,
        max_length=200,
    )

    bhs_arranger = models.CharField(
        blank=True,
        max_length=200,
    )

    bhs_fee = models.FloatField(
        null=True,
        blank=True,
    )

    bhs_songname = models.CharField(
        blank=True,
        max_length=200,
    )

    bhs_copyright_date = models.CharField(
        blank=True,
        max_length=200,
    )

    bhs_copyright_owner = models.CharField(
        blank=True,
        max_length=200,
    )

    DIFFICULTY = Choices(
        (1, "Very Easy"),
        (2, "Easy"),
        (3, "Medium"),
        (4, "Hard"),
        (5, "Very Hard"),
    )

    bhs_difficulty = models.IntegerField(
        null=True,
        blank=True,
        choices=DIFFICULTY
    )

    TEMPO = Choices(
        (1, "Ballad"),
        (2, "Uptune"),
        (3, "Mixed"),
    )

    bhs_tempo = models.IntegerField(
        null=True,
        blank=True,
        choices=TEMPO,
    )

    bhs_medley = models.BooleanField(
        default=False,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        if self.bhs_marketplace:
            bhs_marketplace = "[{0}]".format(self.bhs_marketplace)
        else:
            bhs_marketplace = None
        self.name = " ".join(filter(None, [
            self.title,
            bhs_marketplace,
        ]))
        super(Chart, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('title', 'bhs_marketplace',),
        )

    class JSONAPIMeta:
        resource_name = "chart"


class Contest(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=200,
        unique=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (20, 'started', 'Started',),
        # (25, 'ranked', 'Ranked',),
        (30, 'finished', 'Finished',),
        (40, 'drafted', 'Drafted',),
        (45, 'published', 'Published',),
        (50, 'final', 'Final',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    CYCLE_CHOICES = []
    for r in reversed(range(1939, (datetime.datetime.now().year + 2))):
        CYCLE_CHOICES.append((r, r))

    cycle = models.IntegerField(
        choices=CYCLE_CHOICES,
        editable=False,
    )

    # Denorm
    is_qualifier = models.BooleanField(
        default=False,
        editable=False,
    )

    stix_num = models.IntegerField(
        null=True,
        blank=True,
    )

    stix_name = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )

    session = models.ForeignKey(
        'Session',
        related_name='contests',
    )

    award = models.ForeignKey(
        'Award',
        related_name='contests',
    )

    champion = models.OneToOneField(
        'Contestant',
        related_name='contests',
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        if self.session.convention.season == self.session.convention.SEASON.spring:
            self.cycle = self.session.convention.year
        else:
            self.cycle = self.session.convention.year + 1
        if any([
            all([
                self.session.convention.level == self.session.convention.LEVEL.district,
                self.award.level == self.award.LEVEL.international,
            ]),
            all([
                self.session.convention.division,
                self.award.level != self.award.LEVEL.division,
            ]),
        ]):
            self.is_qualifier = True
        if self.is_qualifier:
            prefix = self.session.name
            suffix = "Qualifier"
        else:
            prefix = None
            suffix = "Championship"
        self.name = " ".join(filter(None, [
            prefix,
            self.award.name,
            suffix,
            str(self.session.convention.year),
            self.id.hex,
        ]))
        super(Contest, self).save(*args, **kwargs)

    def build(self):
        # TODO Future Award/Contestant mapping
        return

    def rank(self):
        if self.award.is_manual:
            return
        if self.award.num_rounds > self.session.completed_rounds:
            return
        contestants = self.contestants.all()
        for contestant in self.contestants.all():
            contestant.calculate()
            contestant.save()
        contestants = self.contestants.order_by('-total_points')
        points = [contestant.total_points for contestant in contestants]
        ranking = Ranking(points, start=1)
        for contestant in contestants:
            if self.is_qualifier:
                if self.award.level == self.award.LEVEL.international:
                    if self.award.kind == self.award.KIND.quartet:
                        if contestant.total_score >= self.award.cutoff:
                            contestant.status = contestant.STATUS.qualified
                        elif contestant.total_score < self.award.minimum:
                            contestant.status = contestant.STATUS.ineligible
                        else:
                            contestant.status = contestant.STATUS.eligible
                    elif self.award.kind == self.award.KIND.chorus:
                        if ranking.rank(contestant.total_points) == 1:
                            contestant.status = contestant.STATUS.qualified
                        elif contestant.total_score < self.award.minimum:
                            contestant.status = contestant.STATUS.ineligible
                        else:
                            contestant.status = contestant.STATUS.eligible
                    elif self.award.kind == self.award.KIND.seniors:
                        if ranking.rank(contestant.total_points) == 1:
                            contestant.status = contestant.STATUS.qualified
                        else:
                            contestant.status = contestant.STATUS.eligible
                    elif self.award.kind == self.award.KIND.youth or self.award.kind == self.award.KIND.collegiate:
                        if ranking.rank(contestant.total_points) == 1:
                            contestant.status = contestant.STATUS.qualified
                        elif contestant.total_score < self.award.minimum:
                            contestant.status = contestant.STATUS.ineligible
                        elif contestant.total_score >= self.award.cutoff:
                            contestant.status = contestant.STATUS.qualified
                        else:
                            contestant.rank = contestant.STATUS.eligible
                    else:
                        raise RuntimeError("No Award Kind")
                else:
                    log.error("District Qual not run")
                    continue  # TODO DIstrict Quals
            else:
                contestant.rank = ranking.rank(contestant.total_points)
                contestant.status = contestant.STATUS.ranked
                if contestant.rank == 1:
                    self.champion = contestant
            contestant.save()
        self.status = self.STATUS.drafted
        self.save()
        return

    class Meta:
        unique_together = (
            ('session', 'award',)
        )

    class JSONAPIMeta:
        resource_name = "contest"


class Contestant(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'eligible', 'Eligible',),
        (20, 'ineligible', 'Ineligible',),
        (30, 'dnq', 'Did Not Qualify',),
        (50, 'qualified', 'Qualified',),
        (60, 'ranked', 'Ranked',),
        (90, 'final', 'Final',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    performer = models.ForeignKey(
        'Performer',
        related_name='contestants',
    )

    contest = models.ForeignKey(
        'Contest',
        related_name='contestants',
    )

    # Denormalization
    rank = models.IntegerField(
        help_text="""
            The final ranking relative to this award.""",
        null=True,
        blank=True,
        editable=False,
    )

    mus_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_points = models.IntegerField(
        null=True,
        editable=False,
        blank=True,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    total_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    total_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.contest.award.name,
            str(self.performer.session.convention.year),
            # self.performer.group.name,
            # self.contest.award.name,
            self.performer.name,
        ]))
        super(Contestant, self).save(*args, **kwargs)

    def calculate(self):
        Score = apps.get_model('api', 'Score')
        scores = Score.objects.filter(
            song__performance__performer=self.performer,
            song__performance__round__num__lte=self.contest.award.num_rounds,
        ).exclude(
            kind=Score.KIND.practice,
        ).order_by(
            'category',
        ).values(
            'category',
        ).annotate(
            total=models.Sum('points'),
            average=models.Avg('points'),
        )
        for score in scores:
            if score['category'] == Score.CATEGORY.music:
                self.mus_points = score['total']
                self.mus_score = round(score['average'], 1)
            if score['category'] == Score.CATEGORY.presentation:
                self.prs_points = score['total']
                self.prs_score = round(score['average'], 1)
            if score['category'] == Score.CATEGORY.singing:
                self.sng_points = score['total']
                self.sng_score = round(score['average'], 1)

        # Calculate total points.
        try:
            self.total_points = sum([
                self.mus_points,
                self.prs_points,
                self.sng_points,
            ])
        except TypeError:
            self.total_points = None

        # Calculate total score.
        try:
            self.total_score = round(sum([
                self.mus_score,
                self.prs_score,
                self.sng_score,
            ]) / 3, 1)
        except TypeError:
            self.total_score = None

    class Meta:
        unique_together = (
            ('performer', 'contest',),
        )

    class JSONAPIMeta:
        resource_name = "contestant"


class Convention(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'scheduled', 'Scheduled',),
        (15, 'upcoming', 'Upcoming',),
        (20, 'started', 'Started',),
        (30, 'finished', 'Finished',),
        (40, 'recent', 'Recent',),
        (50, 'final', 'Final',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    KIND = Choices(
        (10, 'international', 'International'),
        (20, 'district', 'District'),
        (30, 'division', 'Division'),
        (40, 'disdiv', 'District and Division'),
    )

    kind = models.IntegerField(
        choices=KIND,
        null=True,
        blank=True,
    )

    SEASON = Choices(
        (1, 'international', 'International',),
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

    risers = ArrayField(
        base_field=models.IntegerField(null=True, blank=True),
        null=True,
        blank=True,
    )

    # Denormalization
    LEVEL = Choices(
        (0, 'international', "International"),
        (1, 'district', "District"),
        (2, 'division', "Division"),
        (3, 'chapter', "Chapter"),
    )

    level = models.IntegerField(
        choices=LEVEL,
        null=True,
        blank=True,
        editable=False,
    )

    DIVISION = Choices(
        (200, 'evgd1', "Division I"),
        (210, 'evgd2', "Division II"),
        (220, 'evgd3', "Division III"),
        (230, 'evgd4', "Division IV"),
        (240, 'evgd5', "Division V"),
        (250, 'fwdaz', "Arizona Division"),
        (260, 'fwdnenw', "NE/NW Divisions"),
        (270, 'fwdsesw', "SE/SW Divisions"),
        (280, 'lolp1', "Division One/Packerland Divisions"),
        (290, 'lolnp', "Northern Plains Division"),
        (300, 'lol10sw', "10,000 Lakes and Southwest Divisions"),
        # (310, 'madatl', "Atlantic Division"),  <- LEGACY
        # (320, 'madnw', "Northern and Western Divisions"), <- LEGACY
        (322, 'madnth', "Northern Division"),
        (324, 'madcen', "Central Division"),
        (330, 'madsth', "Southern Division"),
        (340, 'nedsun', "Sunrise Division"),
        (342, 'nedwst', "Western Regional"),
        (344, 'nedest', "Eastern Regional"),
        (350, 'swdnenwsesw', "NE/NW/SE/SW Divisions"),
    )

    division = models.IntegerField(
        help_text="""
            Detail if division/combo convention.""",
        choices=DIVISION,
        null=True,
        blank=True,
    )

    YEAR_CHOICES = []
    for r in reversed(range(1939, (datetime.datetime.now().year + 2))):
        YEAR_CHOICES.append((r, r))

    year = models.IntegerField(
        choices=YEAR_CHOICES,
        null=True,
        blank=True,
        # editable=False,
    )

    date = DateTimeRangeField(
        help_text="""
            The scheduled time frame for the convention.""",
        null=True,
        blank=True,
    )

    location = models.CharField(
        help_text="""
            The location of the convention.""",
        max_length=200,
        blank=True,
    )

    venue = models.ForeignKey(
        'Venue',
        null=True,
        blank=True,
        related_name='conventions',
        help_text="""
            The venue for the convention.""",
    )

    organization = TreeForeignKey(
        'Organization',
        help_text="""
            The organization hosting the convention.""",
        related_name='conventions',
        null=True,
        blank=True,
    )

    drcj = models.ForeignKey(
        'Person',
        null=True,
        blank=True,
        related_name='conventions',
        help_text="""
            The person managing the convention.""",
    )

    stix_name = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    stix_div = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    stix_file = models.FileField(
        help_text="""
            The bbstix file.""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    @transition(field=status, source='*', target=STATUS.started)
    def start(self, *args, **kwargs):
        return

    @transition(field=status, source='*', target=STATUS.finished)
    def finish(self, *args, **kwargs):
        return

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        # self.year = arrow.get(self.date.lower).year
        # if self.division:
        #     self.level = self.LEVEL.division
        # else:
        #     self.level = self.organization.level
        # if self.division:
        #     division = str(self.get_division_display())
        # else:
        #     division = None
        organizations = " ".join(filter(None, [
            p.organization.short_name for p in self.participants.all()
        ]))
        self.name = " ".join(filter(None, [
            organizations,
            # division,
            self.get_season_display(),
            u"Convention",
            str(self.year),
        ]))
        super(Convention, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('organization', 'season', 'year', 'division',),
        )

    class JSONAPIMeta:
        resource_name = "convention"


class Group(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the resource.""",
        max_length=200,
        blank=False,
        error_messages={
            'unique': 'The name must be unique.  Add middle initials, suffixes, years, or other identifiers to make the name unique.',
        }
    )

    date = DateRangeField(
        help_text="""
            The active dates of the resource.""",
        null=True,
        blank=True,
    )

    location = models.CharField(
        help_text="""
            The geographical location of the resource.""",
        max_length=200,
        blank=True,
        default='',
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
        default='',
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
        default='',
    )

    phone = PhoneNumberField(
        help_text="""
            The phone number of the resource.  Include country code.""",
        blank=True,
        default='',
    )

    picture = models.ImageField(
        upload_to=generate_image_filename,
        help_text="""
            The picture/logo of the resource.""",
        blank=True,
        null=True,
    )

    description = models.TextField(
        help_text="""
            A description/bio of the resource.  Max 1000 characters.""",
        blank=True,
        max_length=1000,
    )

    notes = models.TextField(
        help_text="""
            Notes (for internal use only).""",
        blank=True,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'inactive', 'Inactive',),
        (50, 'dup', 'Duplicate',),
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    KIND = Choices(
        (1, 'quartet', 'Quartet'),
        (2, 'chorus', 'Chorus'),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of group; choices are Quartet or Chorus.""",
        choices=KIND,
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

    is_novice = models.BooleanField(
        default=False,
    )

    chapter = models.ForeignKey(
        'Chapter',
        related_name='groups',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    organization = models.ForeignKey(
        'Organization',
        related_name='groups',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    chap_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        editable=False,
    )

    bhs_id = models.IntegerField(
        unique=True,
        null=True,
        blank=True,
    )

    bhs_name = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_chapter_name = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_chapter_code = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_website = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_district = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_location = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_contact = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_phone = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_expiration = models.CharField(
        max_length=255,
        blank=True,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        if self.kind == self.KIND.chorus:
            try:
                self.chap_name = u"{0} {1} - {2}".format(
                    self.chapter.code,
                    self.chapter.name,
                    self.name,
                )
            except AttributeError:
                self.chap_name = self.name
        else:
            self.chap_name = self.name
        super(Group, self).save(*args, **kwargs)

    class JSONAPIMeta:
        resource_name = "group"


class Judge(TimeStampedModel):
    """Panel Judge."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'scheduled', 'Scheduled',),
        (20, 'confirmed', 'Confirmed',),
        (30, 'final', 'Final',),
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    CATEGORY = Choices(
        (1, 'music', 'Music'),
        (2, 'presentation', 'Presentation'),
        (3, 'singing', 'Singing'),
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

    slot = models.IntegerField(
        null=True,
        blank=True,
    )

    session = models.ForeignKey(
        'Session',
        related_name='judges',
    )

    person = models.ForeignKey(
        'Person',
        related_name='panels',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    organization = TreeForeignKey(
        'Organization',
        related_name='judges',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    bhs_panel_id = models.IntegerField(
        null=True,
        blank=True,
    )

    @property
    def designation(self):
        designation = u"{0[0]}{1:1d}".format(
            self.get_category_display(),
            self.slot,
        )
        return designation

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        # Very hacky slot designator
        if not self.slot:
            try:
                self.slot = self.__class__.objects.filter(
                    session=self.session,
                    category=self.category,
                    kind=self.kind,
                ).aggregate(
                    max=models.Max('slot')
                )['max'] + 1
            except TypeError:
                if self.kind == self.KIND.practice:
                    self.slot = 6
                else:
                    self.slot = 1
        self.name = u"{0} {1} {2} {3}".format(
            self.session,
            self.get_kind_display(),
            self.get_category_display(),
            self.slot,
        )
        super(Judge, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('session', 'category', 'kind', 'slot'),
        )

    class JSONAPIMeta:
        resource_name = "judge"


class Member(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'inactive', 'Inactive',),
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    chapter = models.ForeignKey(
        'Chapter',
        related_name='members',
        on_delete=models.CASCADE,
    )

    person = models.ForeignKey(
        'Person',
        related_name='members',
        on_delete=models.CASCADE,
    )

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.chapter.name,
            self.person.name,
        ]))
        super(Member, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('chapter', 'person',),
        )

    class JSONAPIMeta:
        resource_name = "member"


class Organization(MPTTModel, TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the resource.""",
        max_length=200,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'inactive', 'Inactive',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    LEVEL = Choices(
        (0, 'international', "International"),
        (1, 'district', "District/Affiliates"),
        (2, 'division', "Division"),
        (3, 'chapter', "Chapter"),
    )

    level = models.IntegerField(
        choices=LEVEL,
        null=True,
        blank=True,
    )

    KIND = Choices(
        ('International', [
            (0, 'international', "International"),
            (50, 'hi', "Harmony Incorporated"),
        ]),
        ('District', [
            (10, 'district', "District"),
            (20, 'noncomp', "Noncompetitive"),
            (30, 'affiliate', "Affiliate"),
        ]),
        ('Division', [
            (40, 'division', "Division"),
        ]),
        ('Chapter', [
            (60, 'chapter', "Chapter"),
        ]),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of organization.""",
        choices=KIND,
        null=True,
        blank=True,
    )

    date = DateRangeField(
        help_text="""
            The active dates of the resource.""",
        null=True,
        blank=True,
    )

    location = models.CharField(
        help_text="""
            The geographical location of the resource.""",
        max_length=200,
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

    phone = PhoneNumberField(
        help_text="""
            The phone number of the resource.  Include country code.""",
        blank=True,
        null=True,
    )

    picture = models.ImageField(
        upload_to=generate_image_filename,
        help_text="""
            The picture/logo of the resource.""",
        blank=True,
        null=True,
    )

    description = models.TextField(
        help_text="""
            A description/bio of the resource.  Max 1000 characters.""",
        blank=True,
        max_length=1000,
    )

    notes = models.TextField(
        help_text="""
            Notes (for internal use only).""",
        blank=True,
    )

    short_name = models.CharField(
        help_text="""
            A short-form name for the resource.""",
        blank=True,
        max_length=200,
    )

    long_name = models.CharField(
        help_text="""
            A long-form name for the resource.""",
        blank=True,
        max_length=200,
    )

    code = models.CharField(
        help_text="""
            The chapter code.""",
        max_length=200,
        blank=True,
        null=True,
    )

    bhs_id = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
    )

    bhs_name = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_chapter_name = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_group_name = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_chapter_code = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_website = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_district = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_venue = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_address = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_city = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_state = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_zip = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_contact = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_phone = models.CharField(
        max_length=255,
        blank=True,
    )

    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        on_delete=models.SET_NULL,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    class MPTTMeta:
        order_insertion_by = [
            'kind',
            'short_name',
        ]
        ordering = (
            'tree_id',
        )

    class JSONAPIMeta:
        resource_name = "organization"


class Participant(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    convention = models.ForeignKey(
        'Convention',
        related_name='participants',
        null=True,
        blank=True,
    )

    organization = models.ForeignKey(
        'Organization',
        related_name='participants',
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.convention.name,
            self.organization.name,
        ]))
        super(Participant, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('organization', 'convention',),
        )

    class JSONAPIMeta:
        resource_name = "participant"


class Performance(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'started', 'Started',),
        (20, 'finished', 'Finished',),
        (30, 'completed', 'Completed',),
        (50, 'confirmed', 'Confirmed',),
        (90, 'final', 'Final',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    slot = models.IntegerField(
        null=True,
        blank=True,
    )

    scheduled = DateTimeRangeField(
        help_text="""
            The scheduled performance window.""",
        null=True,
        blank=True,
    )

    actual = DateTimeRangeField(
        help_text="""
            The actual performance window.""",
        null=True,
        blank=True,
    )

    # Denormalized
    rank = models.IntegerField(
        help_text="""
            The final ranking relative to this round.""",
        null=True,
        blank=True,
        editable=False,
    )

    mus_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    total_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    total_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    round = models.ForeignKey(
        'Round',
        related_name='performances',
    )

    performer = models.ForeignKey(
        'Performer',
        related_name='performances',
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.round.session.convention.organization.name,
            str(self.round.session.convention.get_division_display()),
            self.round.session.convention.get_season_display(),
            self.round.session.get_kind_display(),
            self.round.get_kind_display(),
            str(self.round.session.convention.year),
            "Performance",
            self.id.hex,
        ]))
        super(Performance, self).save(*args, **kwargs)

    # class Meta:
    #     unique_together = (
    #         ('round', 'slot',),
    #     )

    class JSONAPIMeta:
        resource_name = "performance"

    def calculate(self):
        Score = apps.get_model('api', 'Score')
        scores = Score.objects.filter(
            song__performance=self,
        ).exclude(
            kind=Score.KIND.practice,
        ).order_by(
            'category',
        ).values(
            'category',
        ).annotate(
            total=models.Sum('points'),
            average=models.Avg('points'),
        )
        for score in scores:
            if score['category'] == Score.CATEGORY.music:
                self.mus_points = score['total']
                self.mus_score = round(score['average'], 1)
            if score['category'] == Score.CATEGORY.presentation:
                self.prs_points = score['total']
                self.prs_score = round(score['average'], 1)
            if score['category'] == Score.CATEGORY.singing:
                self.sng_points = score['total']
                self.sng_score = round(score['average'], 1)

        # Calculate total points.
        try:
            self.total_points = sum([
                self.mus_points,
                self.prs_points,
                self.sng_points,
            ])
        except TypeError:
            self.total_points = None

        # Calculate total score.
        try:
            self.total_score = round(sum([
                self.mus_score,
                self.prs_score,
                self.sng_score,
            ]) / 3, 1)
        except TypeError:
            self.total_score = None

    def move_top(self):
        performances = self.round.performances.filter(
            slot__lt=self.slot,
        ).order_by('-slot')
        top = performances.last().scheduled
        slot_cursor = self.slot
        scheduled_cursor = self.scheduled
        for performance in performances:
            prior_slot = performance.slot
            prior_scheduled = performance.scheduled
            performance.slot = slot_cursor
            performance.scheduled = scheduled_cursor
            performance.save()
            slot_cursor = prior_slot
            scheduled_cursor = prior_scheduled
        self.slot = 1
        self.scheduled = top
        self.save()
        return {'success': 'moved'}

    def move_up(self):
        old_slot = self.slot
        if old_slot == 1:
            return {'success': 'already at top'}
        self.slot = -1
        self.save()
        new_slot = old_slot - 1
        replaced = self.round.performances.get(
            slot=new_slot,
        )
        replaced.slot = old_slot
        replaced.save()
        self.slot = new_slot
        self.save()
        return {'success': 'moved'}

    def move_down(self):
        old_slot = self.slot
        max_slot = self.round.performances.aggregate(m=models.Max('slot'))['m']
        if old_slot == max_slot:
            return {'success': 'already at bottom'}
        self.slot = -1
        self.save()
        new_slot = old_slot + 1
        replaced = self.round.performances.get(
            slot=new_slot,
        )
        replaced.slot = old_slot
        replaced.save()
        self.slot = new_slot
        self.save()
        return {'success': 'moved'}

    def move_bottom(self):
        i = self.slot
        self.slot = -1
        self.save()
        performances = self.round.performances.filter(
            slot__gt=i,
        ).order_by('slot')
        total = performances.aggregate(m=models.Max('slot'))['m']
        for performance in performances:
            performance.slot -= 1
            performance.save()
        self.slot = total
        self.save()
        return {'success': 'moved'}

    def scratch(self):
        i = self.slot
        self.slot = -1
        self.save()
        performances = self.round.performances.filter(
            slot__gt=i,
        ).order_by('slot')
        for performance in performances:
            performance.slot -= 1
            performance.save()
        self.performer.status = self.performer.STATUS.dropped
        self.performer.save()
        self.delete()
        return {'success': 'scratched'}

    def build(self):
        i = 1
        while i <= 2:
            song, c = self.songs.get_or_create(
                performance=self,
                order=i,
            )
            for judge in self.round.session.judges.all():
                song.scores.get_or_create(
                    song=song,
                    judge=judge,
                    category=judge.category,
                    kind=judge.kind,
                )
            i += 1
        return

    @transition(field=status, source='*', target=STATUS.started)
    def start(self, *args, **kwargs):
        self.actual = DateTimeTZRange(
            lower=timezone.now(),
            upper=timezone.now() + datetime.timedelta(minutes=10),
        )
        return

    @transition(field=status, source='*', target=STATUS.finished)
    def finish(self, *args, **kwargs):
        self.actual = DateTimeTZRange(
            lower=self.actual.lower,
            upper=timezone.now(),
        )
        return

    @transition(field=status, source='*', target=STATUS.completed)
    def complete(self, *args, **kwargs):
        self.calculate()
        return

    @property
    def get_preceding(self):
        try:
            obj = self.__class__.objects.get(
                round=self.round,
                slot=self.slot - 1,
            )
            return obj.id
        except self.DoesNotExist:
            return None
        except TypeError:
            return None

    @property
    def get_next(self):
        try:
            obj = self.__class__.objects.get(
                round=self.round,
                slot=self.slot + 1,
            )
            return obj.id
        except self.DoesNotExist:
            return None
        except TypeError:
            return None


class Performer(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'qualified', 'Qualified',),
        (20, 'accepted', 'Accepted',),
        (30, 'declined', 'Declined',),
        (40, 'dropped', 'Dropped',),
        (50, 'official', 'Official',),
        (55, 'disqualified', 'Disqualified',),
        (60, 'finished', 'Finished',),
        (90, 'final', 'Final',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    picture = models.ImageField(
        help_text="""
            The on-stage session picture (as opposed to the "official" photo).""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    men = models.IntegerField(
        help_text="""
            The number of men on stage.""",
        default=4,
        null=True,
        blank=True,
    )

    tenor = models.ForeignKey(
        'Role',
        null=True,
        blank=True,
        related_name='performers_tenor',
        on_delete=models.SET_NULL,
    )

    lead = models.ForeignKey(
        'Role',
        null=True,
        blank=True,
        related_name='performers_lead',
        on_delete=models.SET_NULL,
    )

    baritone = models.ForeignKey(
        'Role',
        null=True,
        blank=True,
        related_name='performers_baritone',
        on_delete=models.SET_NULL,
    )

    bass = models.ForeignKey(
        'Role',
        null=True,
        blank=True,
        related_name='performers_bass',
        on_delete=models.SET_NULL,
    )

    director = models.ForeignKey(
        'Role',
        null=True,
        blank=True,
        related_name='performers_director',
        on_delete=models.SET_NULL,
    )

    codirector = models.ForeignKey(
        'Role',
        null=True,
        blank=True,
        related_name='performers_codirector',
        on_delete=models.SET_NULL,
    )

    representing = TreeForeignKey(
        'Organization',
        related_name='performers',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # Denormalized
    seed = models.IntegerField(
        help_text="""
            The incoming rank based on prelim score.""",
        null=True,
        blank=True,
        editable=False,
    )

    prelim = models.FloatField(
        help_text="""
            The incoming prelim score.""",
        null=True,
        blank=True,
        editable=False,
    )

    rank = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    mus_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_points = models.IntegerField(
        null=True,
        editable=False,
        blank=True,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    total_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    total_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    session = models.ForeignKey(
        'Session',
        related_name='performers',
    )

    group = models.ForeignKey(
        'Group',
        related_name='performers',
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    # def clean(self):
    #     if self.singers.count() > 4:
    #         raise ValidationError('There can not be more than four persons in a quartet.')

    def save(self, *args, **kwargs):
        # NOTE Calls post-save signal on create.  Only way to do it with UUID
        self.name = " ".join(filter(None, [
            self.session.convention.organization.name,
            str(self.session.convention.get_division_display()),
            self.session.convention.get_season_display(),
            str(self.session.convention.year),
            self.session.get_kind_display(),
            "Performer",
            self.group.name,
        ]))

        super(Performer, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('group', 'session',),
        )

    class JSONAPIMeta:
        resource_name = "performer"

    def calculate(self):
        Score = apps.get_model('api', 'Score')
        scores = Score.objects.filter(
            song__performance__performer=self,
        ).exclude(
            kind=Score.KIND.practice,
        ).order_by(
            'category',
        ).values(
            'category',
        ).annotate(
            total=models.Sum('points'),
            average=models.Avg('points'),
        )
        for score in scores:
            if score['category'] == Score.CATEGORY.music:
                self.mus_points = score['total']
                self.mus_score = round(score['average'], 1)
            if score['category'] == Score.CATEGORY.presentation:
                self.prs_points = score['total']
                self.prs_score = round(score['average'], 1)
            if score['category'] == Score.CATEGORY.singing:
                self.sng_points = score['total']
                self.sng_score = round(score['average'], 1)

        # Calculate total points.
        try:
            self.total_points = sum([
                self.mus_points,
                self.prs_points,
                self.sng_points,
            ])
        except TypeError:
            self.total_points = None

        # Calculate total score.
        try:
            self.total_score = round(sum([
                self.mus_score,
                self.prs_score,
                self.sng_score,
            ]) / 3, 1)
        except TypeError:
            self.total_score = None

    def build(self):
        # TODO Future work for automated award mapping
        return

    def scratch(self):
        performances = self.performances.exclude(
            status=self.performances.model.STATUS.final,
        )
        for performance in performances:
            i = performance.slot
            performance.slot = -1
            performance.save()
            others = performance.round.performances.filter(
                slot__gt=i,
            ).order_by('slot')
            for other in others:
                other.slot -= 1
                other.save()
            performance.delete()
        self.status = self.STATUS.dropped
        self.save()
        return {'success': 'scratched'}

    def disqualify(self):
        performances = self.performances.exclude(
            status=self.performances.model.STATUS.final,
        )
        for performance in performances:
            i = performance.slot
            performance.slot = -1
            performance.save()
            others = performance.round.performances.filter(
                slot__gt=i,
            ).order_by('slot')
            for other in others:
                other.slot -= 1
                other.save()
        self.status = self.STATUS.disqualified
        self.save()
        return {'success': 'scratched'}


class Person(TimeStampedModel):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the resource.""",
        max_length=200,
        blank=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'inactive', 'Inactive',),
        (30, 'retired', 'Retired',),
        (40, 'deceased', 'Deceased',),
        (50, 'stix', 'Stix Issue',),
        (60, 'dup', 'Possible Duplicate',),
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    date = DateRangeField(
        help_text="""
            The active dates of the resource.""",
        null=True,
        blank=True,
    )

    location = models.CharField(
        help_text="""
            The geographical location of the resource.""",
        max_length=200,
        blank=True,
        default='',
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
        default='',
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
        default='',
    )

    phone = PhoneNumberField(
        help_text="""
            The phone number of the resource.  Include country code.""",
        blank=True,
        default='',
    )

    picture = models.ImageField(
        upload_to=generate_image_filename,
        help_text="""
            The picture/logo of the resource.""",
        blank=True,
        null=True,
    )

    description = models.TextField(
        help_text="""
            A description/bio of the resource.  Max 1000 characters.""",
        blank=True,
        max_length=1000,
    )

    notes = models.TextField(
        help_text="""
            Notes (for internal use only).""",
        blank=True,
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
    )

    bhs_id = models.IntegerField(
        null=True,
        blank=True,
        unique=True,
    )

    # Denormalization for searching
    common_name = models.CharField(
        max_length=255,
        blank=True,
        editable=False,
        default='',
    )

    # Denormalization for searching
    full_name = models.CharField(
        max_length=255,
        blank=True,
        editable=False,
        default='',
    )

    # Denormalization for searching
    formal_name = models.CharField(
        max_length=255,
        blank=True,
        editable=False,
        default='',
    )

    organization = TreeForeignKey(
        'Organization',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    chapter = models.ForeignKey(
        'Chapter',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    bhs_name = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_city = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_state = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_phone = models.CharField(
        max_length=255,
        blank=True,
    )

    bhs_email = models.EmailField(
        blank=True,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        name = HumanName(self.name)
        if name.nickname:
            self.common_name = " ".join(filter(None, [
                u"{0}".format(name.nickname),
                u"{0}".format(name.last),
                u"{0}".format(name.suffix),
            ]))
        else:
            self.common_name = u'{0}'.format(self.name)
        self.formal_name = " ".join(filter(None, [
            u'{0}'.format(name.first),
            u'{0}'.format(name.last),
            u'{0}'.format(name.suffix),
        ]))
        super(Person, self).save(*args, **kwargs)

    class JSONAPIMeta:
        resource_name = "person"

    @property
    def first_name(self):
        if self.name:
            name = HumanName(self.name)
            return name.first
        else:
            return None

    @property
    def last_name(self):
        if self.name:
            name = HumanName(self.name)
            return name.last
        else:
            return None

    @property
    def nick_name(self):
        if self.name:
            name = HumanName(self.name)
            return name.nickname
        else:
            return None


class Role(TimeStampedModel):
    """Quartet Relation."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'inactive', 'Inactive',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    PART = Choices(
        (1, 'tenor', 'Tenor'),
        (2, 'lead', 'Lead'),
        (3, 'baritone', 'Baritone'),
        (4, 'bass', 'Bass'),
        (5, 'director', 'Director'),
    )

    part = models.IntegerField(
        choices=PART,
    )

    date = DateRangeField(
        help_text="""
            Active Dates""",
        null=True,
        blank=True,
    )

    group = models.ForeignKey(
        'Group',
        related_name='roles',
    )

    person = models.ForeignKey(
        'Person',
        related_name='roles',
    )

    bhs_id = models.IntegerField(
        null=True,
        blank=True,
    )

    bhs_file = models.FileField(
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    # def clean(self):
    #     if all([
    #         self.performer.group.kind == Group.KIND.chorus,
    #         self.part != self.PART.director,
    #     ]):
    #         raise ValidationError('Choruses do not have quartet singers.')
    #     if all([
    #         self.performer.group.kind == Group.KIND.quartet,
    #         self.part == self.PART.director,
    #     ]):
    #         raise ValidationError('Quartets do not have directors.')
        # if self.part:
        #     if [s['part'] for s in self.performer.singers.values(
        #         'part'
        #     )].count(self.part) > 1:
        #         raise ValidationError('There can not be more than one of the same part in a quartet.')

    class JSONAPIMeta:
        resource_name = "role"

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.group.name,
            self.person.name,
            self.get_part_display(),
        ]))
        super(Role, self).save(*args, **kwargs)


class Round(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'built', 'Built',),
        (15, 'ready', 'Ready',),
        (20, 'started', 'Started',),
        (25, 'finished', 'Finished',),
        (28, 'ranked', 'Ranked',),
        (30, 'final', 'Final',),
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

    date = DateTimeRangeField(
        help_text="""
            The active dates of the resource.""",
        null=True,
        blank=True,
    )

    stix_name = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )

    mt = models.ForeignKey(
        'Group',
        related_name='mic_tester',
        null=True,
        blank=True,
    )

    session = models.ForeignKey(
        'Session',
        related_name='rounds',
    )

    class Meta:
        unique_together = (
            ('session', 'kind',),
        )

    class JSONAPIMeta:
        resource_name = "round"

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.session.convention.organization.name,
            str(self.session.convention.get_division_display()),
            self.session.convention.get_season_display(),
            self.session.get_kind_display(),
            self.get_kind_display(),
            str(self.session.convention.year),
        ]))
        super(Round, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"{0}".format(self.name)

    def draw(self):
        i = 1
        for performance in self.performances.order_by('?'):
            performance.slot = i
            performance.save()
            i += 1
        return {'success': 'drew {0} performances'.format(i)}

    def resort(self):
        i = 1
        if self.session.kind == self.session.KIND.chorus:
            duration = 10
            slack = 10
        else:
            duration = 10
            slack = 2
        cursor = None
        for performance in self.performances.order_by('slot'):
            if self.date:
                if not cursor:
                    cursor = (
                        self.date.lower,
                        self.date.lower + datetime.timedelta(minutes=duration),
                    )
                else:
                    cursor = (
                        cursor[1] + datetime.timedelta(minutes=slack),
                        cursor[1] + datetime.timedelta(minutes=(duration + slack))
                    )
                performance.scheduled = cursor
            performance.slot = i
            performance.save()
            i += 1
        return {'success': 'resorted {0} performances'.format(i)}

    def promote(self):
        for contest in self.session.contests.all():
            contest.rank()
        performers = self.session.performers.filter(
            contestants__contest__award__num_rounds=2,
            contestants__rank__lte=self.session.cutoff,
        )
        for performer in performers:
            obj = self.__class__.objects.get(
                session=self.session,
                num=self.num + 1,
            )
            self.performances.model.objects.create(
                round=obj,
                performer=performer,
            )

    @transition(field=status, source='*', target=STATUS.started)
    def start(self, *args, **kwargs):
        return

    @transition(field=status, source='*', target=STATUS.finished)
    def finish(self, *args, **kwargs):
        return


class Score(TimeStampedModel):
    """The Score is never released publicly.

    These are the actual Judge's scores.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (20, 'entered', 'Entered',),
        (30, 'flagged', 'Flagged',),
        (35, 'validated', 'Validated',),
        (40, 'confirmed', 'Confirmed',),
        (50, 'final', 'Final',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    song = models.ForeignKey(
        'Song',
        related_name='scores',
    )

    judge = models.ForeignKey(
        'Judge',
        related_name='scores',
    )

    CATEGORY = Choices(
        (1, 'music', 'Music'),
        (2, 'presentation', 'Presentation'),
        (3, 'singing', 'Singing'),
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

    dixon_test = models.NullBooleanField(
    )

    asterisk_test = models.NullBooleanField(
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

    class JSONAPIMeta:
        resource_name = "score"

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.id.hex,
        ]))
        super(Score, self).save(*args, **kwargs)


class Session(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (4, 'opened', 'Opened',),
        (8, 'closed', 'Closed',),
        (10, 'validated', 'Validated',),
        (20, 'started', 'Started',),
        # (25, 'ranked', 'Ranked',),
        (30, 'finished', 'Finished',),
        (40, 'drafted', 'Drafted',),
        (45, 'published', 'Published',),
        (50, 'final', 'Final',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    KIND = Choices(
        (1, 'quartet', 'Quartet',),
        (2, 'chorus', 'Chorus',),
        (10, 'seniors', 'Seniors',),
        (20, 'collegiate', 'Collegiate',),
        (30, 'youth', 'Youth',),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of session.  Generally this will be either quartet or chorus, with the exception being International and Midwinter which hold exclusive Collegiate and Senior sessions respectively.""",
        choices=KIND,
    )

    date = DateTimeRangeField(
        help_text="""
            The active dates of the session.""",
        null=True,
        blank=True,
    )

    administrator = models.ForeignKey(
        'Person',
        related_name='sessions_ca',
        null=True,
        blank=True,
    )

    aca = models.ForeignKey(
        'Person',
        related_name='sessions_aca',
        null=True,
        blank=True,
    )

    cutoff = models.IntegerField(
        null=True,
        blank=True,
    )

    scoresheet_pdf = models.FileField(
        help_text="""
            The historical PDF OSS.""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    entry_form = models.FileField(
        help_text="""
            The cj20 entry form.""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    song_list = models.FileField(
        help_text="""
            The cj20 song list.""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    convention = models.ForeignKey(
        'Convention',
        related_name='sessions',
    )

    cursor = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    @property
    def completed_rounds(self):
        return self.rounds.filter(status=self.rounds.model.STATUS.finished).count()

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.organization = self.convention.organization
        if self.convention.division:
            division = str(self.convention.get_division_display())
        else:
            division = None
        self.name = " ".join(filter(None, [
            self.convention.organization.name,
            division,
            self.convention.get_season_display(),
            self.get_kind_display(),
            "Session",
            str(self.convention.year),
        ]))
        super(Session, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('convention', 'kind',),
        )

    class JSONAPIMeta:
        resource_name = "session"

    @transition(field=status, source='*', target=STATUS.opened)
    def open(self, *args, **kwargs):
        return

    @transition(field=status, source='*', target=STATUS.closed)
    def close(self, *args, **kwargs):
        return

    @transition(field=status, source='*', target=STATUS.validated)
    def validate(self, *args, **kwargs):
        return

    @transition(field=status, source='*', target=STATUS.started)
    def start(self, *args, **kwargs):
        return

    @transition(field=status, source='*', target=STATUS.finished)
    def finish(self, *args, **kwargs):
        return

    # @transition(field=status, source='*', target=STATUS.drafted)
    # def draft(self, *args, **kwargs):
    #     for contest in self.contests.all():
    #         contest.rank()
    #     return

    @transition(field=status, source='*', target=STATUS.published)
    def publish(self, *args, **kwargs):
        return


class Submission(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    performer = models.ForeignKey(
        'Performer',
        related_name='submissions',
        on_delete=models.CASCADE,
    )

    chart = models.ForeignKey(
        'Chart',
        related_name='submissions',
        on_delete=models.CASCADE,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    class Meta:
        unique_together = (
            ('performer', 'chart',),
        )

    class JSONAPIMeta:
        resource_name = "submission"

    def save(self, *args, **kwargs):
        self.name = u"{0}".format(
            self.id.hex,
        )
        super(Submission, self).save(*args, **kwargs)


class Song(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        # (10, 'built', 'Built',),
        # (20, 'entered', 'Entered',),
        # (30, 'flagged', 'Flagged',),
        # (35, 'validated', 'Validated',),
        (40, 'confirmed', 'Confirmed',),
        (50, 'final', 'Final',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    ORDER = Choices(
        (1, 'first', 'First'),
        (2, 'second', 'Second'),
    )

    order = models.IntegerField(
        choices=ORDER,
    )

    is_parody = models.BooleanField(
        default=False,
    )

    # Denormalized values
    mus_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    total_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    total_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    chart = models.ForeignKey(
        'Chart',
        related_name='songs',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    performance = models.ForeignKey(
        'Performance',
        related_name='songs',
    )

    class Meta:
        unique_together = (
            ('performance', 'order',),
        )

    class JSONAPIMeta:
        resource_name = "song"

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.performance.round.session.convention.organization.name,
            str(self.performance.round.session.convention.get_division_display()),
            self.performance.round.session.convention.get_season_display(),
            self.performance.round.session.get_kind_display(),
            self.performance.round.get_kind_display(),
            str(self.performance.round.session.convention.year),
            "Performance",
            str(self.performance.slot),
            'Song',
            str(self.order),
            self.id.hex,
        ]))
        super(Song, self).save(*args, **kwargs)

    def calculate(self):
        Score = apps.get_model('api', 'Score')
        scores = Score.objects.filter(
            song=self,
        ).exclude(
            kind=Score.KIND.practice,
        ).order_by(
            'category',
        ).values(
            'category',
        ).annotate(
            total=models.Sum('points'),
            average=models.Avg('points'),
        )
        for score in scores:
            if score['category'] == Score.CATEGORY.music:
                self.mus_points = score['total']
                self.mus_score = round(score['average'], 1)
            if score['category'] == Score.CATEGORY.presentation:
                self.prs_points = score['total']
                self.prs_score = round(score['average'], 1)
            if score['category'] == Score.CATEGORY.singing:
                self.sng_points = score['total']
                self.sng_score = round(score['average'], 1)

        # Calculate total points.
        try:
            self.total_points = sum([
                self.mus_points,
                self.prs_points,
                self.sng_points,
            ])
        except TypeError:
            self.total_points = None

        # Calculate total score.
        try:
            self.total_score = round(sum([
                self.mus_score,
                self.prs_score,
                self.sng_score,
            ]) / 3, 1)
        except TypeError:
            self.total_score = None


class Venue(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=200,
        unique=True,
        editable=False,
    )

    location = models.CharField(
        max_length=255,
    )

    city = models.CharField(
        max_length=255,
    )

    state = models.CharField(
        max_length=255,
    )

    airport = models.CharField(
        max_length=3,
        null=True,
        blank=True,
    )

    timezone = TimeZoneField(
        help_text="""
            The local timezone of the venue.""",
        default='US/Pacific',
    )

    class JSONAPIMeta:
        resource_name = "venue"

    def save(self, *args, **kwargs):
        self.name = " ".join(filter(None, [
            self.location,
            " - ",
            "{0},".format(self.city),
            self.state,
        ]))
        super(Venue, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"{0}".format(self.name)


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    email = models.EmailField(
        unique=True,
        help_text="""Your email address will be your username.""",
    )
    name = models.CharField(
        max_length=200,
        help_text="""Your full name.""",
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )
    date_joined = models.DateField(
        auto_now_add=True,
    )

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    class JSONAPIMeta:
        resource_name = "user"
