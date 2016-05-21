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


# Organizations
class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization

    status = Organization.STATUS.active


class BHSFactory(OrganizationFactory):
    level = Organization.LEVEL.international
    kind = Organization.KIND.international
    name = 'International'
    short_name = 'BHS'
    long_name = 'International'
    parent = None


class DistrictFactory(OrganizationFactory):
    level = Organization.LEVEL.district
    kind = Organization.KIND.district
    parent = SubFactory(
        'apps.api.factories.BHSFactory',
    )


class DivisionOrganizationFactory(OrganizationFactory):
    level = Organization.LEVEL.division
    kind = Organization.KIND.division


class FHTFactory(OrganizationFactory):
    level = Organization.LEVEL.district
    kind = Organization.KIND.noncomp
    name = 'Frank Thorne District'
    short_name = 'FHT'
    long_name = 'Frank Thorne'
    parent = SubFactory(
        'apps.api.factories.BHSFactory',
    )


class AffiliateDistrictOrganizationFactory(OrganizationFactory):
    level = Organization.LEVEL.district
    kind = Organization.KIND.affiliate
    parent = SubFactory(
        'apps.api.factories.BHSFactory',
    )


# Awards
class AwardFactory(DjangoModelFactory):
    class Meta:
        model = Award
    status = Award.STATUS.active


class InternationalQuartetAward(AwardFactory):
    kind = Award.KIND.quartet
    season = Award.SEASON.international
    championship_rounds = 3
    qualifier_rounds = 2
    is_primary = True
    threshold = 76.0
    minimum = 73.0
    organization = SubFactory(
        'apps.api.factories.BHSFactory'
    )


class InternationalChorusAward(AwardFactory):
    kind = Award.KIND.chorus
    season = Award.SEASON.international
    championship_rounds = 1
    is_primary = True
    organization = SubFactory(
        'apps.api.factories.BHSFactory'
    )


class DistrictQuartetAward(AwardFactory):
    kind = Award.KIND.quartet
    season = Award.SEASON.district
    championship_rounds = 2
    is_primary = True
    # threshold = 76.0
    # minimum = 73.0
    organization = SubFactory(
        'apps.api.factories.DistrictFactory'
    )


class DistrictChorusAward(AwardFactory):
    kind = Award.KIND.chorus
    season = Award.SEASON.district
    championship_rounds = 1
    is_primary = True
    organization = SubFactory(
        'apps.api.factories.DistrictFactory'
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
    venue = SubFactory(
        'apps.api.factories.VenueFactory'
    )


class SummerConventionFactory(ConventionFactory):
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
        'apps.api.factories.BHSFactory',
    )


class MidwinterConventionFactory(ConventionFactory):
    kind = Convention.KIND.international
    season = Convention.SEASON.midwinter
    risers = [0, ]
    year = 2016
    date = DateTimeTZRange(
        lower=datetime(2016, 01, 29, 12, 00),
        upper=datetime(2016, 01, 30, 12, 00),
        bounds='[)',
    )
    organization = SubFactory(
        'apps.api.factories.BHSFactory',
    )


class SpringConventionFactory(ConventionFactory):
    kind = Convention.KIND.district
    season = Convention.SEASON.spring
    risers = [5, 7, 9, ]
    year = 2016
    date = DateTimeTZRange(
        lower=datetime(2016, 04, 01, 12, 00),
        upper=datetime(2016, 04, 02, 12, 00),
        bounds='[)',
    )


class FallConventionFactory(ConventionFactory):
    kind = Convention.KIND.district
    season = Convention.SEASON.fall
    risers = [5, 7, 9, ]
    year = 2016
    date = DateTimeTZRange(
        lower=datetime(2016, 10, 01, 12, 00),
        upper=datetime(2016, 10, 02, 12, 00),
        bounds='[)',
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
