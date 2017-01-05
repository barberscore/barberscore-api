# Standard Libary
from datetime import datetime

# Third-Party
import pytz
from factory import (
    Faker,
    PostGenerationMethodCall,
    SubFactory,
)
from factory.django import DjangoModelFactory
from psycopg2.extras import DateTimeTZRange

# First-Party
from app.models import (
    Assignment,
    Award,
    Chapter,
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
    Slot,
    Song,
    Submission,
    User,
    Venue,
)


# Users
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = (
            'email',
        )


class AdminFactory(UserFactory):
    email = 'admin@barberscore.com'
    password = PostGenerationMethodCall('set_password', 'password')
    name = 'Admin User'
    is_staff = True


class PublicFactory(UserFactory):
    email = 'user@barberscore.com'
    password = PostGenerationMethodCall('set_password', 'password')
    name = 'Public User'


# Awards
class AwardFactory(DjangoModelFactory):
    class Meta:
        model = Award
    status = Award.STATUS.active


class InternationalQuartetAwardFactory(AwardFactory):
    kind = Award.KIND.quartet
    championship_season = Award.SEASON.summer
    championship_rounds = 3
    is_primary = True
    is_qualification_required = True
    qualifier_season = Award.SEASON.spring
    qualifier_rounds = 2
    threshold = 76
    minimum = 70
    advance = 73
    organization = SubFactory(
        'app.factories.InternationalFactory'
    )


class InternationalChorusAwardFactory(AwardFactory):
    kind = Award.KIND.chorus
    championship_season = Award.SEASON.summer
    championship_rounds = 1
    is_primary = True
    is_qualification_required = True
    qualifier_season = Award.SEASON.fall
    qualifier_rounds = 1
    organization = SubFactory(
        'app.factories.InternationalFactory'
    )


class InternationalSeniorsAwardFactory(AwardFactory):
    kind = Award.KIND.seniors
    championship_season = Award.SEASON.midwinter
    championship_rounds = 1
    is_primary = True
    is_qualification_required = True
    qualifier_season = Award.SEASON.spring
    qualifier_rounds = 1
    organization = SubFactory(
        'app.factories.InternationalFactory'
    )


class InternationalYouthAwardFactory(AwardFactory):
    kind = Award.KIND.youth
    championship_season = Award.SEASON.summer
    championship_rounds = 1
    is_primary = True
    is_qualification_required = True
    qualifier_season = Award.SEASON.spring
    qualifier_rounds = 1
    threshold = 73
    minimum = 61
    advance = 70
    organization = SubFactory(
        'app.factories.InternationalFactory'
    )


class DistrictQuartetAwardFactory(AwardFactory):
    kind = Award.KIND.quartet
    championship_season = Award.SEASON.fall
    championship_rounds = 2
    is_primary = True
    # is_qualification_required = True
    # qualifier_season = Award.SEASON.spring
    # qualifier_rounds = 2
    # threshold = 76
    # minimum = 70
    # advance = 73
    organization = SubFactory(
        'app.factories.DistrictFactory'
    )


class DistrictChorusAwardFactory(AwardFactory):
    kind = Award.KIND.chorus
    championship_season = Award.SEASON.spring
    championship_rounds = 1
    is_primary = True
    # is_qualification_required = True
    # qualifier_season = Award.SEASON.fall
    # qualifier_rounds = 1
    organization = SubFactory(
        'app.factories.DistrictFactory'
    )


class DistrictSeniorsAwardFactory(AwardFactory):
    kind = Award.KIND.seniors
    championship_season = Award.SEASON.fall
    championship_rounds = 1
    is_primary = True
    # is_qualification_required = True
    # qualifier_season = Award.SEASON.spring
    # qualifier_rounds = 1
    organization = SubFactory(
        'app.factories.DistrictFactory'
    )


class DistrictYouthAwardFactory(AwardFactory):
    kind = Award.KIND.youth
    championship_season = Award.SEASON.fall
    championship_rounds = 1
    is_primary = True
    # is_qualification_required = True
    # qualifier_season = Award.SEASON.spring
    # qualifier_rounds = 1d
    # threshold = 73
    # minimum = 61
    # advance = 70
    organization = SubFactory(
        'app.factories.DistrictFactory'
    )


