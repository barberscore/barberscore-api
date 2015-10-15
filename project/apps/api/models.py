from __future__ import division

import logging
log = logging.getLogger(__name__)

import uuid

import os
import datetime
from django.db import (
    models,
)

from autoslug import AutoSlugField

from django.core.validators import (
    RegexValidator,
    MaxValueValidator,
    MinValueValidator,
)

from django.core.exceptions import (
    ValidationError,
)

from model_utils.models import (
    TimeFramedModel,
    TimeStampedModel,
)

from model_utils import Choices

from timezone_field import TimeZoneField

from phonenumber_field.modelfields import PhoneNumberField

from nameparser import HumanName

from .validators import (
    validate_trimmed,
)


def generate_image_filename(instance, filename):
    f, ext = os.path.splitext(filename)
    return '{0}{1}'.format(instance.id, ext)


class Common(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the resource.""",
        max_length=200,
        unique=True,
        validators=[
            validate_trimmed,
        ],
        error_messages={
            'unique': 'The name must be unique.  Add middle initials, suffixes, years, or other identifiers to make the name unique.',
        }
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    start = models.DateField(
        help_text="""
            The founding/birth date of the resource.""",
        blank=True,
        null=True,
    )

    end = models.DateField(
        help_text="""
            The retirement/deceased date of the resource.""",
        blank=True,
        null=True,
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

    is_active = models.BooleanField(
        help_text="""
            A boolean for active/living resources.""",
        default=True,
    )

    class Meta:
        abstract = True


class Person(Common):

    KIND = Choices(
        (1, 'individual', "Individual"),
        (2, 'team', "Team"),
    )

    kind = models.IntegerField(
        help_text="""
            Most persons are individuals; however, they can be grouped into teams for the purpose of multi-arranger songs.""",
        choices=KIND,
        default=KIND.individual,
    )

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u"{0}".format(self.name)

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

    fuzzy = models.TextField(
        blank=True,
    )


class Group(Common):

    KIND = Choices(
        (1, 'quartet', 'Quartet'),
        (2, 'chorus', 'Chorus'),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of group; choices are Quartet or Chorus.""",
        choices=KIND,
        default=KIND.quartet,
    )

    chapter_name = models.CharField(
        help_text="""
            The chapter name (only for choruses).""",
        max_length=200,
        blank=True,
    )

    chapter_code = models.CharField(
        help_text="""
            The chapter code (only for choruses).""",
        max_length=200,
        blank=True,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def clean(self):
        if self.kind == self.KIND.quartet and self.chapter_name:
            raise ValidationError(
                {'chapter_name': 'Chapter names are only for choruses.'}
            )
        if self.kind == self.KIND.quartet and self.chapter_code:
            raise ValidationError(
                {'chapter_code': 'Chapter codes are only for choruses.'}
            )

    class Meta:
        ordering = (
            'name',
        )

    fuzzy = models.TextField(
        blank=True,
    )


class Judge(models.Model):
    """Contest Judge"""

    STATUS = Choices(
        (0, 'new', 'New',),
    )

    PART = Choices(
        (1, 'music', 'Music'),
        (2, 'presentation', 'Presentation'),
        (3, 'singing', 'Singing'),
        (4, 'administrator', 'Administrator'),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    contest = models.ForeignKey(
        'Contest',
        related_name='judges',
    )

    person = models.ForeignKey(
        'Person',
        related_name='contests',
        null=True,
        on_delete=models.SET_NULL,
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    part = models.IntegerField(
        choices=PART,
    )

    num = models.IntegerField(
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2:02d}".format(
            self.contest,
            self.get_part_display(),
            self.num,
        )
        super(Judge, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('contest', 'part', 'num'),
        )
        ordering = (
            'contest',
            'part',
            'num',
        )


class Singer(models.Model):
    """Quartet Relation"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    PART = Choices(
        (1, 'tenor', 'Tenor'),
        (2, 'lead', 'Lead'),
        (3, 'baritone', 'Baritone'),
        (4, 'bass', 'Bass'),
    )

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    contestant = models.ForeignKey(
        'Contestant',
        related_name='singers',
    )

    person = models.ForeignKey(
        'Person',
        related_name='quartets',
    )

    part = models.IntegerField(
        choices=PART,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2}".format(
            self.contestant,
            self.get_part_display(),
            self.person,
        )
        super(Singer, self).save(*args, **kwargs)

    def clean(self):
        # if self.contestant.group.kind == Group.CHORUS:
        #     raise ValidationError('Choruses do not have quartet singers.')
        if self.part:
            if [s['part'] for s in self.contestant.singers.values(
                'part'
            )].count(self.part) > 1:
                raise ValidationError('There can not be more than one of the same part in a quartet.')

    class Meta:
        unique_together = (
            ('contestant', 'person',),
        )
        ordering = (
            '-name',
        )


class Director(models.Model):
    """Chorus relation"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    PART = Choices(
        (1, 'director', 'Director'),
        (2, 'codirector', 'Co-Director'),
    )

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    contestant = models.ForeignKey(
        'Contestant',
        related_name='directors',
    )

    person = models.ForeignKey(
        'Person',
        related_name='choruses',
    )

    part = models.IntegerField(
        choices=PART,
        default=PART.director,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2}".format(
            self.contestant,
            self.get_part_display(),
            self.person,
        )
        super(Director, self).save(*args, **kwargs)

    def clean(self):
        if self.contestant.group.kind == Group.KIND.quartet:
            raise ValidationError('Quartets do not have directors.')

    class Meta:
        unique_together = (
            ('contestant', 'person',),
        )


