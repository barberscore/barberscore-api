# Standard Libary
from datetime import datetime

# Third-Party
import pytz
from factory import (
    Faker,
    PostGenerationMethodCall,
    SubFactory,
)
from factory.django import (
    DjangoModelFactory,
    ImageField,
)

# First-Party
from app.models import (
    Assignment,
    Award,
    Catalog,
    Contest,
    ContestScore,
    Contestant,
    ContestantScore,
    Convention,
    Entity,
    Host,
    Membership,
    Office,
    Officer,
    Performance,
    PerformanceScore,
    Performer,
    PerformerScore,
    Person,
    Round,
    Score,
    Session,
    Slot,
    Song,
    SongScore,
    Submission,
    Venue,
    User,
)

# Primitives
class AssignmentFactory(DjangoModelFactory):
    status = Assignment.STATUS.new
    kind = Assignment.KIND.drcj
    convention = SubFactory('app.factories.ConventionFactory')
    person = SubFactory('app.factories.PersonFactory')

    class Meta:
        model = Assignment


class AwardFactory(DjangoModelFactory):
    name = 'Test Award'
    status = Award.STATUS.active
    kind = Award.KIND.quartet
    championship_season = Award.SEASON.summer
    qualifier_season = Award.SEASON.spring
    is_primary = True
    is_improved = False
    is_novice = False
    is_manual = False
    is_multi = True
    is_district_representative = True
    championship_rounds = 3
    qualifier_rounds = 2
    threshold = 76
    minimum = 70
    advance = 73
    entity = SubFactory(
        'app.factories.EntityFactory'
    )

    class Meta:
        model = Award


class CatalogFactory(DjangoModelFactory):
    status = Catalog.STATUS.new
    title = 'Test Title'

    class Meta:
        model = Catalog


class ContestFactory(DjangoModelFactory):
    status = Contest.STATUS.new
    is_qualifier = False
    session = SubFactory('app.factories.SessionFactory')
    award = SubFactory('app.factories.AwardFactory')

    class Meta:
        model = Contest


class ContestScoreFactory(DjangoModelFactory):
    champion = None

    class Meta:
        model = ContestScore


class ContestantFactory(DjangoModelFactory):
    status = Contestant.STATUS.new
    performer = SubFactory('app.factories.PerformerFactory')
    contest = SubFactory('app.factories.ContestFactory')

    class Meta:
        model = Contestant


class ContestantScoreFactory(DjangoModelFactory):
    class Meta:
        model = ContestantScore


class ConventionFactory(DjangoModelFactory):
    name = 'Test Convention'
    status = Convention.STATUS.new
    level = Convention.LEVEL.international
    season = Convention.SEASON.summer
    panel = Convention.PANEL.quintiple
    risers = [0, 13]
    year = 2017
    start_date = '2017-07-01'
    end_date = '2017-07-04'
    location = 'Nashville, TN'
    venue = None

    class Meta:
        model = Convention


class EntityFactory(DjangoModelFactory):
    name = 'Barbershop Harmony Society'
    status = Entity.STATUS.active
    kind = Entity.KIND.bhs
    age = None
    is_novice = False
    short_name = 'BHS'
    long_name = 'Barbershop Harmony Society'
    code = None
    start_date = None
    end_date = None
    location = 'Nashville, TN'
    website = 'http://barbershop.org'
    facebook = None
    twitter = None
    email = 'admin@barbershop.org'
    phone = '415.555.1212'
    picture = ImageField(color='blue')
    description = 'The society'
    notes = None
    bhs_id = None
    parent = None

    class Meta:
        model = Entity


class HostFactory(DjangoModelFactory):
    status = Host.STATUS.new
    convention = SubFactory('app.factories.ConventionFactory')
    entity = SubFactory('app.factories.EntityFactory')

    class Meta:
        model = Host


class MembershipFactory(DjangoModelFactory):
    status = Membership.STATUS.active
    part = None
    start_date = None
    end_date = None
    status = Host.STATUS.new
    entity = SubFactory('app.factories.EntityFactory')
    person = SubFactory('app.factories.PersonFactory')

    class Meta:
        model = Membership


class OfficeFactory(DjangoModelFactory):
    name = 'Test Office'
    status = Office.STATUS.active
    kind = Office.KIND.new
    short_name = 'TEST'
    long_name = 'Test Office'

    class Meta:
        model = Office