class DivisionQuartetAwardFactory(AwardFactory):
    kind = Award.KIND.quartet
    championship_season = Award.SEASON.spring
    championship_rounds = 2
    is_primary = True
    is_qualification_required = False
    organization = SubFactory(
        'app.factories.DivisionFactory'
    )


class DivisionChorusAwardFactory(AwardFactory):
    kind = Award.KIND.chorus
    championship_season = Award.SEASON.spring
    championship_rounds = 1
    is_primary = True
    is_qualification_required = False
    organization = SubFactory(
        'app.factories.DivisionFactory'
    )


class DivisionSeniorsAwardFactory(AwardFactory):
    kind = Award.KIND.seniors
    championship_season = Award.SEASON.spring
    championship_rounds = 1
    is_primary = True
    is_qualification_required = False
    organization = SubFactory(
        'app.factories.DivisionFactory'
    )


class DivisionYouthAwardFactory(AwardFactory):
    kind = Award.KIND.youth
    championship_season = Award.SEASON.spring
    championship_rounds = 1
    is_primary = True
    is_qualification_required = False
    organization = SubFactory(
        'app.factories.DivisionFactory'
    )


# Chapters
class ChapterFactory(DjangoModelFactory):
    class Meta:
        model = Chapter
    status = Chapter.STATUS.active


class DistrictChapterFactory(ChapterFactory):
    name = Faker('city')
    organization = SubFactory(
        'app.factories.DistrictFactory',
    )


class AffiliateChapterFactory(ChapterFactory):
    name = 'Test Affiliate Chapter'
    organization = SubFactory(
        'app.factories.AffiliateFactory',
    )


# Groups
class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group
    name = Faker('company')
    status = Group.STATUS.active


class QuartetFactory(GroupFactory):
    kind = Group.KIND.quartet
    organization = SubFactory(
        'app.factories.DistrictFactory',
    )


class ChorusFactory(GroupFactory):
    kind = Group.KIND.chorus
    organization = SubFactory(
        'app.factories.DistrictFactory',
    )
    chapter = SubFactory(
        'app.factories.DistrictChapterFactory'
    )


# Organizations
class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization
        django_get_or_create = ('name', 'level', 'kind',)
    status = Organization.STATUS.active


class InternationalFactory(OrganizationFactory):
    level = Organization.LEVEL.international
    kind = Organization.KIND.international
    name = 'International'
    short_name = 'BHS'
    long_name = 'International'
    parent = None


class DistrictFactory(OrganizationFactory):
    level = Organization.LEVEL.district
    kind = Organization.KIND.district
    name = 'Test District'
    short_name = 'TDI'
    long_name = 'District'
    parent = SubFactory(
        'app.factories.InternationalFactory',
        name='International',
    )


class DivisionFactory(OrganizationFactory):
    level = Organization.LEVEL.division
    kind = Organization.KIND.division
    name = 'Test Division'
    short_name = 'TDV'
    long_name = 'Test'
    parent = SubFactory(
        'app.factories.DistrictFactory',
    )


class NoncompFactory(OrganizationFactory):
    level = Organization.LEVEL.district
    kind = Organization.KIND.noncomp
    name = 'Frank Thorne District'
    short_name = 'TNC'
    long_name = 'Frank Thorne'
    parent = SubFactory(
        'app.factories.InternationalFactory',
    )


class AffiliateFactory(OrganizationFactory):
    level = Organization.LEVEL.district
    kind = Organization.KIND.affiliate
    name = 'Test Affiliate'
    short_name = 'TAF'
    long_name = 'Affiliate'
    parent = SubFactory(
        'app.factories.InternationalFactory',
    )


# Persons
class PersonFactory(DjangoModelFactory):
    class Meta:
        model = Person
    status = Person.STATUS.active
    name = Faker('name_male')


# Venues
class VenueFactory(DjangoModelFactory):
    class Meta:
        model = Venue
    location = Faker('company')
    city = Faker('city')
    state = Faker('state')
    timezone = pytz.timezone('US/Central')


