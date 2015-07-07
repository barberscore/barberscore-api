from __future__ import division

import logging
log = logging.getLogger(__name__)

import uuid

import csv
import os
import datetime
from django.db import (
    models,
)

from autoslug import AutoSlugField

from django.core.validators import (
    RegexValidator,
)

from django.core.exceptions import (
    ValidationError,
)

from timezone_field import TimeZoneField

from phonenumber_field.modelfields import PhoneNumberField

from nameparser import HumanName


def generate_image_filename(instance, filename):
    f, ext = os.path.splitext(filename)
    return '{0}{1}'.format(instance.id, ext)


class Common(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the resource.  Must be unique.  If there are singer name conflicts, please add middle initial, nickname, or other identifying information.""",
        max_length=200,
        unique=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
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
        null=True,
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
        null=True,
    )

    class Meta:
        abstract = True


class Person(Common):

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

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


class Group(Common):

    QUARTET = 1
    CHORUS = 2

    KIND_CHOICES = (
        (QUARTET, "Quartet"),
        (CHORUS, "Chorus"),
    )

    awards = models.ManyToManyField(
        'Award',
        through='GroupAward',
        related_name='groups',
    )

    kind = models.IntegerField(
        choices=KIND_CHOICES,
        default=QUARTET,
    )

    director = models.ForeignKey(
        'Person',
        related_name='groups',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    lead = models.ForeignKey(
        'Person',
        related_name='groups_lead',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    tenor = models.ForeignKey(
        'Person',
        related_name='groups_tenor',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    baritone = models.ForeignKey(
        'Person',
        related_name='groups_baritone',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    bass = models.ForeignKey(
        'Person',
        related_name='groups_bass',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    chapter_name = models.CharField(
        help_text="""
            The name of the director(s) of the chorus.""",
        max_length=200,
        blank=True,
        null=True,
    )

    chapter_code = models.CharField(
        help_text="""
            The code of the director(s) of the chorus.""",
        max_length=200,
        blank=True,
    )

    is_active = models.BooleanField(
        default=False,
    )

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            self.director = self.contestants.order_by('contest__year').last().director
        except AttributeError:
            self.director = None
        try:
            self.tenor = self.contestants.order_by('contest__year').last().tenor
        except AttributeError:
            self.tenor = None
        try:
            self.lead = self.contestants.order_by('contest__year').last().lead
        except AttributeError:
            self.lead = None
        try:
            self.baritone = self.contestants.order_by('contest__year').last().baritone
        except AttributeError:
            self.baritone = None
        try:
            self.bass = self.contestants.order_by('contest__year').last().bass
        except AttributeError:
            self.bass = None
        super(Group, self).save(*args, **kwargs)

    class Meta:
        ordering = (
            'name',
        )


class District(Common):
    BHS = 0
    DISTRICT = 1
    AFFILIATE = 2

    KIND_CHOICES = (
        (BHS, "BHS"),
        (DISTRICT, "District"),
        (AFFILIATE, "Affiliate"),
    )

    long_name = models.CharField(
        null=True,
        blank=True,
        max_length=200,
    )

    kind = models.IntegerField(
        choices=KIND_CHOICES,
        default=BHS,
    )

    class Meta:
        ordering = [
            'kind',
            'name',
        ]

    def __unicode__(self):
        return self.name


class Convention(models.Model):
    YEAR_CHOICES = []
    for r in reversed(range(1939, (datetime.datetime.now().year + 1))):
        YEAR_CHOICES.append((r, r))

    INTERNATIONAL = 1
    MIDWINTER = 2
    FALL = 3
    SPRING = 4
    PACIFIC = 5

    KIND_CHOICES = (
        (INTERNATIONAL, 'International',),
        (MIDWINTER, 'Midwinter',),
        (FALL, 'Fall',),
        (SPRING, 'Spring',),
        (PACIFIC, 'Pacific',),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the convention.""",
        max_length=200,
        unique=True,
    )

    kind = models.IntegerField(
        choices=KIND_CHOICES,
        null=True,
        blank=True,
    )

    year = models.IntegerField(
        choices=YEAR_CHOICES,
        default=datetime.datetime.now().year,
        null=True,
        blank=True,
    )

    district = models.ForeignKey(
        'District',
        null=True,
        blank=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
    )

    dates = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    location = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    timezone = TimeZoneField(
        default='US/Pacific',
    )

    is_active = models.BooleanField(
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
        return self.name

    def save(self, *args, **kwargs):
        if self.kind in [
            self.INTERNATIONAL,
            self.MIDWINTER,
            self.PACIFIC,
        ]:
            self.name = "{0} {1}".format(
                self.get_kind_display(),
                self.get_year_display(),
            )
        else:
            self.name = "{0} {1} {2}".format(
                self.district,
                self.get_kind_display(),
                self.get_year_display(),
            )
        super(Convention, self).save(*args, **kwargs)


class Contest(models.Model):

    YEAR_CHOICES = []
    for r in reversed(range(1939, (datetime.datetime.now().year + 1))):
        YEAR_CHOICES.append((r, r))

    QUARTET = 1
    CHORUS = 2
    SENIOR = 3
    COLLEGIATE = 4

    KIND_CHOICES = (
        (QUARTET, 'Quartet',),
        (CHORUS, 'Chorus',),
        (SENIOR, 'Senior',),
        (COLLEGIATE, 'Collegiate',),
    )

    INTERNATIONAL = 1
    DISTRICT = 2
    REGIONAL = 3
    PRELIMS = 4

    LEVEL_CHOICES = (
        (INTERNATIONAL, "International"),
        (DISTRICT, "District"),
        (REGIONAL, "Regional"),
        (PRELIMS, "Prelims"),
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
    )

    name = models.CharField(
        max_length=200,
        unique=True,
    )

    level = models.IntegerField(
        choices=LEVEL_CHOICES,
        default=INTERNATIONAL,
    )

    kind = models.IntegerField(
        choices=KIND_CHOICES,
        default=QUARTET,
    )

    year = models.IntegerField(
        choices=YEAR_CHOICES,
        default=datetime.datetime.now().year,
    )

    district = models.ForeignKey(
        'District',
        null=True,
        blank=True,
    )

    convention = models.ForeignKey(
        'Convention',
        related_name='contests',
        null=True,
        blank=True,
    )

    panel = models.IntegerField(
        help_text="""
            Size of the judging panel (typically
            three or five.)""",
        default=5,
    )

    scoresheet_pdf = models.FileField(
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    scoresheet_csv = models.FileField(
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=False,
    )

    is_complete = models.BooleanField(
        default=False,
    )

    is_place = models.BooleanField(
        default=False,
    )

    # is_score = models.BooleanField(
    #     default=False,
    # )

    class Meta:
        unique_together = (
            ('level', 'kind', 'year', 'district',),
        )
        ordering = (
            'level',
            '-year',
            'kind',
        )

    @property
    def is_score(self):
        if self.year > 1993:
            return True
        else:
            return False

    def clean(self):
            if self.level == self.INTERNATIONAL and self.district is not None:
                raise ValidationError('International does not have a district.')
            if self.level != self.INTERNATIONAL and self.district is None:
                raise ValidationError('You must provide a district.')
            if self.year != self.convention.year:
                raise ValidationError("The contest should be the same year as the convention.")

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.level == self.INTERNATIONAL:
            self.name = "{0} {1} {2}".format(
                self.get_level_display(),
                self.get_kind_display(),
                self.get_year_display(),
            )
        elif self.level == self.PRELIMS:
            self.name = "{0} {1} {2}".format(
                self.district,
                self.get_level_display(),
                self.get_year_display(),
            )
        else:
            self.name = "{0} {1} {2}".format(
                self.district,
                self.get_kind_display(),
                self.get_year_display(),
            )
        super(Contest, self).save(*args, **kwargs)

    def import_legacy(self):
        reader = csv.reader(self.scoresheet_csv)
        # next(reader)
        data = [row for row in reader]

        mappings = {
            'The Westminster Chorus': 'Westminster',
            'Southern Gateway': 'Southern Gateway Chorus',
            'Chorus of Chesapeake': 'Chorus of the Chesapeake',
            'The Big Orange': 'The Big Orange Chorus',
            'The Pathfinder Chorus': 'Pathfinder Chorus',
            'The Big Apple Chorus': 'Big Apple Chorus',
            'Downeasters': 'The Downeasters',
        }

        for row in data:
            row[2] = reduce(lambda a, kv: a.replace(*kv), mappings.iteritems(), row[2])
            try:
                group = Group.objects.get(
                    name__iexact=row[2],
                )
            except Group.DoesNotExist:
                if self.kind == self.COLLEGIATE:
                    group = Group.objects.create(
                        name=row[2],
                    )
                else:
                    log.error(u"Missing Group: {0}".format(row[2]))
                    continue
            try:
                contestant = Contestant.objects.get(
                    contest=self,
                    group=group,
                )
            except Contestant.DoesNotExist:
                if self.kind == self.COLLEGIATE:
                    try:
                        district = District.objects.get(
                            name=row[4],
                        )
                    except District.DoesNotExist:
                        district = None
                    contestant = Contestant.objects.create(
                        contest=self,
                        group=group,
                        district=district,
                    )
                else:
                    log.error(u"Missing Contestant: {0}".format(row[2]))
                    continue
            if int(row[0]) == 3:
                contestant.quarters_song1, created = Song.objects.get_or_create(
                    name=u"{0}".format(row[5]).strip(),
                )
                contestant.quarters_mus1_points = int(row[6])
                contestant.quarters_prs1_points = int(row[7])
                contestant.quarters_sng1_points = int(row[8])

                contestant.quarters_song2, created = Song.objects.get_or_create(
                    name=u"{0}".format(row[9]).strip(),
                )
                contestant.quarters_mus2_points = int(row[10])
                contestant.quarters_prs2_points = int(row[11])
                contestant.quarters_sng2_points = int(row[12])

                contestant.quarters_place = int(row[1])

            elif int(row[0]) == 2:
                contestant.semis_song1, created = Song.objects.get_or_create(
                    name=u"{0}".format(row[5]).strip(),
                )
                contestant.semis_mus1_points = int(row[6])
                contestant.semis_prs1_points = int(row[7])
                contestant.semis_sng1_points = int(row[8])

                contestant.semis_song2, created = Song.objects.get_or_create(
                    name=u"{0}".format(row[9]).strip(),
                )
                contestant.semis_mus2_points = int(row[10])
                contestant.semis_prs2_points = int(row[11])
                contestant.semis_sng2_points = int(row[12])

                contestant.semis_place = int(row[1])
            elif int(row[0]) == 1:
                contestant.finals_song1, created = Song.objects.get_or_create(
                    name=u"{0}".format(row[5]).strip(),
                )
                contestant.finals_mus1_points = int(row[6])
                contestant.finals_prs1_points = int(row[7])
                contestant.finals_sng1_points = int(row[8])

                contestant.finals_song2, created = Song.objects.get_or_create(
                    name=u"{0}".format(row[9]).strip(),
                )
                contestant.finals_mus2_points = int(row[10])
                contestant.finals_prs2_points = int(row[11])
                contestant.finals_sng2_points = int(row[12])

                contestant.finals_place = int(row[1])
                if contestant.group.kind == 2:
                    contestant.men = int(row[14])
                if self.kind == self.COLLEGIATE:
                    contestant.place = int(row[1])
            else:
                log.error("Missing round")
            contestant.score = float(row[13])
            contestant.save()

    def place_quarters(self):
        if self.kind != self.QUARTET:
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
        if self.kind != self.QUARTET:
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
        if self.kind != self.QUARTET:
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


class Contestant(models.Model):
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
        related_name='contestants',
        null=True,
        blank=True,
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
        upload_to=generate_image_filename,
        help_text="""
            The picture/logo of the resource.""",
        blank=True,
        null=True,
    )

    director = models.ForeignKey(
        'Person',
        related_name='contestants_director',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    lead = models.ForeignKey(
        'Person',
        related_name='contestants_lead',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    tenor = models.ForeignKey(
        'Person',
        related_name='contestants_tenor',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    baritone = models.ForeignKey(
        'Person',
        related_name='contestants_baritone',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    bass = models.ForeignKey(
        'Person',
        related_name='contestants_bass',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    seed = models.IntegerField(
        null=True,
        blank=True,
    )

    prelim = models.FloatField(
        null=True,
        blank=True,
    )

    place = models.IntegerField(
        null=True,
        blank=True,
    )

    score = models.FloatField(
        null=True,
        blank=True,
    )

    stagetime = models.DateTimeField(
        null=True,
        blank=True,
    )

    draw = models.IntegerField(
        null=True,
        blank=True,
    )

    points = models.IntegerField(
        null=True,
        blank=True,
    )

    men = models.IntegerField(
        null=True,
        blank=True,
    )

    quarters_song1 = models.ForeignKey(
        'Song',
        related_name='contestants_quarters_song1',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    quarters_song1_arranger = models.ForeignKey(
        'Person',
        related_name='contestants_quarters_song1_arranger',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    quarters_mus1_points = models.IntegerField(
        null=True,
        blank=True,
    )

    quarters_prs1_points = models.IntegerField(
        null=True,
        blank=True,
    )

    quarters_sng1_points = models.IntegerField(
        null=True,
        blank=True,
    )

    quarters_song1_points = models.IntegerField(
        null=True,
        blank=True,
    )

    quarters_mus1_score = models.FloatField(
        null=True,
        blank=True,
    )

    quarters_prs1_score = models.FloatField(
        null=True,
        blank=True,
    )

    quarters_sng1_score = models.FloatField(
        null=True,
        blank=True,
    )

    quarters_song1_score = models.FloatField(
        null=True,
        blank=True,
    )

    quarters_song2 = models.ForeignKey(
        'Song',
        related_name='contestants_quarters_song2',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    quarters_song2_arranger = models.ForeignKey(
        'Person',
        related_name='contestants_quarters_song2_arranger',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    quarters_mus2_points = models.IntegerField(
        null=True,
        blank=True,
    )

    quarters_prs2_points = models.IntegerField(
        null=True,
        blank=True,
    )

    quarters_sng2_points = models.IntegerField(
        null=True,
        blank=True,
    )

    quarters_song2_points = models.IntegerField(
        null=True,
        blank=True,
    )

    quarters_mus2_score = models.FloatField(
        null=True,
        blank=True,
    )

    quarters_prs2_score = models.FloatField(
        null=True,
        blank=True,
    )

    quarters_sng2_score = models.FloatField(
        null=True,
        blank=True,
    )

    quarters_song2_score = models.FloatField(
        null=True,
        blank=True,
    )

    quarters_place = models.IntegerField(
        null=True,
        blank=True,
    )

    quarters_points = models.IntegerField(
        null=True,
        blank=True,
    )

    quarters_score = models.FloatField(
        null=True,
        blank=True,
    )

    semis_song1 = models.ForeignKey(
        'Song',
        related_name='contestants_semis_song1',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    semis_song1_arranger = models.ForeignKey(
        'Person',
        related_name='contestants_semis_song1_arranger',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    semis_mus1_points = models.IntegerField(
        null=True,
        blank=True,
    )

    semis_prs1_points = models.IntegerField(
        null=True,
        blank=True,
    )

    semis_sng1_points = models.IntegerField(
        null=True,
        blank=True,
    )

    semis_song1_points = models.IntegerField(
        null=True,
        blank=True,
    )

    semis_mus1_score = models.FloatField(
        null=True,
        blank=True,
    )

    semis_prs1_score = models.FloatField(
        null=True,
        blank=True,
    )

    semis_sng1_score = models.FloatField(
        null=True,
        blank=True,
    )

    semis_song1_score = models.FloatField(
        null=True,
        blank=True,
    )

    semis_song2 = models.ForeignKey(
        'Song',
        related_name='contestants_semis_song2',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    semis_song2_arranger = models.ForeignKey(
        'Person',
        related_name='contestants_semis_song2_arranger',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    semis_mus2_points = models.IntegerField(
        null=True,
        blank=True,
    )

    semis_prs2_points = models.IntegerField(
        null=True,
        blank=True,
    )

    semis_sng2_points = models.IntegerField(
        null=True,
        blank=True,
    )

    semis_song2_points = models.IntegerField(
        null=True,
        blank=True,
    )

    semis_mus2_score = models.FloatField(
        null=True,
        blank=True,
    )

    semis_prs2_score = models.FloatField(
        null=True,
        blank=True,
    )

    semis_sng2_score = models.FloatField(
        null=True,
        blank=True,
    )

    semis_song2_score = models.FloatField(
        null=True,
        blank=True,
    )

    semis_place = models.IntegerField(
        null=True,
        blank=True,
    )

    semis_points = models.IntegerField(
        null=True,
        blank=True,
    )

    semis_score = models.FloatField(
        null=True,
        blank=True,
    )

    finals_song1 = models.ForeignKey(
        'Song',
        related_name='contestants_finals_song1',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    finals_song1_arranger = models.ForeignKey(
        'Person',
        related_name='contestants_f1_arranger',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    finals_mus1_points = models.IntegerField(
        null=True,
        blank=True,
    )

    finals_prs1_points = models.IntegerField(
        null=True,
        blank=True,
    )

    finals_sng1_points = models.IntegerField(
        null=True,
        blank=True,
    )

    finals_song1_points = models.IntegerField(
        null=True,
        blank=True,
    )

    finals_mus1_score = models.FloatField(
        null=True,
        blank=True,
    )

    finals_prs1_score = models.FloatField(
        null=True,
        blank=True,
    )

    finals_sng1_score = models.FloatField(
        null=True,
        blank=True,
    )

    finals_song1_score = models.FloatField(
        null=True,
        blank=True,
    )

    finals_song2 = models.ForeignKey(
        'Song',
        related_name='contestants_finals_song2',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    finals_song2_arranger = models.ForeignKey(
        'Person',
        related_name='contestants_f2_arranger',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    finals_mus2_points = models.IntegerField(
        null=True,
        blank=True,
    )

    finals_prs2_points = models.IntegerField(
        null=True,
        blank=True,
    )

    finals_sng2_points = models.IntegerField(
        null=True,
        blank=True,
    )

    finals_song2_points = models.IntegerField(
        null=True,
        blank=True,
    )

    finals_mus2_score = models.FloatField(
        null=True,
        blank=True,
    )

    finals_prs2_score = models.FloatField(
        null=True,
        blank=True,
    )

    finals_sng2_score = models.FloatField(
        null=True,
        blank=True,
    )

    finals_song2_score = models.FloatField(
        null=True,
        blank=True,
    )

    finals_place = models.IntegerField(
        null=True,
        blank=True,
    )

    finals_points = models.IntegerField(
        null=True,
        blank=True,
    )

    finals_score = models.FloatField(
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        self.name = "{0} {1}".format(
            self.contest,
            self.group,
        )
        try:
            self.quarters_song1_points = self.performances.get(
                round=3,
                order=1,
            ).total_points
        except Performance.DoesNotExist:
            self.quarters_song1_points = None
        try:
            self.quarters_song2_points = self.performances.get(
                round=3,
                order=2,
            ).total_points
        except Performance.DoesNotExist:
            self.quarters_song2_points = None
        self.quarters_points = sum(filter(None, [
            self.quarters_song1_points,
            self.quarters_song2_points,
        ])) or None
        try:
            self.semis_song1_points = self.performances.get(
                round=2,
                order=1,
            ).total_points
        except Performance.DoesNotExist:
            self.semis_song1_points = None
        try:
            self.semis_song2_points = self.performances.get(
                round=2,
                order=2,
            ).total_points
        except Performance.DoesNotExist:
            self.semis_song2_points = None
        self.semis_points = sum(filter(None, [
            self.semis_song1_points,
            self.semis_song2_points,
        ])) or None
        try:
            self.finals_song1_points = self.performances.get(
                round=1,
                order=1,
            ).total_points
        except Performance.DoesNotExist:
            self.finals_song1_points = None
        try:
            self.finals_song2_points = self.performances.get(
                round=1,
                order=2,
            ).total_points
        except Performance.DoesNotExist:
            self.finals_song2_points = None
        self.finals_points = sum(filter(None, [
            self.finals_song1_points,
            self.finals_song2_points,
        ])) or None
        self.points = sum(filter(None, [
            self.quarters_points,
            self.semis_points,
            self.finals_points,
        ])) or None
        panel = self.contest.panel
        if self.quarters_points:
            self.quarters_mus1_score = round(self.quarters_mus1_points / panel, 1)
            self.quarters_prs1_score = round(self.quarters_prs1_points / panel, 1)
            self.quarters_sng1_score = round(self.quarters_sng1_points / panel, 1)
            self.quarters_song1_score = round(self.quarters_song1_points / (panel * 3), 1)
            self.quarters_mus2_score = round(self.quarters_mus2_points / panel, 1)
            self.quarters_prs2_score = round(self.quarters_prs2_points / panel, 1)
            self.quarters_sng2_score = round(self.quarters_sng2_points / panel, 1)
            self.quarters_song2_score = round(self.quarters_song2_points / (panel * 3), 1)
            self.quarters_score = round(self.quarters_points / (panel * 6), 1)
        if self.semis_points:
            self.semis_mus1_score = round(self.semis_mus1_points / panel, 1)
            self.semis_prs1_score = round(self.semis_prs1_points / panel, 1)
            self.semis_sng1_score = round(self.semis_sng1_points / panel, 1)
            self.semis_song1_score = round(self.semis_song1_points / (panel * 3), 1)
            self.semis_mus2_score = round(self.semis_mus2_points / panel, 1)
            self.semis_prs2_score = round(self.semis_prs2_points / panel, 1)
            self.semis_sng2_score = round(self.semis_sng2_points / panel, 1)
            self.semis_song2_score = round(self.semis_song2_points / (panel * 3), 1)
            self.semis_score = round(self.semis_points / (panel * 6), 1)
        if self.finals_points:
            self.finals_mus1_score = round(self.finals_mus1_points / panel, 1)
            self.finals_prs1_score = round(self.finals_prs1_points / panel, 1)
            self.finals_sng1_score = round(self.finals_sng1_points / panel, 1)
            self.finals_song1_score = round(self.finals_song1_points / (panel * 3), 1)
            self.finals_mus2_score = round(self.finals_mus2_points / panel, 1)
            self.finals_prs2_score = round(self.finals_prs2_points / panel, 1)
            self.finals_sng2_score = round(self.finals_sng2_points / panel, 1)
            self.finals_song2_score = round(self.finals_song2_points / (panel * 3), 1)
            self.finals_score = round(self.finals_points / (panel * 6), 1)
        self.group.save()
        super(Contestant, self).save(*args, **kwargs)

    def clean(self):
            if self.group.kind == Group.QUARTET and self.director is not None:
                raise ValidationError('Quartets do not have directors.')
            if self.group.kind == Group.CHORUS and (
                self.lead is not None or
                self.tenor is not None or
                self.baritone is not None or
                self.bass is not None
            ):
                raise ValidationError('Choruses do not have parts.')
            if self.group.kind == Group.QUARTET and self.contest.kind == Contest.CHORUS:
                raise ValidationError("Group and Contest types must match.")
            if self.group.kind == Group.CHORUS and self.contest.kind != Contest.CHORUS:
                raise ValidationError("Group and Contest types must match.")

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
        return self.name

    class Meta:
        ordering = (
            '-contest__year',
            'place',
            '-score',
        )
        unique_together = (
            ('group', 'contest',),
        )


class Award(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the award.  Must be unique.""",
        max_length=200,
        unique=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
    )

    description = models.CharField(
        null=True,
        blank=True,
        max_length=200,
    )

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse(
    #         'website:award-detail',
    #         args=[self.slug],
    #     )


class GroupAward(models.Model):
    """Awards and placement"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    group = models.ForeignKey(
        'Group',
    )

    contest = models.ForeignKey(
        'Contest',
    )

    award = models.ForeignKey(
        'Award',
    )

    def __unicode__(self):
        return self.name


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

    is_medley = models.BooleanField(
        default=False,
    )

    is_parody = models.BooleanField(
        default=False,
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
        return self.name


class Performance(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    FINALS = 1
    SEMIS = 2
    QUARTERS = 3

    ROUND_CHOICES = (
        (FINALS, "Finals"),
        (SEMIS, "Semis"),
        (QUARTERS, "Quarters"),
    )

    FIRST = 1
    SECOND = 2

    ORDER_CHOICES = (
        (FIRST, '1'),
        (SECOND, '2'),
    )

    name = models.CharField(
        max_length=255,
        # unique=True,
        null=True,
        blank=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        # unique=True,
        max_length=255,
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

    round = models.IntegerField(
        null=True,
        blank=True,
        default=QUARTERS,
        choices=ROUND_CHOICES,
    )

    order = models.IntegerField(
        null=True,
        blank=True,
        choices=ORDER_CHOICES,
    )

    song = models.ForeignKey(
        'Song',
        related_name='performances',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    arranger = models.ForeignKey(
        'Person',
        related_name='performances',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    mus_points = models.IntegerField(
        null=True,
        blank=True,
    )

    prs_points = models.IntegerField(
        null=True,
        blank=True,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
    )

    total_points = models.IntegerField(
        null=True,
        blank=True,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
    )

    prs_score = models.FloatField(
        null=True,
        blank=True,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
    )

    total_score = models.FloatField(
        null=True,
        blank=True,
    )

    penalty = models.TextField(
        null=True,
        blank=True,
    )

    unique_together = (
        ('contestant', 'round', 'order',),
    )

    class Meta:
        ordering = [
            'contestant',
            'round',
            'order',
        ]

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = "{0} {1} {2} {3}".format(
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
        if self.mus_points:
            self.mus_score = round(self.mus_points / panel, 1)
        if self.prs_points:
            self.prs_score = round(self.prs_points / panel, 1)
        if self.sng_points:
            self.sng_score = round(self.sng_points / panel, 1)
        if self.total_points:
            self.total_score = round(self.total_points / (panel * 3), 1)
        super(Performance, self).save(*args, **kwargs)