class OfficerFactory(DjangoModelFactory):
    status = Officer.STATUS.new
    start_date = None
    end_date = None
    office = SubFactory('app.factories.OfficeFactory')
    membership = SubFactory('app.factories.MembershipFactory')

    class Meta:
        model = Officer


class PerformanceFactory(DjangoModelFactory):
    status = Performance.STATUS.new
    num = None
    actual_start = None
    actual_finish = None
    round = SubFactory('app.factories.RoundFactory')
    performer = SubFactory('app.factories.PerformerFactory')
    slot = None

    class Meta:
        model = Performance


class PerformanceScoreFactory(DjangoModelFactory):
    class Meta:
        model = PerformanceScore


class PerformerFactory(DjangoModelFactory):
    status = Performer.STATUS.new
    picture = ImageField(color='green')
    men = None
    risers = None
    is_evaluation = True
    is_private = False
    session = SubFactory('app.factories.SessionFactory')
    entity = SubFactory('app.factories.EntityFactory')
    tenor = None
    lead = None
    baritone = None
    bass = None
    director = None
    codirector = None

    class Meta:
        model = Performance


class PerformerScoreFactory(DjangoModelFactory):
    class Meta:
        model = PerformerScore


class PersonFactory(DjangoModelFactory):
    name = 'Test Person'
    status = Person.STATUS.active
    kind = Person.KIND.new
    birth_date = None
    start_date = None
    end_date = None
    location = 'Nashville, TN'
    website = 'http://barbershop.org'
    facebook = None
    twitter = None
    email = 'admin@barbershop.org'
    phone = '415.555.1212'
    picture = ImageField(color='red')
    description = 'The society'
    notes = None
    bhs_id = None
    user = None

    class Meta:
        model = Person


class RoundFactory(DjangoModelFactory):
    status = Round.STATUS.new
    kind = Round.KIND.finals
    num = 1
    num_songs = 2
    start_date = None
    end_date = None
    ann_pdf = None
    session = SubFactory('app.factories.SessionFactory')

    class Meta:
        model = Round


class ScoreFactory(DjangoModelFactory):
    status = Score.STATUS.new
    category = Score.CATEGORY.music
    kind = Score.KIND.official
    points = 100
    original = None
    violation = None
    penalty = None
    is_flagged = None
    song = SubFactory('app.factories.SongFactory')
    person = None

    class Meta:
        model = Score


class SessionFactory(DjangoModelFactory):
    status = Session.STATUS.new
    kind = Session.KIND.quartet
    start_date = None
    end_date = None
    num_rounds = 1
    panel_size = None
    is_prelims = None
    cursor = None
    current = None
    primary = None
    scoresheet_pdf = None
    convention = SubFactory('app.factories.ConventionFactory')

    class Meta:
        model = Session


class SlotFactory(DjangoModelFactory):
    status = Slot.STATUS.new
    num = 1
    location = None
    round = SubFactory('app.factories.RoundFactory')

    class Meta:
        model = Slot


class SongFactory(DjangoModelFactory):
    status = Song.STATUS.new
    num = 1
    performance = SubFactory('app.factories.PerformanceFactory')
    submission = None

    class Meta:
        model = Song


class SongScoreFactory(DjangoModelFactory):
    class Meta:
        model = SongScore


class SubmissionFactory(DjangoModelFactory):
    status = Submission.STATUS.new
    title = 'Test Song Title'
    bhs_catalog = None
    is_medley = None
    is_parody = None
    arrangers = None
    composers = None
    holders = None
    performer = SubFactory('app.factories.PerformerFactory')
    catalog = None

    class Meta:
        model = Submission


class VenueFactory(DjangoModelFactory):
    name = 'Test Convention Center'
    status = Venue.STATUS.active
    location = 'Nashville, TN'
    city = 'Nashville',
    state = 'TN'
    airport = 'TNA'
    timezone = 'US/Central'

    class Meta:
        model = Venue


class UserFactory(DjangoModelFactory):
    username = 'test@barberscore.com'
    password = PostGenerationMethodCall('set_password', 'password')
    is_active = True
    is_staff = False

    class Meta:
        model = User


# Pre-Built Factories
# # Users
# class AdminFactory(UserFactory):
#     email = 'admin@barberscore.com'
#     password = PostGenerationMethodCall('set_password', 'password')
#     name = 'Admin User'
#     is_staff = True


