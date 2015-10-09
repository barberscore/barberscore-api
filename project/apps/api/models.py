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
)

from django.core.exceptions import (
    ValidationError,
)

from model_utils.models import (
    TimeFramedModel,
    StatusModel,
)

from model_utils import Choices

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
        max_length=255,
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

    def clean(self):
        if self.name.endswith(" ") or self.name.startswith(" "):
            raise ValidationError('Names must not start or end with extra spaces.')

    class Meta:
        abstract = True


class Person(Common):

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
        null=True,
        blank=True,
    )


class Group(Common):

    KIND = Choices(
        (1, 'quartet', 'Quartet'),
        (2, 'chorus', 'Chorus'),
    )

    kind = models.IntegerField(
        choices=KIND,
        default=KIND.quartet,
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
        return u"{0}".format(self.name)

    class Meta:
        ordering = (
            'name',
        )

    fuzzy = models.TextField(
        null=True,
        blank=True,
    )


class District(Common):
    KIND = Choices(
        (0, 'bhs', "BHS"),
        (1, 'district', "District"),
        (2, 'affiliate', "Affiliate"),
    )

    long_name = models.CharField(
        null=True,
        blank=True,
        max_length=200,
    )

    kind = models.IntegerField(
        choices=KIND,
        default=KIND.bhs,
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

    YEAR = Choices(
        (2016, '2016', '2016'),
        (2015, '2015', '2015'),
        (2014, '2014', '2014'),
        (2013, '2013', '2013'),
        (2012, '2012', '2012'),
        (2011, '2011', '2011'),
        (2010, '2010', '2010'),
        (2009, '2009', '2009'),
        (2008, '2008', '2008'),
        (2007, '2007', '2007'),
        (2006, '2006', '2006'),
        (2005, '2005', '2005'),
        (2004, '2004', '2004'),
        (2003, '2003', '2003'),
        (2002, '2002', '2002'),
        (2001, '2001', '2001'),
        (2000, '2000', '2000'),
        (1999, '1999', '1999'),
        (1998, '1998', '1998'),
        (1997, '1997', '1997'),
        (1996, '1996', '1996'),
        (1995, '1995', '1995'),
        (1994, '1994', '1994'),
        (1993, '1993', '1993'),
        (1992, '1992', '1992'),
        (1991, '1991', '1991'),
        (1990, '1990', '1990'),
        (1989, '1989', '1989'),
        (1988, '1988', '1988'),
        (1987, '1987', '1987'),
        (1986, '1986', '1986'),
        (1985, '1985', '1985'),
        (1984, '1984', '1984'),
        (1983, '1983', '1983'),
        (1982, '1982', '1982'),
        (1981, '1981', '1981'),
        (1980, '1980', '1980'),
        (1979, '1979', '1979'),
        (1978, '1978', '1978'),
        (1977, '1977', '1977'),
        (1976, '1976', '1976'),
        (1975, '1975', '1975'),
        (1974, '1974', '1974'),
        (1973, '1973', '1973'),
        (1972, '1972', '1972'),
        (1971, '1971', '1971'),
        (1970, '1970', '1970'),
        (1969, '1969', '1969'),
        (1968, '1968', '1968'),
        (1967, '1967', '1967'),
        (1966, '1966', '1966'),
        (1965, '1965', '1965'),
        (1964, '1964', '1964'),
        (1963, '1963', '1963'),
        (1962, '1962', '1962'),
        (1961, '1961', '1961'),
        (1960, '1960', '1960'),
        (1959, '1959', '1959'),
        (1958, '1958', '1958'),
        (1957, '1957', '1957'),
        (1956, '1956', '1956'),
        (1955, '1955', '1955'),
        (1954, '1954', '1954'),
        (1953, '1953', '1953'),
        (1952, '1952', '1952'),
        (1951, '1951', '1951'),
        (1950, '1950', '1950'),
        (1949, '1949', '1949'),
        (1948, '1948', '1948'),
        (1947, '1947', '1947'),
        (1946, '1946', '1946'),
        (1945, '1945', '1945'),
        (1944, '1944', '1944'),
        (1943, '1943', '1943'),
        (1942, '1942', '1942'),
        (1941, '1941', '1941'),
        (1940, '1940', '1940'),
        (1939, '1939', '1939'),
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
        choices=KIND,
        null=True,
        blank=True,
    )

    year = models.IntegerField(
        choices=YEAR,
        default=datetime.datetime.now().year,
        null=True,
        blank=True,
    )

    district = models.ForeignKey(
        'District',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
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
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        if self.kind in [
            self.INTERNATIONAL,
            self.MIDWINTER,
            self.PACIFIC,
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


class Contest(StatusModel):

    STATUS = Choices(
        'Upcoming',
        'Current',
        'Pending',
        'Complete',
    )

    YEAR = Choices(
        (2016, '2016', '2016'),
        (2015, '2015', '2015'),
        (2014, '2014', '2014'),
        (2013, '2013', '2013'),
        (2012, '2012', '2012'),
        (2011, '2011', '2011'),
        (2010, '2010', '2010'),
        (2009, '2009', '2009'),
        (2008, '2008', '2008'),
        (2007, '2007', '2007'),
        (2006, '2006', '2006'),
        (2005, '2005', '2005'),
        (2004, '2004', '2004'),
        (2003, '2003', '2003'),
        (2002, '2002', '2002'),
        (2001, '2001', '2001'),
        (2000, '2000', '2000'),
        (1999, '1999', '1999'),
        (1998, '1998', '1998'),
        (1997, '1997', '1997'),
        (1996, '1996', '1996'),
        (1995, '1995', '1995'),
        (1994, '1994', '1994'),
        (1993, '1993', '1993'),
        (1992, '1992', '1992'),
        (1991, '1991', '1991'),
        (1990, '1990', '1990'),
        (1989, '1989', '1989'),
        (1988, '1988', '1988'),
        (1987, '1987', '1987'),
        (1986, '1986', '1986'),
        (1985, '1985', '1985'),
        (1984, '1984', '1984'),
        (1983, '1983', '1983'),
        (1982, '1982', '1982'),
        (1981, '1981', '1981'),
        (1980, '1980', '1980'),
        (1979, '1979', '1979'),
        (1978, '1978', '1978'),
        (1977, '1977', '1977'),
        (1976, '1976', '1976'),
        (1975, '1975', '1975'),
        (1974, '1974', '1974'),
        (1973, '1973', '1973'),
        (1972, '1972', '1972'),
        (1971, '1971', '1971'),
        (1970, '1970', '1970'),
        (1969, '1969', '1969'),
        (1968, '1968', '1968'),
        (1967, '1967', '1967'),
        (1966, '1966', '1966'),
        (1965, '1965', '1965'),
        (1964, '1964', '1964'),
        (1963, '1963', '1963'),
        (1962, '1962', '1962'),
        (1961, '1961', '1961'),
        (1960, '1960', '1960'),
        (1959, '1959', '1959'),
        (1958, '1958', '1958'),
        (1957, '1957', '1957'),
        (1956, '1956', '1956'),
        (1955, '1955', '1955'),
        (1954, '1954', '1954'),
        (1953, '1953', '1953'),
        (1952, '1952', '1952'),
        (1951, '1951', '1951'),
        (1950, '1950', '1950'),
        (1949, '1949', '1949'),
        (1948, '1948', '1948'),
        (1947, '1947', '1947'),
        (1946, '1946', '1946'),
        (1945, '1945', '1945'),
        (1944, '1944', '1944'),
        (1943, '1943', '1943'),
        (1942, '1942', '1942'),
        (1941, '1941', '1941'),
        (1940, '1940', '1940'),
        (1939, '1939', '1939'),
    )

    KIND = Choices(
        (1, 'quartet', 'Quartet',),
        (2, 'chorus', 'Chorus',),
        (3, 'senior', 'Senior',),
        (4, 'collegiate', 'Collegiate',),
    )

    LEVEL = Choices(
        (1, 'international', "International"),
        (2, 'district', "District"),
        (4, 'prelims', "Prelims"),
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
        max_length=200,
        unique=True,
    )

    level = models.IntegerField(
        choices=LEVEL,
        default=LEVEL.international,
    )

    kind = models.IntegerField(
        choices=KIND,
        default=KIND.quartet,
    )

    year = models.IntegerField(
        choices=YEAR,
        default=datetime.datetime.now().year,
    )

    district = models.ForeignKey(
        'District',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    convention = models.ForeignKey(
        'Convention',
        related_name='contests',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
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
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        if self.level == self.INTERNATIONAL:
            self.name = u"{0} {1} {2}".format(
                self.get_level_display(),
                self.get_kind_display(),
                self.get_year_display(),
            )
        elif self.level == self.PRELIMS:
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

    # def import_legacy(self):
    #     reader = csv.reader(self.scoresheet_csv)
    #     # next(reader)
    #     data = [row for row in reader]

    #     mappings = {
    #         'The Westminster Chorus': 'Westminster',
    #         'Southern Gateway': 'Southern Gateway Chorus',
    #         'Chorus of Chesapeake': 'Chorus of the Chesapeake',
    #         'The Big Orange': 'The Big Orange Chorus',
    #         'The Pathfinder Chorus': 'Pathfinder Chorus',
    #         'The Big Apple Chorus': 'Big Apple Chorus',
    #         'Downeasters': 'The Downeasters',
    #     }

    #     for row in data:
    #         row[2] = reduce(lambda a, kv: a.replace(*kv), mappings.iteritems(), row[2])
    #         try:
    #             group = Group.objects.get(
    #                 name__iexact=row[2],
    #             )
    #         except Group.DoesNotExist:
    #             if self.kind == self.COLLEGIATE:
    #                 group = Group.objects.create(
    #                     name=row[2],
    #                 )
    #             else:
    #                 log.error(u"Missing Group: {0}".format(row[2]))
    #                 continue
    #         try:
    #             contestant = Contestant.objects.get(
    #                 contest=self,
    #                 group=group,
    #             )
    #         except Contestant.DoesNotExist:
    #             if self.kind == self.COLLEGIATE:
    #                 try:
    #                     district = District.objects.get(
    #                         name=row[4],
    #                     )
    #                 except District.DoesNotExist:
    #                     district = None
    #                 contestant = Contestant.objects.create(
    #                     contest=self,
    #                     group=group,
    #                     district=district,
    #                 )
    #             else:
    #                 log.error(u"Missing Contestant: {0}".format(row[2]))
    #                 continue
    #         if int(row[0]) == 3:
    #             contestant.quarters_song1, created = Song.objects.get_or_create(
    #                 name=u"{0}".format(row[5]).strip(),
    #             )
    #             contestant.quarters_mus1_points = int(row[6])
    #             contestant.quarters_prs1_points = int(row[7])
    #             contestant.quarters_sng1_points = int(row[8])

    #             contestant.quarters_song2, created = Song.objects.get_or_create(
    #                 name=u"{0}".format(row[9]).strip(),
    #             )
    #             contestant.quarters_mus2_points = int(row[10])
    #             contestant.quarters_prs2_points = int(row[11])
    #             contestant.quarters_sng2_points = int(row[12])

    #             contestant.quarters_place = int(row[1])

    #         elif int(row[0]) == 2:
    #             contestant.semis_song1, created = Song.objects.get_or_create(
    #                 name=u"{0}".format(row[5]).strip(),
    #             )
    #             contestant.semis_mus1_points = int(row[6])
    #             contestant.semis_prs1_points = int(row[7])
    #             contestant.semis_sng1_points = int(row[8])

    #             contestant.semis_song2, created = Song.objects.get_or_create(
    #                 name=u"{0}".format(row[9]).strip(),
    #             )
    #             contestant.semis_mus2_points = int(row[10])
    #             contestant.semis_prs2_points = int(row[11])
    #             contestant.semis_sng2_points = int(row[12])

    #             contestant.semis_place = int(row[1])
    #         elif int(row[0]) == 1:
    #             contestant.finals_song1, created = Song.objects.get_or_create(
    #                 name=u"{0}".format(row[5]).strip(),
    #             )
    #             contestant.finals_mus1_points = int(row[6])
    #             contestant.finals_prs1_points = int(row[7])
    #             contestant.finals_sng1_points = int(row[8])

    #             contestant.finals_song2, created = Song.objects.get_or_create(
    #                 name=u"{0}".format(row[9]).strip(),
    #             )
    #             contestant.finals_mus2_points = int(row[10])
    #             contestant.finals_prs2_points = int(row[11])
    #             contestant.finals_sng2_points = int(row[12])

    #             contestant.finals_place = int(row[1])
    #             if contestant.group.kind == 2:
    #                 contestant.men = int(row[14])
    #             if self.kind == self.COLLEGIATE:
    #                 contestant.place = int(row[1])
    #         else:
    #             log.error("Missing round")
    #         contestant.score = float(row[13])
    #         contestant.save()

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


class Contestant(TimeFramedModel):
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
        upload_to=generate_image_filename,
        help_text="""
            The picture/logo of the resource.""",
        blank=True,
        null=True,
    )

    seed = models.IntegerField(
        null=True,
        blank=True,
    )

    prelim = models.FloatField(
        null=True,
        blank=True,
    )

    points = models.IntegerField(
        null=True,
        blank=True,
    )

    score = models.FloatField(
        null=True,
        blank=True,
    )

    place = models.IntegerField(
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

    men = models.IntegerField(
        null=True,
        blank=True,
    )

    quarters_points = models.IntegerField(
        null=True,
        blank=True,
    )

    semis_points = models.IntegerField(
        null=True,
        blank=True,
    )

    finals_points = models.IntegerField(
        null=True,
        blank=True,
    )

    quarters_score = models.FloatField(
        null=True,
        blank=True,
    )

    semis_score = models.FloatField(
        null=True,
        blank=True,
    )

    finals_score = models.FloatField(
        null=True,
        blank=True,
    )

    quarters_place = models.IntegerField(
        null=True,
        blank=True,
    )

    semis_place = models.IntegerField(
        null=True,
        blank=True,
    )

    finals_place = models.IntegerField(
        null=True,
        blank=True,
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


class Judge(models.Model):
    """Contest Judge"""
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
    )

    part = models.IntegerField(
        choices=PART,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2}".format(
            self.contest,
            self.get_part_display(),
            self.person,
        )
        super(Judge, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('contest', 'person',),
        )
        ordering = (
            '-name',
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
        null=True,
        blank=True,
    )


class Performance(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
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

    contestant = models.ForeignKey(
        'Contestant',
        related_name='performances',
    )

    round = models.IntegerField(
        choices=ROUND,
    )

    order = models.IntegerField(
        choices=ORDER,
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
    CATEGORY = Choices(
        (1, "Music"),
        (2, "Presentation"),
        (3, "Singing"),
        (4, "Admin"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    performance = models.ForeignKey(
        'Performance',
        related_name='scores',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    judge = models.ForeignKey(
        'Judge',
        related_name='scores',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    points = models.IntegerField(
        null=True,
        blank=True,
    )

    category = models.IntegerField(
        null=True,
        blank=True,
        choices=CATEGORY,
    )

    is_practice = models.BooleanField(
        default=False,
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
        null=True,
        blank=True,
        max_length=200,
    )

    bhs_arranger = models.CharField(
        null=True,
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
        null=True,
        blank=True,
        max_length=200,
    )

    name = models.CharField(
        max_length=200,
        unique=True,
    )

    person_match = models.CharField(
        null=True,
        blank=True,
        max_length=200,
    )

    fuzzy = models.TextField(
        null=True,
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
            ('bhs_arranger', 'bhs_songname')
        )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} [{1}]".format(
            self.song,
            self.arranger,
        )
        super(Arrangement, self).save(*args, **kwargs)


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
