# Third-Party
import datetime
from factory import (
    Faker,
    PostGenerationMethodCall,
    LazyAttribute,
    Sequence,
    SubFactory,
    Iterator,
    # post_generation,
)
from factory.django import (
    DjangoModelFactory,
)
from factory.fuzzy import FuzzyInteger

# First-Party
from api.models import (
    Appearance,
    Assignment,
    Award,
    Chart,
    Contest,
    Contestant,
    Convention,
    Competitor,
    Enrollment,
    Entry,
    Grantor,
    Grid,
    Group,
    Member,
    Office,
    Officer,
    Organization,
    Panelist,
    Participant,
    Person,
    Repertory,
    Round,
    Score,
    Session,
    Song,
    User,
    Venue,
)


class AppearanceFactory(DjangoModelFactory):
    status = Appearance.STATUS.new
    num = None
    actual_start = None
    actual_finish = None
    round = SubFactory('api.factories.RoundFactory')
    competitor = SubFactory('api.factories.CompetitorFactory')

    class Meta:
        model = Appearance


class AssignmentFactory(DjangoModelFactory):
    status = Assignment.STATUS.confirmed
    kind = Assignment.KIND.official
    convention = SubFactory('api.factories.ConventionFactory')
    person = SubFactory('api.factories.PersonFactory')

    class Meta:
        model = Assignment


class AwardFactory(DjangoModelFactory):
    name = Faker('word')
    status = Award.STATUS.active
    kind = Award.KIND.quartet
    level = Award.LEVEL.championship
    season = Award.SEASON.summer
    is_primary = True
    is_invitational = True
    is_manual = False
    rounds = 3
    threshold = None
    minimum = None
    advance = None
    organization = SubFactory('api.factories.OrganizationFactory')

    class Meta:
        model = Award


class ChartFactory(DjangoModelFactory):
    status = Chart.STATUS.active
    title = Faker('word')
    arrangers = Faker('name_male')
    composers = Faker('name_male')
    lyricists = Faker('name_male')

    class Meta:
        model = Chart


class ContestFactory(DjangoModelFactory):
    status = Contest.STATUS.included
    session = SubFactory('api.factories.SessionFactory')
    award = SubFactory('api.factories.AwardFactory')

    class Meta:
        model = Contest


class ContestantFactory(DjangoModelFactory):
    status = Contestant.STATUS.new
    entry = SubFactory('api.factories.EntryFactory')
    contest = SubFactory('api.factories.ContestFactory')

    class Meta:
        model = Contestant


class ConventionFactory(DjangoModelFactory):
    name = Faker('city')
    status = Convention.STATUS.new
    season = Convention.SEASON.summer
    panel = Convention.PANEL.quintiple
    year = 2017
    open_date = datetime.date(2017, 6, 1)
    close_date = datetime.date(2017, 6, 30)
    start_date = datetime.date(2017, 7, 1)
    end_date = datetime.date(2017, 7, 8)
    location = Faker('city')
    venue = SubFactory('api.factories.VenueFactory')
    organization = SubFactory('api.factories.OrganizationFactory')

    class Meta:
        model = Convention

    # @post_generation
    # def create_assignments(self, create, extracted, **kwargs):
    #     if create:
    #         AssignmentFactory(
    #             convention=self,
    #             category=Assignment.CATEGORY.drcj,
    #         )
    #         AssignmentFactory(
    #             convention=self,
    #             category=Assignment.CATEGORY.ca,
    #         )
    #         for i in range(self.panel):
    #             AssignmentFactory(
    #                 convention=self,
    #                 category=Assignment.CATEGORY.music,
    #             )
    #             AssignmentFactory(
    #                 convention=self,
    #                 category=Assignment.CATEGORY.performance,
    #             )
    #             AssignmentFactory(
    #                 convention=self,
    #                 category=Assignment.CATEGORY.singing,
    #             )


class CompetitorFactory(DjangoModelFactory):
    status = Competitor.STATUS.new
    is_archived = False
    img = None
    session = SubFactory('api.factories.SessionFactory')
    group = SubFactory('api.factories.GroupFactory')

    class Meta:
        model = Competitor


class EnrollmentFactory(DjangoModelFactory):
    status = Enrollment.STATUS.active
    organization = SubFactory('api.factories.OrganizationFactory')
    person = SubFactory('api.factories.PersonFactory')

    class Meta:
        model = Enrollment


class EntryFactory(DjangoModelFactory):
    status = Entry.STATUS.new
    is_archived = False
    is_evaluation = True
    is_private = False
    session = SubFactory('api.factories.SessionFactory')
    group = SubFactory('api.factories.GroupFactory')

    class Meta:
        model = Entry


class GrantorFactory(DjangoModelFactory):
    status = Grantor.STATUS.new
    convention = SubFactory('api.factories.ConventionFactory')
    organization = SubFactory('api.factories.OrganizationFactory')

    class Meta:
        model = Grantor


class GridFactory(DjangoModelFactory):
    status = Grid.STATUS.new
    competitor = SubFactory('api.factories.CompetitorFactory')
    round = SubFactory('api.factories.RoundFactory')

    class Meta:
        model = Grid


class GroupFactory(DjangoModelFactory):
    name = Faker('company')
    status = Group.STATUS.active
    kind = Group.KIND.quartet
    short_name = Faker('word')
    code = ''
    start_date = None
    end_date = None
    email = Faker('email')
    phone = Faker('phone_number')
    location = ''
    website = ''
    facebook = ''
    twitter = ''
    img = None
    description = ''
    notes = ''
    bhs_id = Sequence(lambda x: x)
    organization = None

    class Meta:
        model = Group

    # @post_generation
    # def create_members(self, create, extracted, **kwargs):
    #     if create:
    #         if self.kind == self.KIND.quartet:
    #             size = 4
    #         else:
    #             size = 20
    #         for i in range(size):
    #             MemberFactory.create(group=self)

    # @post_generation
    # def create_repertories(self, create, extracted, **kwargs):
    #     if create:
    #         for i in range(6):
    #             RepertoryFactory.create(group=self)