# class PublicFactory(UserFactory):
#     email = 'user@barberscore.com'
#     password = PostGenerationMethodCall('set_password', 'password')
#     name = 'Public User'


# # Awards
# class AwardFactory(DjangoModelFactory):
#     class Meta:
#         model = Award
#     status = Award.STATUS.active


# class InternationalQuartetAwardFactory(AwardFactory):
#     kind = Award.KIND.quartet
#     championship_season = Award.SEASON.summer
#     championship_rounds = 3
#     is_primary = True
#     is_qualification_required = True
#     qualifier_season = Award.SEASON.spring
#     qualifier_rounds = 2
#     threshold = 76
#     minimum = 70
#     advance = 73
#     organization = SubFactory(
#         'app.factories.InternationalFactory'
#     )


# class InternationalChorusAwardFactory(AwardFactory):
#     kind = Award.KIND.chorus
#     championship_season = Award.SEASON.summer
#     championship_rounds = 1
#     is_primary = True
#     is_qualification_required = True
#     qualifier_season = Award.SEASON.fall
#     qualifier_rounds = 1
#     organization = SubFactory(
#         'app.factories.InternationalFactory'
#     )


# class InternationalSeniorsAwardFactory(AwardFactory):
#     kind = Award.KIND.seniors
#     championship_season = Award.SEASON.midwinter
#     championship_rounds = 1
#     is_primary = True
#     is_qualification_required = True
#     qualifier_season = Award.SEASON.spring
#     qualifier_rounds = 1
#     organization = SubFactory(
#         'app.factories.InternationalFactory'
#     )


# class InternationalYouthAwardFactory(AwardFactory):
#     kind = Award.KIND.youth
#     championship_season = Award.SEASON.summer
#     championship_rounds = 1
#     is_primary = True
#     is_qualification_required = True
#     qualifier_season = Award.SEASON.spring
#     qualifier_rounds = 1
#     threshold = 73
#     minimum = 61
#     advance = 70
#     organization = SubFactory(
#         'app.factories.InternationalFactory'
#     )


# class DistrictQuartetAwardFactory(AwardFactory):
#     kind = Award.KIND.quartet
#     championship_season = Award.SEASON.fall
#     championship_rounds = 2
#     is_primary = True
#     # is_qualification_required = True
#     # qualifier_season = Award.SEASON.spring
#     # qualifier_rounds = 2
#     # threshold = 76
#     # minimum = 70
#     # advance = 73
#     organization = SubFactory(
#         'app.factories.DistrictFactory'
#     )


# class DistrictChorusAwardFactory(AwardFactory):
#     kind = Award.KIND.chorus
#     championship_season = Award.SEASON.spring
#     championship_rounds = 1
#     is_primary = True
#     # is_qualification_required = True
#     # qualifier_season = Award.SEASON.fall
#     # qualifier_rounds = 1
#     organization = SubFactory(
#         'app.factories.DistrictFactory'
#     )


# class DistrictSeniorsAwardFactory(AwardFactory):
#     kind = Award.KIND.seniors
#     championship_season = Award.SEASON.fall
#     championship_rounds = 1
#     is_primary = True
#     # is_qualification_required = True
#     # qualifier_season = Award.SEASON.spring
#     # qualifier_rounds = 1
#     organization = SubFactory(
#         'app.factories.DistrictFactory'
#     )


# class DistrictYouthAwardFactory(AwardFactory):
#     kind = Award.KIND.youth
#     championship_season = Award.SEASON.fall
#     championship_rounds = 1
#     is_primary = True
#     # is_qualification_required = True
#     # qualifier_season = Award.SEASON.spring
#     # qualifier_rounds = 1d
#     # threshold = 73
#     # minimum = 61
#     # advance = 70
#     organization = SubFactory(
#         'app.factories.DistrictFactory'
#     )


# class DivisionQuartetAwardFactory(AwardFactory):
#     kind = Award.KIND.quartet
#     championship_season = Award.SEASON.spring
#     championship_rounds = 2
#     is_primary = True
#     is_qualification_required = False
#     organization = SubFactory(
#         'app.factories.DivisionFactory'
#     )