class Song(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=200,
        unique=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u"{0}".format(self.name)

    fuzzy = models.TextField(
        blank=True,
    )


class Arrangement(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    TEMPO = Choices(
        (1, "Ballad"),
        (2, "Uptune"),
        (3, "Mixed"),
    )

    DIFFICULTY = Choices(
        (1, "Very Easy"),
        (2, "Easy"),
        (3, "Medium"),
        (4, "Hard"),
        (5, "Very Hard"),
    )

    bhs_id = models.IntegerField(
        null=True,
        blank=True,
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

    bhs_difficulty = models.IntegerField(
        null=True,
        blank=True,
        choices=DIFFICULTY
    )

    bhs_tempo = models.IntegerField(
        null=True,
        blank=True,
        choices=TEMPO,
    )

    bhs_medley = models.BooleanField(
        default=False,
    )

    is_parody = models.BooleanField(
        default=False,
    )

    is_medley = models.BooleanField(
        default=False,
    )

    song = models.ForeignKey(
        'Song',
        null=True,
        blank=True,
        related_name='arrangements',
    )

    arranger = models.ForeignKey(
        'Person',
        null=True,
        blank=True,
        related_name='arrangements',
    )

    song_match = models.CharField(
        blank=True,
        max_length=200,
    )

    name = models.CharField(
        max_length=200,
        unique=True,
    )

    person_match = models.CharField(
        blank=True,
        max_length=200,
    )

    fuzzy = models.TextField(
        blank=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    class Meta:
        unique_together = (
            ('arranger', 'song')
        )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} [{1}]".format(
            self.song,
            self.arranger,
        )
        super(Arrangement, self).save(*args, **kwargs)


class Award(models.Model):

    KIND = Choices(
        (1, 'first', 'First Place Gold Medalist'),
        (2, 'second', 'Second Place Silver Medalist'),
        (3, 'third', 'Third Place Bronze Medalist'),
        (4, 'fourth', 'Fourth Place Bronze Medalist'),
        (5, 'fifth', 'Fifth Place Bronze Medalist'),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    kind = models.IntegerField(
        choices=KIND,
    )

    contestant = models.ForeignKey(
        'Contestant',
        related_name='awards',
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1}".format(
            self.contestant,
            self.get_kind_display(),
        )
        super(Award, self).save(*args, **kwargs)

    class Meta:
        ordering = (
            'name',
        )

        unique_together = (
            ('kind', 'contestant',),
        )


class District(Common):
    KIND = Choices(
        (0, 'bhs', "BHS"),
        (1, 'district', "District"),
        (2, 'affiliate', "Affiliate"),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of District.  Choices are BHS (International), District, and Affiliate.""",
        choices=KIND,
        default=KIND.bhs,
    )

    long_name = models.CharField(
        help_text="""
            A long-form name for the resource.""",
        blank=True,
        max_length=200,
    )

    class Meta:
        ordering = [
            'kind',
            'name',
        ]

    def __unicode__(self):
        return u"{0}".format(self.name)


class Convention(TimeFramedModel):
    KIND = Choices(
        (1, 'international', 'International',),
        (2, 'midwinter', 'Midwinter',),
        (3, 'fall', 'Fall',),
        (4, 'spring', 'Spring',),
        (5, 'pacific', 'Pacific',),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the convention (determined programmatically.)""",
        max_length=200,
        unique=True,
    )

    kind = models.IntegerField(
        help_text="""
            The kind of convention.""",
        choices=KIND,
    )

    year = models.IntegerField(
        default=datetime.datetime.now().year,
        validators=[
            MaxValueValidator(
                2016,
                message='Year must be between 1939 and 2016',
            ),
            MinValueValidator(
                1938,
                message='Year must be between 1939 and 2016',
            ),
        ]
    )

    district = models.ForeignKey(
        'District',
        help_text="""
            The district for the convention.  If International, this is 'BHS'.""",
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    dates = models.CharField(
        help_text="""
            The convention dates (will be replaced by start/end).""",
        max_length=200,
        blank=True,
    )

    location = models.CharField(
        help_text="""
            The location of the convention.""",
        max_length=200,
        blank=True,
    )

    timezone = TimeZoneField(
        help_text="""
            The local timezone of the convention.""",
        default='US/Pacific',
    )

    is_active = models.BooleanField(
        help_text="""
            A global boolean that controls if the resource is accessible via the API""",
        default=False,
    )

    class Meta:
        ordering = [
            'district',
            '-year',
        ]

        unique_together = (
            ('district', 'kind', 'year',),
        )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        if self.kind in [
            self.KIND.international,
            self.KIND.midwinter,
            self.KIND.pacific,
        ]:
            self.name = u"{0} {1}".format(
                self.get_kind_display(),
                self.get_year_display(),
            )
        else:
            self.name = u"{0} {1} {2}".format(
                self.district,
                self.get_kind_display(),
                self.get_year_display(),
            )
        super(Convention, self).save(*args, **kwargs)


class Contest(models.Model):

    STATUS = Choices(
        (0, 'new', 'New',),
        (1, 'upcoming', 'Upcoming',),
        (2, 'current', 'Current',),
        (3, 'reviewing', 'Reviewing',),
        (4, 'complete', 'Complete',),
    )

    KIND = Choices(
        (1, 'quartet', 'Quartet',),
        (2, 'chorus', 'Chorus',),
        (3, 'senior', 'Senior',),
        (4, 'collegiate', 'Collegiate',),
    )

    LEVEL = Choices(
        (1, 'international', "International"),
        # (2, 'district', "District"),
        # (4, 'prelims', "Prelims"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    name = models.CharField(
        help_text="""
            The name of the contest (determined programmatically.)""",
        max_length=200,
        unique=True,
    )

    level = models.IntegerField(
        help_text="""
            The level of the contest (currently only International is supported.)""",
        choices=LEVEL,
        default=LEVEL.international,
    )

    kind = models.IntegerField(
        help_text="""
            The kind of the contest (quartet, chorus, senior, collegiate.)""",
        choices=KIND,
        default=KIND.quartet,
    )

    year = models.IntegerField(
        default=datetime.datetime.now().year,
        validators=[
            MaxValueValidator(
                2016,
                message='Year must be between 1939 and 2016',
            ),
            MinValueValidator(
                1938,
                message='Year must be between 1939 and 2016',
            ),
        ]
    )

    district = models.ForeignKey(
        'District',
        related_name='contests',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    convention = models.ForeignKey(
        'Convention',
        help_text="""
            The convention at which this contest occurred.""",
        related_name='contests',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    panel = models.IntegerField(
        help_text="""
            Size of the judging panel (typically three or five.)""",
        default=5,
    )

    scoresheet_pdf = models.FileField(
        help_text="""
            PDF of the OSS.""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    scoresheet_csv = models.FileField(
        help_text="""
            The parsed scoresheet (used for legacy imports).""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        help_text="""
            A global boolean that controls if the resource is accessible via the API""",
        default=False,
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    class Meta:
        unique_together = (
            ('level', 'kind', 'year', 'district',),
        )
        ordering = (
            'level',
            '-year',
            'kind',
        )

    def clean(self):
            if self.level == self.LEVEL.international and self.district != 'BHS':
                raise ValidationError('International does not have a district.')
            if self.level != self.LEVEL.international and self.district is None:
                raise ValidationError('You must provide a district.')
            if self.year != self.convention.year:
                raise ValidationError("The contest should be the same year as the convention.")

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        if self.level == self.LEVEL.international:
            self.name = u"{0} {1} {2}".format(
                self.get_level_display(),
                self.get_kind_display(),
                self.get_year_display(),
            )
        elif self.level == self.LEVEL.prelims:
            self.name = u"{0} {1} {2}".format(
                self.district,
                self.get_level_display(),
                self.get_year_display(),
            )
        else:
            self.name = u"{0} {1} {2}".format(
                self.district,
                self.get_kind_display(),
                self.get_year_display(),
            )
        super(Contest, self).save(*args, **kwargs)

    def prep_panel(self):
        """
            Return sentinels for juding panel.
        """
        pass

    def place_quarters(self):
        if self.kind != self.KIND.quartet:
            return
        marker = []
        i = 1
        for contestant in self.contestants.order_by('-quarters_points'):
            try:
                match = contestant.quarters_points == marker[0].quarters_points
            except IndexError:
                contestant.quarters_place = i
                contestant.save()
                marker.append(contestant)
                continue
            if match:
                contestant.quarters_place = i
                i += len(marker)
                contestant.save()
                marker.append(contestant)
                continue
            else:
                i += 1
                contestant.quarters_place = i
                contestant.save()
                marker = [contestant]
        return

    def place_semis(self):
        if self.kind != self.KIND.quartet:
            return
        marker = []
        i = 1
        for contestant in self.contestants.order_by('-semis_points'):
            try:
                match = contestant.semis_points == marker[0].semis_points
            except IndexError:
                contestant.semis_place = i
                contestant.save()
                marker.append(contestant)
                continue
            if match:
                contestant.semis_place = i
                i += len(marker)
                contestant.save()
                marker.append(contestant)
                continue
            else:
                i += 1
                contestant.semis_place = i
                contestant.save()
                marker = [contestant]
        return

    def place_finals(self):
        if self.kind != self.KIND.quartet:
            return
        marker = []
        i = 1
        for contestant in self.contestants.order_by('-finals_points'):
            try:
                match = contestant.finals_points == marker[0].finals_points
            except IndexError:
                contestant.finals_place = i
                contestant.save()
                marker.append(contestant)
                continue
            if match:
                contestant.finals_place = i
                i += len(marker)
                contestant.save()
                marker.append(contestant)
                continue
            else:
                i += 1
                contestant.finals_place = i
                contestant.save()
                marker = [contestant]
        return

    def seed(self):
        marker = []
        i = 1
        for contestant in self.contestants.order_by('-prelim'):
            try:
                match = contestant.prelim == marker[0].prelim
            except IndexError:
                contestant.seed = i
                contestant.save()
                marker.append(contestant)
                continue
            if match:
                contestant.seed = i
                i += len(marker)
                contestant.save()
                marker.append(contestant)
                continue
            else:
                i += 1
                contestant.seed = i
                contestant.save()
                marker = [contestant]
        return


class Contestant(TimeFramedModel):

    STATUS = Choices(
        (0, 'new', 'New',),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    contest = models.ForeignKey(
        'Contest',
        related_name='contestants',
    )

    group = models.ForeignKey(
        'Group',
        related_name='contestants',
    )

    district = models.ForeignKey(
        'District',
        help_text="""
            The district this contestant is representing.""",
        related_name='contestants',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    picture = models.ImageField(
        help_text="""
            The performance picture (as opposed to the "official" photo).""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    seed = models.IntegerField(
        help_text="""
            The incoming rank based on prelim score.""",
        null=True,
        blank=True,
    )

    prelim = models.FloatField(
        help_text="""
            The incoming prelim score.""",
        null=True,
        blank=True,
    )

    # Should make this a property or denorm it.
    draw = models.IntegerField(
        help_text="""
            The OA (Order of Appearance) in the contest schedule.  Specific to each round/session.""",
        null=True,
        blank=True,
    )

    # Should make this a property or denorm it.
    stagetime = models.DateTimeField(
        help_text="""
            The estimated stagetime (may be replaced by 'start' in later versions).""",
        null=True,
        blank=True,
    )

    # TODO Everything below here must be protected in some way.  Different model?

    points = models.IntegerField(
        help_text="""
            Total raw points for this contestant (cumuative).""",
        null=True,
        blank=True,
    )

    score = models.FloatField(
        help_text="""
            The percentile of the total points (cumulative , all rounds).""",
        null=True,
        blank=True,
    )

    place = models.IntegerField(
        help_text="""
            The final placement/rank of the contestant.""",
        null=True,
        blank=True,
    )

    men = models.IntegerField(
        help_text="""
            The number of men on stage (only for chourses).""",
        null=True,
        blank=True,
    )

    quarters_points = models.IntegerField(
        help_text="""
            The total points for the quarterfinal round/session.""",
        null=True,
        blank=True,
    )

    semis_points = models.IntegerField(
        help_text="""
            The total points for the semifinal round/session.""",
        null=True,
        blank=True,
    )

    finals_points = models.IntegerField(
        help_text="""
            The total points for the final round/session.""",
        null=True,
        blank=True,
    )

    quarters_score = models.FloatField(
        help_text="""
            The percential score for the quarterfinal round/session.""",
        null=True,
        blank=True,
    )

    semis_score = models.FloatField(
        help_text="""
            The percential score for the semifinal round/session.""",
        null=True,
        blank=True,
    )

    finals_score = models.FloatField(
        help_text="""
            The percential score for the final round/session.""",
        null=True,
        blank=True,
    )

    quarters_place = models.IntegerField(
        help_text="""
            The place for the quarterfinal round/session.  This is for the quarters only and is NOT cumulative.""",
        null=True,
        blank=True,
    )

    semis_place = models.IntegerField(
        help_text="""
            The place for the semifinal round/session.  This is for the semis only and is NOT cumulative.""",
        null=True,
        blank=True,
    )

    finals_place = models.IntegerField(
        help_text="""
            The place for the fainal round/session.  This is for the finals only and is NOT cumulative.""",
        null=True,
        blank=True,
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    def save(self, *args, **kwargs):
        self.name = u"{0} {1}".format(
            self.contest,
            self.group,
        )
        self.finals_points = self.performances.filter(
            round=1,
        ).aggregate(sum=models.Sum('total_points'))['sum']
        self.semis_points = self.performances.filter(
            round=2,
        ).aggregate(sum=models.Sum('total_points'))['sum']
        self.quarters_points = self.performances.filter(
            round=3,
        ).aggregate(sum=models.Sum('total_points'))['sum']
        self.points = sum(filter(None, [
            self.quarters_points,
            self.semis_points,
            self.finals_points,
        ])) or None
        panel = self.contest.panel
        if self.quarters_points:
            self.quarters_score = round(self.quarters_points / (panel * 6), 1)
        if self.semis_points:
            self.semis_score = round(self.semis_points / (panel * 6), 1)
        if self.finals_points:
            self.finals_score = round(self.finals_points / (panel * 6), 1)
        super(Contestant, self).save(*args, **kwargs)

    @property
    def delta_score(self):
        try:
            return self.score - self.prelim
        except TypeError:
            return None

    @property
    def delta_place(self):
        try:
            return self.seed - self.place
        except TypeError:
            return None

    def __unicode__(self):
        return u"{0}".format(self.name)

    class Meta:
        ordering = (
            '-contest__year',
            'place',
            '-score',
        )
        unique_together = (
            ('group', 'contest',),
        )

    def clean(self):
        if self.singers.count() > 4:
            raise ValidationError('There can not be more than four persons in a quartet.')


class Slot(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    KIND = Choices(
        (1, 'finals', 'Finals'),
        (2, 'semis', 'Semis'),
        (3, 'quarters', 'Quarters'),
    )

    STATUS = Choices(
        (0, 'new', 'New',),
    )

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    contestant = models.ForeignKey(
        'Contestant',
        related_name='sessions',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    contest = models.ForeignKey(
        'Contest',
        related_name='sessions',
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    kind = models.IntegerField(
        choices=KIND,
        default=KIND.finals,
    )

    draw = models.IntegerField(
        help_text="""
            The OA (Order of Appearance) in the contest schedule.  Specific to each round/session.""",
    )

    stagetime = models.DateTimeField(
        help_text="""
            The estimated stagetime (may be replaced by 'start' in later versions).""",
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2:02d}".format(
            self.contest,
            self.get_kind_display(),
            self.draw,
        )
        super(Slot, self).save(*args, **kwargs)

    # class Meta:
        # unique_together = (
        #     ('contest', 'kind', 'draw'),
        # )


class Performance(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
    )

    ROUND = Choices(
        (1, 'finals', 'Finals'),
        (2, 'semis', 'Semis'),
        (3, 'quarters', 'Quarters'),
    )

    ORDER = Choices(
        (1, 'first', 'First'),
        (2, 'second', 'Second'),
    )

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    contest = models.ForeignKey(
        'Contest',
        related_name='performances',
        null=True,
        blank=True,
    )

    contestant = models.ForeignKey(
        'Contestant',
        related_name='performances',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    round = models.IntegerField(
        choices=ROUND,
    )

    order = models.IntegerField(
        choices=ORDER,
    )

    draw = models.IntegerField(
        help_text="""
            The OA (Order of Appearance) in the contest schedule.  Specific to each round/session.""",
        null=True,
        blank=True,
    )

    stagetime = models.DateTimeField(
        help_text="""
            The estimated stagetime (may be replaced by 'start' in later versions).""",
        null=True,
        blank=True,
    )

    is_parody = models.BooleanField(
        default=False,
    )

    arrangement = models.ForeignKey(
        'Arrangement',
        related_name='performances',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # The following need to be protected until released.
    # Different model?

    mus_points = models.IntegerField(
        help_text="""
            The total music points for this performance.""",
        null=True,
        blank=True,
    )

    prs_points = models.IntegerField(
        help_text="""
            The total presentation points for this performance.""",
        null=True,
        blank=True,
    )

    sng_points = models.IntegerField(
        help_text="""
            The total singing points for this performance.""",
        null=True,
        blank=True,
    )

    total_points = models.IntegerField(
        help_text="""
            The total points for this performance.""",
        null=True,
        blank=True,
    )

    mus_score = models.FloatField(
        help_text="""
            The percentile music score for this performance.""",
        null=True,
        blank=True,
    )

    prs_score = models.FloatField(
        help_text="""
            The percentile presentation score for this performance.""",
        null=True,
        blank=True,
    )

    sng_score = models.FloatField(
        help_text="""
            The percentile singing score for this performance.""",
        null=True,
        blank=True,
    )

    total_score = models.FloatField(
        help_text="""
            The total percentile score for this performance.""",
        null=True,
        blank=True,
    )

    penalty = models.TextField(
        help_text="""
            Free form for penalties (notes).""",
        blank=True,
    )

    class Meta:
        ordering = [
            'contestant',
            'round',
            'order',
        ]
        unique_together = (
            ('contestant', 'round', 'order',),
        )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2} {3}".format(
            self.contestant,
            self.get_round_display(),
            "Song",
            self.get_order_display(),
        )
        self.total_points = sum(filter(None, [
            self.mus_points,
            self.prs_points,
            self.sng_points,
        ])) or None
        panel = self.contestant.contest.panel
        if self.scores.exists():
            self.mus_points = self.scores.filter(
                category=1,  # TODO how does ModelUtils handle?
            ).aggregate(mp=models.Sum('points'))['mp']
            self.prs_points = self.scores.filter(
                category=2,  # TODO how does ModelUtils handle?
            ).aggregate(mp=models.Sum('points'))['mp']
            self.sng_points = self.scores.filter(
                category=3,  # TODO how does ModelUtils handle?
            ).aggregate(mp=models.Sum('points'))['mp']
        if self.mus_points:
            self.mus_score = round(self.mus_points / panel, 1)
        if self.prs_points:
            self.prs_score = round(self.prs_points / panel, 1)
        if self.sng_points:
            self.sng_score = round(self.sng_points / panel, 1)
        if self.total_points:
            self.total_score = round(self.total_points / (panel * 3), 1)
        super(Performance, self).save(*args, **kwargs)


class Score(models.Model):
    """
        The Score is never released publicly.  These are the actual
        Judge's scores from the contest.
    """
    STATUS = Choices(
        (0, 'new', 'New',),
    )

    CATEGORY = Choices(
        (1, 'music', "Music"),
        (2, 'presentation', "Presentation"),
        (3, 'singing', "Singing"),
        (4, 'admin', "Admin"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    performance = models.ForeignKey(
        'Performance',
        related_name='scores',
    )

    judge = models.ForeignKey(
        'Judge',
        related_name='scores',
    )

    points = models.IntegerField(
        help_text="""
            The number of points awarded (0-100)""",
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

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    category = models.IntegerField(
        choices=CATEGORY,
    )

    is_practice = models.BooleanField(
        default=False,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2} {3}".format(
            self.performance,
            self.judge.person.name,
            self.get_category_display(),
            self.points,
        )
        super(Score, self).save(*args, **kwargs)


class Event(TimeFramedModel):
    KIND = Choices(
        (
            'Session', [
                (1, 'finals', 'Finals'),
                (2, 'semis', 'Semis'),
                (3, 'quarters', 'Quarters'),
            ]
        ), (
            'Other', [
                (4, 'other', 'Other',),
            ]
        )
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the event (determined programmatically.)""",
        max_length=200,
        unique=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    convention = models.ForeignKey(
        'Convention',
        help_text="""
            The convention at which this event occurs.""",
        related_name='events',
    )

    contest = models.ForeignKey(
        'Contest',
        help_text="""
            The contest associated with this event.""",
        related_name='events',
        null=True,
        on_delete=models.SET_NULL,
    )

    contestant = models.ForeignKey(
        'Contestant',
        help_text="""
            The contestant associated with this event.""",
        related_name='events',
        null=True,
        on_delete=models.SET_NULL,
    )

    draw = models.IntegerField(
        help_text="""
            The OA (Order of Appearance) in the contest schedule.  Specific to each round/session.""",
        null=True,
        blank=True,
    )

    kind = models.IntegerField(
        help_text="""
            The kind of event.""",
        choices=KIND,
    )

    location = models.CharField(
        help_text="""
            The location of the event.""",
        max_length=200,
        blank=True,
    )

    is_active = models.BooleanField(
        help_text="""
            A global boolean that controls if the resource is accessible via the API""",
        default=False,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0}".format(
            self.id,
        )
        super(Event, self).save(*args, **kwargs)


class DuplicateGroup(models.Model):
    parent = models.ForeignKey(
        Group,
        related_name='duplicates',
    )
    child = models.ForeignKey(
        Group,
        related_name='children',
    )
    score = models.IntegerField(
    )


class DuplicateSong(models.Model):
    parent = models.ForeignKey(
        Song,
        related_name='duplicates',
    )
    child = models.ForeignKey(
        Song,
        related_name='children',
    )
    score = models.IntegerField(
    )


class DuplicatePerson(models.Model):
    parent = models.ForeignKey(
        Person,
        related_name='duplicates',
    )
    child = models.ForeignKey(
        Person,
        related_name='children',
    )
    score = models.IntegerField(
    )