# Judges
class JudgeFactory(DjangoModelFactory):
    class Meta:
        model = Judge
    status = Judge.STATUS.active
    person = SubFactory(
        'app.factories.PersonFactory'
    )


class OfficialAdminJudgeFactory(JudgeFactory):
    category = Judge.CATEGORY.admin
    kind = Judge.KIND.certified


class OfficialMusicJudgeFactory(JudgeFactory):
    category = Judge.CATEGORY.music
    kind = Judge.KIND.certified


class OfficialPresentationJudgeFactory(JudgeFactory):
    category = Judge.CATEGORY.presentation
    kind = Judge.KIND.certified


class OfficialSingingJudgeFactory(JudgeFactory):
    category = Judge.CATEGORY.singing
    kind = Judge.KIND.certified


class CandidateAdminJudgeFactory(JudgeFactory):
    category = Judge.CATEGORY.admin
    kind = Judge.KIND.candidate


class CandidateMusicJudgeFactory(JudgeFactory):
    category = Judge.CATEGORY.music
    kind = Judge.KIND.candidate


class CandidatePresentationJudgeFactory(JudgeFactory):
    category = Judge.CATEGORY.presentation
    kind = Judge.KIND.candidate


class CandidateSingingJudgeFactory(JudgeFactory):
    category = Judge.CATEGORY.singing
    kind = Judge.KIND.candidate


# Assignments
class AssignmentFactory(DjangoModelFactory):
    class Meta:
        model = Assignment


# class InternationalQuartetOfficialAdminAssignmentFactory(AssignmentFactory):
#     session = SubFactory(
#         'app.factories.InternationalQuartetSessionFactory'
#     )
#     judge = SubFactory(
#         'app.factories.OfficialAdminJudgeFactory'
#     )


# class InternationalQuartetOfficialMusicAssignmentFactory(AssignmentFactory):
#     session = SubFactory(
#         'app.factories.InternationalQuartetSessionFactory'
#     )
#     judge = SubFactory(
#         'app.factories.OfficialMusicJudgeFactory'
#     )


# class InternationalQuartetOfficialPresentationAssignmentFactory(AssignmentFactory):
#     session = SubFactory(
#         'app.factories.InternationalQuartetSessionFactory'
#     )
#     judge = SubFactory(
#         'app.factories.OfficialPresentationJudgeFactory'
#     )


# class InternationalQuartetOfficialSingingAssignmentFactory(AssignmentFactory):
#     session = SubFactory(
#         'app.factories.InternationalQuartetSessionFactory'
#     )
#     judge = SubFactory(
#         'app.factories.OfficialSingingJudgeFactory'
#     )


# Submissions
class SubmissionFactory(DjangoModelFactory):
    class Meta:
        model = Submission
    status = Submission.STATUS.new
    performer = SubFactory(
        'app.factories.PerformerFactory'
    )


# Members
class MemberFactory(DjangoModelFactory):
    class Meta:
        model = Member

    status = Member.STATUS.active
    chapter = SubFactory(
        'app.factories.DistrictChapterFactory'
    )
    person = SubFactory(
        'app.factories.PersonFactory'
    )


# Roles
class RoleFactory(DjangoModelFactory):
    class Meta:
        model = Role

    status = Role.STATUS.active
    person = SubFactory(
        'app.factories.PersonFactory'
    )
    group = SubFactory(
        'app.factories.QuartetFactory'
    )


class TenorFactory(RoleFactory):
    part = Role.PART.tenor


class LeadFactory(RoleFactory):
    part = Role.PART.lead


class BaritoneFactory(RoleFactory):
    part = Role.PART.baritone


class BassFactory(RoleFactory):
    part = Role.PART.bass


# Conventions
class ConventionFactory(DjangoModelFactory):
    class Meta:
        model = Convention

    status = Convention.STATUS.new
    venue = SubFactory(
        'app.factories.VenueFactory'
    )