# class DivisionChorusAwardFactory(AwardFactory):
#     kind = Award.KIND.chorus
#     championship_season = Award.SEASON.spring
#     championship_rounds = 1
#     is_primary = True
#     is_qualification_required = False
#     organization = SubFactory(
#         'app.factories.DivisionFactory'
#     )


# class DivisionSeniorsAwardFactory(AwardFactory):
#     kind = Award.KIND.seniors
#     championship_season = Award.SEASON.spring
#     championship_rounds = 1
#     is_primary = True
#     is_qualification_required = False
#     organization = SubFactory(
#         'app.factories.DivisionFactory'
#     )


# class DivisionYouthAwardFactory(AwardFactory):
#     kind = Award.KIND.youth
#     championship_season = Award.SEASON.spring
#     championship_rounds = 1
#     is_primary = True
#     is_qualification_required = False
#     organization = SubFactory(
#         'app.factories.DivisionFactory'
#     )


# # Chapters
# class ChapterFactory(DjangoModelFactory):
#     class Meta:
#         model = Chapter
#     status = Chapter.STATUS.active


# class DistrictChapterFactory(ChapterFactory):
#     name = Faker('city')
#     organization = SubFactory(
#         'app.factories.DistrictFactory',
#     )


# class AffiliateChapterFactory(ChapterFactory):
#     name = 'Test Affiliate Chapter'
#     organization = SubFactory(
#         'app.factories.AffiliateFactory',
#     )


# # Groups
# class GroupFactory(DjangoModelFactory):
#     class Meta:
#         model = Group
#     name = Faker('company')
#     status = Group.STATUS.active


# class QuartetFactory(GroupFactory):
#     kind = Group.KIND.quartet
#     organization = SubFactory(
#         'app.factories.DistrictFactory',
#     )


# class ChorusFactory(GroupFactory):
#     kind = Group.KIND.chorus
#     organization = SubFactory(
#         'app.factories.DistrictFactory',
#     )
#     chapter = SubFactory(
#         'app.factories.DistrictChapterFactory'
#     )


# # Organizations
# class OrganizationFactory(DjangoModelFactory):
#     class Meta:
#         model = Organization
#         django_get_or_create = ('name', 'level', 'kind',)
#     status = Organization.STATUS.active


# class InternationalFactory(OrganizationFactory):
#     level = Organization.LEVEL.international
#     kind = Organization.KIND.international
#     name = 'International'
#     short_name = 'BHS'
#     long_name = 'International'
#     parent = None


# class DistrictFactory(OrganizationFactory):
#     level = Organization.LEVEL.district
#     kind = Organization.KIND.district
#     name = 'Test District'
#     short_name = 'TDI'
#     long_name = 'District'
#     parent = SubFactory(
#         'app.factories.InternationalFactory',
#         name='International',
#     )


# class DivisionFactory(OrganizationFactory):
#     level = Organization.LEVEL.division
#     kind = Organization.KIND.division
#     name = 'Test Division'
#     short_name = 'TDV'
#     long_name = 'Test'
#     parent = SubFactory(
#         'app.factories.DistrictFactory',
#     )


# class NoncompFactory(OrganizationFactory):
#     level = Organization.LEVEL.district
#     kind = Organization.KIND.noncomp
#     name = 'Frank Thorne District'
#     short_name = 'TNC'
#     long_name = 'Frank Thorne'
#     parent = SubFactory(
#         'app.factories.InternationalFactory',
#     )


# class AffiliateFactory(OrganizationFactory):
#     level = Organization.LEVEL.district
#     kind = Organization.KIND.affiliate
#     name = 'Test Affiliate'
#     short_name = 'TAF'
#     long_name = 'Affiliate'
#     parent = SubFactory(
#         'app.factories.InternationalFactory',
#     )


# # Persons
# class PersonFactory(DjangoModelFactory):
#     class Meta:
#         model = Person
#     status = Person.STATUS.active
#     name = Faker('name_male')


# # Venues
# class VenueFactory(DjangoModelFactory):
#     class Meta:
#         model = Venue
#     location = Faker('company')
#     city = Faker('city')
#     state = Faker('state')
#     timezone = pytz.timezone('US/Central')


# # Judges
# class JudgeFactory(DjangoModelFactory):
#     class Meta:
#         model = Judge
#     status = Judge.STATUS.active
#     person = SubFactory(
#         'app.factories.PersonFactory'
#     )