class MemberFactory(DjangoModelFactory):
    status = Member.STATUS.active
    part = Iterator([
        Member.PART.tenor,
        Member.PART.lead,
        Member.PART.baritone,
        Member.PART.bass,
    ])
    start_date = None
    end_date = None
    group = SubFactory('api.factories.GroupFactory')
    person = SubFactory('api.factories.PersonFactory')

    class Meta:
        model = Member


class OfficeFactory(DjangoModelFactory):
    name = Faker('word')
    status = Office.STATUS.active
    kind = Office.KIND.international
    short_name = Faker('word')

    class Meta:
        model = Office


class OfficerFactory(DjangoModelFactory):
    status = Officer.STATUS.new
    start_date = None
    end_date = None
    office = SubFactory('api.factories.OfficeFactory')
    person = SubFactory('api.factories.PersonFactory')
    organization = SubFactory('api.factories.OrganizationFactory')

    class Meta:
        model = Officer


class OrganizationFactory(DjangoModelFactory):
    name = Faker('company')
    status = Organization.STATUS.active
    kind = Organization.KIND.international
    code = ''
    start_date = None
    end_date = None
    email = Faker('email')
    phone = Faker('phone_number')
    location = ''
    website = ''
    facebook = ''
    twitter = ''
    img = None
    description = ''
    notes = ''
    bhs_id = Sequence(lambda x: x)
    parent = None

    class Meta:
        model = Organization


class PanelistFactory(DjangoModelFactory):
    status = Panelist.STATUS.new
    kind = Panelist.KIND.official
    category = Panelist.CATEGORY.drcj
    round = SubFactory('api.factories.RoundFactory')
    person = SubFactory('api.factories.PersonFactory')

    class Meta:
        model = Panelist


class ParticipantFactory(DjangoModelFactory):
    status = Contestant.STATUS.new
    entry = SubFactory('api.factories.EntryFactory')
    person = SubFactory('api.factories.PersonFactory')

    class Meta:
        model = Participant


class PersonFactory(DjangoModelFactory):
    # name = Faker('name_male')
    first_name = Faker('first_name_male')
    middle_name = ''
    last_name = Faker('last_name_male')
    nick_name = ''
    status = Person.STATUS.active
    birth_date = None
    location = ''
    website = ''
    facebook = ''
    twitter = ''
    email = LazyAttribute(lambda x: '{0}@barberscore.com'.format(x.bhs_id))
    phone = ''
    img = None
    description = ''
    notes = ''
    current_through = '2018-12-31'
    bhs_id = Sequence(lambda x: '1{0:05d}'.format(x))

    class Meta:
        model = Person


class RepertoryFactory(DjangoModelFactory):
    status = Repertory.STATUS.active
    group = SubFactory('api.factories.GroupFactory')
    chart = SubFactory('api.factories.ChartFactory')

    class Meta:
        model = Repertory


class RoundFactory(DjangoModelFactory):
    status = Round.STATUS.new
    kind = Round.KIND.finals
    num = 1
    session = SubFactory('api.factories.SessionFactory')

    class Meta:
        model = Round


class ScoreFactory(DjangoModelFactory):
    status = Score.STATUS.new
    category = Score.CATEGORY.music
    kind = Score.KIND.official
    points = FuzzyInteger(50, 90)
    original = None
    violation = None
    penalty = None
    is_flagged = False
    song = SubFactory('api.factories.SongFactory')
    panelist = None

    class Meta:
        model = Score


class SessionFactory(DjangoModelFactory):
    status = Session.STATUS.new
    is_archived = False
    kind = Session.KIND.quartet
    is_invitational = False
    num_rounds = 2
    convention = SubFactory('api.factories.ConventionFactory')

    class Meta:
        model = Session

    # @post_generation
    # def create_contests(self, create, extracted, **kwargs):
    #     if create:
    #         for grantor in self.convention.grantors.all():
    #             for award in grantor.organization.awards.all():
    #                 ContestFactory(
    #                     session=self,
    #                     award=award,
    #                     status=Contest.STATUS.included,
    #                 )

    # @post_generation
    # def create_rounds(self, create, extracted, **kwargs):
    #     if create:
    #         for i in range(self.num_rounds):
    #             num = i + 1
    #             kind = self.num_rounds - i
    #             RoundFactory(
    #                 session=self,
    #                 num=num,
    #                 kind=kind,
    #             )


class SongFactory(DjangoModelFactory):
    status = Song.STATUS.new
    num = 1
    appearance = SubFactory('api.factories.AppearanceFactory')
    chart = None

    class Meta:
        model = Song


class VenueFactory(DjangoModelFactory):
    name = 'Test Convention Center'
    status = Venue.STATUS.active
    location = 'Nashville, TN'
    city = 'Nashville'
    state = 'TN'
    airport = 'NTA'
    timezone = 'US/Central'

    class Meta:
        model = Venue


class UserFactory(DjangoModelFactory):
    name = Faker('name_male')
    status = User.STATUS.active
    email = Sequence(lambda x: '{0:#}@barberscore.com'.format(x))
    password = PostGenerationMethodCall('set_password', 'password')
    is_active = False
    is_staff = False

    class Meta:
        model = User
