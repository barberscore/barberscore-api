from factory.django import (
    DjangoModelFactory,
)

from factory import (
    SubFactory,
)

from datetime import datetime

from psycopg2.extras import DateTimeTZRange

from apps.api.models import (
    Award,
    Certification,
    Chapter,
    Chart,
    Contest,
    Contestant,
    Convention,
    Group,
    Judge,
    Member,
    Organization,
    Performance,
    Performer,
    Person,
    Role,
    Round,
    Score,
    Session,
    Song,
    Submission,
    Venue,
)


class ConventionFactory(DjangoModelFactory):
    class Meta:
        model = Convention

    status = Convention.STATUS.new
    kind = Convention.KIND.international
    season = Convention.SEASON.international
    risers = [13, ]
    year = 2016
    date = DateTimeTZRange(
        lower=datetime(2016, 07, 01, 12, 00),
        upper=datetime(2016, 07, 04, 12, 00),
        bounds='[)',
    )
    organization = SubFactory(
        'apps.api.factories.InternationalFactory'
    )
    venue = SubFactory(
        'apps.api.factories.VenueFactory'
    )


class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization

    status = Organization.STATUS.active


class InternationalFactory(OrganizationFactory):
    name = 'International'
    level = Organization.LEVEL.international
    kind = Organization.KIND.international
    short_name = 'BHS'
    long_name = 'International'


class DistrictFactory(OrganizationFactory):
    name = 'Cardinal District'
    level = Organization.LEVEL.district
    kind = Organization.KIND.district
    short_name = 'CAR'
    long_name = 'Cardinal'


class VenueFactory(DjangoModelFactory):
    class Meta:
        model = Venue

    location = 'Nashville Convention Center'
    city = 'Nashville'
    state = 'Tennessee'
    timezone = 'US/Central'


class AwardFactory(DjangoModelFactory):
    class Meta:
        model = Award

    status = Award.STATUS.active
    kind = Award.KIND.quartet
    season = Award.SEASON.international
    num_rounds = 3
    is_primary = True
    cutoff = 76.0
    minimum = 73.0
    organization = SubFactory(
        'apps.api.factories.InternationalFactory'
    )


class ChapterFactory(DjangoModelFactory):
    class Meta:
        model = Chapter

    name = 'Test Chapter'
    status = Chapter.STATUS.active
    code = 'A-999'
    organization = SubFactory(
        'apps.api.factories.DistrictFactory',
    )


class ChartFactory(DjangoModelFactory):
    class Meta:
        model = Chart

    title = 'The Old Songs'


class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group

    status = Group.STATUS.active


class QuartetFactory(GroupFactory):

    name = 'Test Quartet'
    kind = Group.KIND.quartet
    organization = SubFactory(
        'apps.api.factories.DistrictFactory',
    )


class ChorusFactory(GroupFactory):

    name = 'Test Chorus'
    kind = Group.KIND.chorus
    chapter = SubFactory(
        'apps.api.factories.ChapterFactory'
    )
    organization = SubFactory(
        'apps.api.factories.DistrictFactory',
    )


class PersonFactory(DjangoModelFactory):
    class Meta:
        model = Person

    name = 'Test Person'
    status = Person.STATUS.active


class SessionFactory(DjangoModelFactory):
    class Meta:
        model = Session

    kind = Session.KIND.quartet
    convention = SubFactory(
        'apps.api.factories.ConventionFactory',
    )


class CertificationFactory(DjangoModelFactory):
    class Meta:
        model = Certification

    status = Certification.STATUS.active
    category = Certification.CATEGORY.admin
    person = SubFactory(
        'apps.api.factories.PersonFactory'
    )


class JudgeFactory(DjangoModelFactory):
    class Meta:
        model = Judge

    category = Judge.CATEGORY.admin
    kind = Judge.KIND.official
    session = SubFactory(
        'apps.api.factories.SessionFactory'
    )
    certification = SubFactory(
        'apps.api.factories.CertificationFactory'
    )