# class OfficialAdminJudgeFactory(JudgeFactory):
#     category = Judge.CATEGORY.admin
#     kind = Judge.KIND.certified


# class OfficialMusicJudgeFactory(JudgeFactory):
#     category = Judge.CATEGORY.music
#     kind = Judge.KIND.certified


# class OfficialPresentationJudgeFactory(JudgeFactory):
#     category = Judge.CATEGORY.presentation
#     kind = Judge.KIND.certified


# class OfficialSingingJudgeFactory(JudgeFactory):
#     category = Judge.CATEGORY.singing
#     kind = Judge.KIND.certified


# class CandidateAdminJudgeFactory(JudgeFactory):
#     category = Judge.CATEGORY.admin
#     kind = Judge.KIND.candidate


# class CandidateMusicJudgeFactory(JudgeFactory):
#     category = Judge.CATEGORY.music
#     kind = Judge.KIND.candidate


# class CandidatePresentationJudgeFactory(JudgeFactory):
#     category = Judge.CATEGORY.presentation
#     kind = Judge.KIND.candidate


# class CandidateSingingJudgeFactory(JudgeFactory):
#     category = Judge.CATEGORY.singing
#     kind = Judge.KIND.candidate


# # Assignments
# class AssignmentFactory(DjangoModelFactory):
#     class Meta:
#         model = Assignment


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


# # Submissions
# class SubmissionFactory(DjangoModelFactory):
#     class Meta:
#         model = Submission
#     status = Submission.STATUS.new
#     performer = SubFactory(
#         'app.factories.PerformerFactory'
#     )


# # Members
# class MemberFactory(DjangoModelFactory):
#     class Meta:
#         model = Member

#     status = Member.STATUS.active
#     chapter = SubFactory(
#         'app.factories.DistrictChapterFactory'
#     )
#     person = SubFactory(
#         'app.factories.PersonFactory'
#     )


# # Roles
# class RoleFactory(DjangoModelFactory):
#     class Meta:
#         model = Role

#     status = Role.STATUS.active
#     person = SubFactory(
#         'app.factories.PersonFactory'
#     )
#     group = SubFactory(
#         'app.factories.QuartetFactory'
#     )


# class TenorFactory(RoleFactory):
#     part = Role.PART.tenor


# class LeadFactory(RoleFactory):
#     part = Role.PART.lead


# class BaritoneFactory(RoleFactory):
#     part = Role.PART.baritone


# class BassFactory(RoleFactory):
#     part = Role.PART.bass


# # Conventions
# class ConventionFactory(DjangoModelFactory):
#     class Meta:
#         model = Convention

#     status = Convention.STATUS.new
#     venue = SubFactory(
#         'app.factories.VenueFactory'
#     )


# class SummerConventionFactory(ConventionFactory):
#     kind = Convention.KIND.international
#     season = Convention.SEASON.summer
#     risers = [13, ]
#     year = 2016
#     date = DateTimeTZRange(
#         lower=datetime(2016, 07, 01, 12, 00),
#         upper=datetime(2016, 07, 04, 12, 00),
#         bounds='[)',
#     )
#     organization = SubFactory(
#         'app.factories.InternationalFactory',
#     )


# class MidwinterConventionFactory(ConventionFactory):
#     kind = Convention.KIND.international
#     season = Convention.SEASON.midwinter
#     risers = [0, ]
#     year = 2016
#     date = DateTimeTZRange(
#         lower=datetime(2016, 01, 29, 12, 00),
#         upper=datetime(2016, 01, 30, 12, 00),
#         bounds='[)',
#     )
#     organization = SubFactory(
#         'app.factories.InternationalFactory',
#     )


# class SpringConventionFactory(ConventionFactory):
#     kind = Convention.KIND.district
#     season = Convention.SEASON.spring
#     risers = [5, 7, 9, ]
#     year = 2016
#     date = DateTimeTZRange(
#         lower=datetime(2016, 04, 01, 12, 00),
#         upper=datetime(2016, 04, 02, 12, 00),
#         bounds='[)',
#     )
#     organization = SubFactory(
#         'app.factories.DistrictFactory',
#     )