class SummerConventionFactory(ConventionFactory):
    kind = Convention.KIND.international
    season = Convention.SEASON.summer
    risers = [13, ]
    year = 2016
    date = DateTimeTZRange(
        lower=datetime(2016, 07, 01, 12, 00),
        upper=datetime(2016, 07, 04, 12, 00),
        bounds='[)',
    )
    organization = SubFactory(
        'app.factories.InternationalFactory',
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
        'app.factories.InternationalFactory',
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
    organization = SubFactory(
        'app.factories.DistrictFactory',
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
    organization = SubFactory(
        'app.factories.DistrictFactory',
    )


class RegionalConventionFactory(ConventionFactory):
    kind = Convention.KIND.fwdnenw
    season = Convention.SEASON.spring
    risers = [5, 7, 9, ]
    year = 2016
    date = DateTimeTZRange(
        lower=datetime(2016, 04, 01, 12, 00),
        upper=datetime(2016, 04, 02, 12, 00),
        bounds='[)',
    )
    organization = SubFactory(
        'app.factories.DistrictFactory',
    )


# Sessions
class SessionFactory(DjangoModelFactory):
    class Meta:
        model = Session
    status = Session.STATUS.new


class InternationalQuartetSessionFactory(SessionFactory):
    kind = Session.KIND.quartet
    convention = SubFactory(
        'app.factories.SummerConventionFactory',
    )


class InternationalChorusSessionFactory(SessionFactory):
    kind = Session.KIND.chorus
    convention = SubFactory(
        'app.factories.SummerConventionFactory',
    )


class InternationalSeniorsSessionFactory(SessionFactory):
    kind = Session.KIND.seniors
    convention = SubFactory(
        'app.factories.MidwinterConvention',
    )


class InternationalYouthSessionFactory(SessionFactory):
    kind = Session.KIND.youth
    convention = SubFactory(
        'app.factories.SummerConventionFactory',
    )


class QuartetSessionFactory(SessionFactory):
    kind = Session.KIND.quartet


class DistrictChorusSessionFactory(SessionFactory):
    kind = Session.KIND.chorus


# Contests
class ContestFactory(DjangoModelFactory):
    class Meta:
        model = Contest

    status = Contest.STATUS.new
    session = SubFactory(
        'app.factories.InternationalQuartetSessionFactory'
    )
    award = SubFactory(
        'app.factories.InternationalQuartetAwardFactory'
    )


# Rounds
class RoundFactory(DjangoModelFactory):
    class Meta:
        model = Round
    status = Round.STATUS.new


# Performers
class PerformerFactory(DjangoModelFactory):
    class Meta:
        model = Performer
    status = Performer.STATUS.new
    # representing = SubFactory(
    #     'app.factories.DistrictFactory'
    # )
    session = SubFactory(
        'app.factories.InternationalQuartetSessionFactory'
    )
    group = SubFactory(
        'app.factories.QuartetFactory'
    )


# Contestants
class ContestantFactory(DjangoModelFactory):
    class Meta:
        model = Contestant

    status = Contestant.STATUS.new
    performer = SubFactory(
        'app.factories.PerformerFactory'
    )
    contest = SubFactory(
        'app.factories.ContestFactory',
    )


# Performances
class PerformanceFactory(DjangoModelFactory):
    class Meta:
        model = Performance

    status = Performance.STATUS.new
    performer = SubFactory(
        'app.factories.PerformerFactory',
    )
    round = SubFactory(
        'app.factories.RoundFactory',
        # session=Iterator(Session.objects.all())
    )


# Slots
class SlotFactory(DjangoModelFactory):
    class Meta:
        model = Slot

    status = Slot.STATUS.new
    num = 1
    round = SubFactory(
        'app.factories.RoundFactory',
    )


# Songs
class SongFactory(DjangoModelFactory):
    class Meta:
        model = Song

    status = Performance.STATUS.new
    num = 1
    performance = SubFactory(
        'app.factories.PerformanceFactory',
    )


# Scores
class ScoreFactory(DjangoModelFactory):
    class Meta:
        model = Score

    status = Score.STATUS.new
    assignment = SubFactory(
        'app.factories.AssignmentFactory',
    )
    song = SubFactory(
        'app.factories.SongFactory',
        # performer=Performer.objects.all().first()
    )
    category = 1
    kind = 10
