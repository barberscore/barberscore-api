from factory.django import (
    DjangoModelFactory,
)

from factory import (
    SubFactory,
    PostGenerationMethodCall,
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
    User,
    Venue,
)


class AdminFactory(DjangoModelFactory):
    class Meta:
        model = User
    email = 'admin@barberscore.com'
    password = PostGenerationMethodCall('set_password', 'password')
    name = 'Admin User'
    is_staff = True


class AwardFactory(DjangoModelFactory):
    class Meta:
        model = Award
    status = Award.STATUS.active
    kind = Award.KIND.quartet
    season = Award.SEASON.international
    championship_rounds = 3
    is_primary = True
    cutoff = 76.0
    minimum = 73.0
    organization = SubFactory(
        'apps.api.factories.InternationalFactory'
    )


class CertificationFactory(DjangoModelFactory):
    class Meta:
        model = Certification

    status = Certification.STATUS.active
    category = Certification.CATEGORY.admin
    person = SubFactory(
        'apps.api.factories.PersonFactory'
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


class ChorusFactory(DjangoModelFactory):
    class Meta:
        model = Group

    status = Group.STATUS.active

    name = 'Test Chorus'
    kind = Group.KIND.chorus
    chapter = SubFactory(
        'apps.api.factories.ChapterFactory'
    )
    organization = SubFactory(
        'apps.api.factories.DistrictFactory',
    )


class ContestantFactory(DjangoModelFactory):
    class Meta:
        model = Contestant

    status = Contestant.STATUS.new
    performer = SubFactory(
        'apps.api.factories.PerformerFactory'
    )
    contest = SubFactory(
        'apps.api.factories.ContestFactory',
    )


class ContestFactory(DjangoModelFactory):
    class Meta:
        model = Contest

    status = Contest.STATUS.new
    cycle = 2016
    session = SubFactory(
        'apps.api.factories.SessionFactory'
    )
    award = SubFactory(
        'apps.api.factories.AwardFactory'
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
    name = 'International'
    level = Organization.LEVEL.international
    kind = Organization.KIND.international
    short_name = 'BHS'
    long_name = 'International'


class DistrictFactory(DjangoModelFactory):
    class Meta:
        model = Organization

    status = Organization.STATUS.active
    name = 'Cardinal District'
    level = Organization.LEVEL.district
    kind = Organization.KIND.district
    short_name = 'CAR'
    long_name = 'Cardinal'


class InternationalFactory(DjangoModelFactory):
    class Meta:
        model = Organization

    status = Organization.STATUS.active
    name = 'International'
    level = Organization.LEVEL.international
    kind = Organization.KIND.international
    short_name = 'BHS'
    long_name = 'International'


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


class MemberFactory(DjangoModelFactory):
    class Meta:
        model = Member

    status = Member.STATUS.active
    chapter = SubFactory(
        'apps.api.factories.ChapterFactory'
    )
    person = SubFactory(
        'apps.api.factories.PersonFactory'
    )


class PerformanceFactory(DjangoModelFactory):
    class Meta:
        model = Performance

    status = Performance.STATUS.new
    performer = SubFactory(
        'apps.api.factories.PerformerFactory',
    )
    round = SubFactory(
        'apps.api.factories.RoundFactory',
        # session=Iterator(Session.objects.all())
    )


class PerformerFactory(DjangoModelFactory):
    class Meta:
        model = Performer
        django_get_or_create = (
            'status',
        )
    status = Performer.STATUS.new
    # representing = SubFactory(
    #     'apps.api.factories.DistrictFactory'
    # )
    session = SubFactory(
        'apps.api.factories.SessionFactory'
    )
    group = SubFactory(
        'apps.api.factories.QuartetFactory'
    )


class PersonFactory(DjangoModelFactory):
    class Meta:
        model = Person

    name = 'Test Person'
    status = Person.STATUS.active


class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group

    status = Group.STATUS.active

    name = 'Test Quartet'
    kind = Group.KIND.quartet
    organization = SubFactory(
        'apps.api.factories.DistrictFactory',
    )


class QuartetFactory(DjangoModelFactory):
    class Meta:
        model = Group

    status = Group.STATUS.active

    name = 'Test Quartet'
    kind = Group.KIND.quartet
    organization = SubFactory(
        'apps.api.factories.DistrictFactory',
    )


class RoundFactory(DjangoModelFactory):
    class Meta:
        model = Round

    status = Round.STATUS.new
    kind = Round.KIND.finals
    num = 1
    session = SubFactory(
        'apps.api.factories.SessionFactory'
    )


class ScoreFactory(DjangoModelFactory):
    class Meta:
        model = Score

    status = Score.STATUS.new
    judge = SubFactory(
        'apps.api.factories.JudgeFactory',
    )
    song = SubFactory(
        'apps.api.factories.SongFactory',
        # performer=Performer.objects.all().first()
    )
    category = 1
    kind = 10


class SessionFactory(DjangoModelFactory):
    class Meta:
        model = Session
        django_get_or_create = (
            'kind',
        )

    kind = Session.KIND.quartet
    convention = SubFactory(
        'apps.api.factories.ConventionFactory',
    )


class SongFactory(DjangoModelFactory):
    class Meta:
        model = Song

    status = Performance.STATUS.new
    order = 1
    performance = SubFactory(
        'apps.api.factories.PerformanceFactory',
    )
    submission = SubFactory(
        'apps.api.factories.SubmissionFactory',
        # performer=Iterator(Performer.objects.all())
    )


class SubmissionFactory(DjangoModelFactory):
    class Meta:
        model = Submission

    status = Submission.STATUS.new
    performer = SubFactory(
        'apps.api.factories.PerformerFactory'
    )
    chart = SubFactory(
        'apps.api.factories.ChartFactory'
    )


class RoleFactory(DjangoModelFactory):
    class Meta:
        model = Role

    status = Role.STATUS.active
    person = SubFactory(
        'apps.api.factories.PersonFactory'
    )
    part = Role.PART.tenor
    group = SubFactory(
        'apps.api.factories.QuartetFactory'
    )


class TenorFactory(DjangoModelFactory):
    class Meta:
        model = Role

    status = Role.STATUS.active
    person = SubFactory(
        'apps.api.factories.PersonFactory'
    )
    part = Role.PART.tenor
    group = SubFactory(
        'apps.api.factories.QuartetFactory'
    )


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    email = 'user@barberscore.com'
    password = PostGenerationMethodCall('set_password', 'password')
    name = 'Test User'


class VenueFactory(DjangoModelFactory):
    class Meta:
        model = Venue
        django_get_or_create = (
            'location',
            'city',
            'state',
            'timezone',
        )
    location = 'Nashville Convention Center'
    city = 'Nashville'
    state = 'Tennessee'
    timezone = 'US/Central'
