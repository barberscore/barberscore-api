# Third-Party
from factory import (
    Faker,
    PostGenerationMethodCall,
    SubFactory,
)
from factory.django import (
    DjangoModelFactory,
    mute_signals,
)
from factory.fuzzy import FuzzyInteger

# Django
from django.db.models.signals import post_save

# First-Party
from api.models import (
    Appearance,
    Assignment,
    Award,
    Chart,
    Contest,
    Contestant,
    Convention,
    Entry,
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
    Slot,
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
    entry = SubFactory('api.factories.EntryFactory')
    slot = None

    class Meta:
        model = Appearance


class AssignmentFactory(DjangoModelFactory):
    status = Assignment.STATUS.active
    kind = Assignment.KIND.official
    category = Assignment.CATEGORY.drcj
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
    status = Chart.STATUS.new
    title = Faker('word')
    arrangers = Faker('name_male')
    composers = Faker('name_male')
    lyricists = Faker('name_male')

    class Meta:
        model = Chart


class ContestFactory(DjangoModelFactory):
    status = Contest.STATUS.new
    is_qualifier = False
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
    open_date = '2017-06-01'
    close_date = '2017-06-30'
    start_date = '2017-07-01'
    end_date = '2017-07-08'
    location = Faker('city')
    venue = SubFactory('api.factories.VenueFactory')
    organization = SubFactory('api.factories.OrganizationFactory')

    class Meta:
        model = Convention


class EntryFactory(DjangoModelFactory):
    status = Entry.STATUS.new
    image = None
    is_evaluation = True
    is_private = False
    session = SubFactory('api.factories.SessionFactory')
    group = SubFactory('api.factories.GroupFactory')

    class Meta:
        model = Entry


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
    image = None
    description = ''
    notes = ''
    bhs_id = FuzzyInteger(100000, 999999)
    organization = None

    class Meta:
        model = Group


class MemberFactory(DjangoModelFactory):
    status = Member.STATUS.new
    part = None
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
    image = None
    description = ''
    notes = ''
    bhs_id = FuzzyInteger(100000, 999999)
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
    member = SubFactory('api.factories.MemberFactory')

    class Meta:
        model = Participant


class PersonFactory(DjangoModelFactory):
    name = Faker('name_male')
    status = Person.STATUS.active
    birth_date = None
    location = ''
    website = ''
    facebook = ''
    twitter = ''
    email = Faker('email')
    phone = ''
    image = None
    description = ''
    notes = ''
    bhs_id = None

    class Meta:
        model = Person


class RepertoryFactory(DjangoModelFactory):
    status = Repertory.STATUS.new
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
    kind = Session.KIND.quartet
    is_invitational = False
    scoresheet = None
    convention = SubFactory('api.factories.ConventionFactory')

    class Meta:
        model = Session


class SlotFactory(DjangoModelFactory):
    status = Slot.STATUS.new
    num = 1
    location = ''
    round = SubFactory('api.factories.RoundFactory')

    class Meta:
        model = Slot


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
    location = ''
    city = '',
    state = ''
    airport = ''
    timezone = ''

    class Meta:
        model = Venue


@mute_signals(post_save)
class UserFactory(DjangoModelFactory):
    email = Faker('email')
    password = PostGenerationMethodCall('set_password', 'password')
    is_active = True
    is_staff = False
    person = SubFactory('api.factories.PersonFactory')

    class Meta:
        model = User