# class FallConventionFactory(ConventionFactory):
#     kind = Convention.KIND.district
#     season = Convention.SEASON.fall
#     risers = [5, 7, 9, ]
#     year = 2016
#     date = DateTimeTZRange(
#         lower=datetime(2016, 10, 01, 12, 00),
#         upper=datetime(2016, 10, 02, 12, 00),
#         bounds='[)',
#     )
#     organization = SubFactory(
#         'app.factories.DistrictFactory',
#     )


# class RegionalConventionFactory(ConventionFactory):
#     kind = Convention.KIND.fwdnenw
#     season = Convention.SEASON.spring
#     risers = [5, 7, 9, ]
#     year = 2016
#     date = DateTimeTZRange(
#         lower=datetime(2016, 04, 01, 12, 00),
#         upper=datetime(2016, 04, 02, 12, 00),
#         bounds='[)',
#     )
#     organization = SubFactory(
#         'app.factories.DistrictFactory',
#     )


# # Sessions
# class SessionFactory(DjangoModelFactory):
#     class Meta:
#         model = Session
#     status = Session.STATUS.new


# class InternationalQuartetSessionFactory(SessionFactory):
#     kind = Session.KIND.quartet
#     convention = SubFactory(
#         'app.factories.SummerConventionFactory',
#     )


# class InternationalChorusSessionFactory(SessionFactory):
#     kind = Session.KIND.chorus
#     convention = SubFactory(
#         'app.factories.SummerConventionFactory',
#     )


# class InternationalSeniorsSessionFactory(SessionFactory):
#     kind = Session.KIND.seniors
#     convention = SubFactory(
#         'app.factories.MidwinterConvention',
#     )


# class InternationalYouthSessionFactory(SessionFactory):
#     kind = Session.KIND.youth
#     convention = SubFactory(
#         'app.factories.SummerConventionFactory',
#     )


# class QuartetSessionFactory(SessionFactory):
#     kind = Session.KIND.quartet


# class DistrictChorusSessionFactory(SessionFactory):
#     kind = Session.KIND.chorus


# # Contests
# class ContestFactory(DjangoModelFactory):
#     class Meta:
#         model = Contest

#     status = Contest.STATUS.new
#     session = SubFactory(
#         'app.factories.InternationalQuartetSessionFactory'
#     )
#     award = SubFactory(
#         'app.factories.InternationalQuartetAwardFactory'
#     )


# # Rounds
# class RoundFactory(DjangoModelFactory):
#     class Meta:
#         model = Round
#     status = Round.STATUS.new


# # Performers
# class PerformerFactory(DjangoModelFactory):
#     class Meta:
#         model = Performer
#     status = Performer.STATUS.new
#     # representing = SubFactory(
#     #     'app.factories.DistrictFactory'
#     # )
#     session = SubFactory(
#         'app.factories.InternationalQuartetSessionFactory'
#     )
#     group = SubFactory(
#         'app.factories.QuartetFactory'
#     )


# # Contestants
# class ContestantFactory(DjangoModelFactory):
#     class Meta:
#         model = Contestant

#     status = Contestant.STATUS.new
#     performer = SubFactory(
#         'app.factories.PerformerFactory'
#     )
#     contest = SubFactory(
#         'app.factories.ContestFactory',
#     )


# # Performances
# class PerformanceFactory(DjangoModelFactory):
#     class Meta:
#         model = Performance

#     status = Performance.STATUS.new
#     performer = SubFactory(
#         'app.factories.PerformerFactory',
#     )
#     round = SubFactory(
#         'app.factories.RoundFactory',
#         # session=Iterator(Session.objects.all())
#     )


# # Slots
# class SlotFactory(DjangoModelFactory):
#     class Meta:
#         model = Slot

#     status = Slot.STATUS.new
#     num = 1
#     round = SubFactory(
#         'app.factories.RoundFactory',
#     )


# # Songs
# class SongFactory(DjangoModelFactory):
#     class Meta:
#         model = Song

#     status = Performance.STATUS.new
#     num = 1
#     performance = SubFactory(
#         'app.factories.PerformanceFactory',
#     )


# # Scores
# class ScoreFactory(DjangoModelFactory):
#     class Meta:
#         model = Score

#     status = Score.STATUS.new
#     assignment = SubFactory(
#         'app.factories.AssignmentFactory',
#     )
#     song = SubFactory(
#         'app.factories.SongFactory',
#         # performer=Performer.objects.all().first()
#     )
#     category = 1
#     kind = 10
