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
        'apps.api.factories.OrganizationFactory'
    )
    venue = SubFactory(
        'apps.api.factories.VenueFactory'
    )


class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization

    name = 'International'
    status = Organization.STATUS.active
    level = Organization.LEVEL.international
    kind = Organization.KIND.international
    short_name = 'BHS'
    long_name = 'International'


class VenueFactory(DjangoModelFactory):
    class Meta:
        model = Venue

    location = 'Nashville Convention Center'
    city = 'Nashville'
    state = 'Tennessee'
    timezone = 'US/Central'
