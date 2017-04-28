# Third-Party
from factory import (
    PostGenerationMethodCall,
    SubFactory,
)
from factory.django import (
    DjangoModelFactory,
    mute_signals,
)

# Django
from django.db.models.signals import post_save

# First-Party
from app.models import (
    Appearance,
    Assignment,
    Award,
    Chart,
    Contest,
    Contestant,
    Convention,
    Entity,
    Entry,
    Member,
    Office,
    Officer,
    Person,
    Repertory,
    Round,
    Score,
    Session,
    Slot,
    Song,
    Submission,
    User,
    Venue,
)


class AssignmentFactory(DjangoModelFactory):
    status = Assignment.STATUS.new
    kind = Assignment.KIND.official
    category = Assignment.CATEGORY.drcj
    convention = SubFactory('app.factories.ConventionFactory')
    person = SubFactory('app.factories.PersonFactory')

    class Meta:
        model = Assignment


class AwardFactory(DjangoModelFactory):
    name = 'Test Award'
    status = Award.STATUS.active
    kind = Award.KIND.quartet
    season = Award.SEASON.summer
    is_primary = True
    is_improved = False
    is_novice = False
    is_manual = False
    is_multi = True
    is_district_representative = True
    rounds = 3
    threshold = 76
    minimum = 70
    advance = 73
    entity = SubFactory(
        'app.factories.InternationalFactory'
    )

    class Meta:
        model = Award


class ChartFactory(DjangoModelFactory):
    status = Chart.STATUS.new
    title = 'Test Title'
    bhs_id = 999999

    class Meta:
        model = Chart


class ContestFactory(DjangoModelFactory):
    status = Contest.STATUS.new
    is_qualifier = False
    session = SubFactory('app.factories.SessionFactory')
    award = SubFactory('app.factories.AwardFactory')

    class Meta:
        model = Contest


class ContestantFactory(DjangoModelFactory):
    status = Contestant.STATUS.new
    entry = SubFactory('app.factories.EntryFactory')
    contest = SubFactory('app.factories.ContestFactory')

    class Meta:
        model = Contestant


class ConventionFactory(DjangoModelFactory):
    name = 'Test Convention'
    status = Convention.STATUS.new
    level = Convention.LEVEL.international
    season = Convention.SEASON.summer
    panel = Convention.PANEL.quintiple
    risers = [0, 13]
    year = 2017
    open_date = None
    close_date = None
    start_date = None
    end_date = None
    location = ''
    venue = None
    entity = SubFactory('app.factories.InternationalFactory')

    class Meta:
        model = Convention


class EntityFactory(DjangoModelFactory):

    class Meta:
        model = Entity


class InternationalFactory(EntityFactory):
    name = 'Test International'
    status = Entity.STATUS.active
    kind = Entity.KIND.international
    age = None
    is_novice = False
    short_name = 'Test ORG'
    long_name = 'Test International'
    code = ''
    start_date = None
    end_date = None
    location = ''
    website = ''
    facebook = ''
    twitter = ''
    email = ''
    phone = ''
    image = None
    description = ''
    notes = ''
    bhs_id = None
    parent = None


class DistrictFactory(EntityFactory):
    name = 'Test District'
    status = Entity.STATUS.active
    kind = Entity.KIND.district
    age = None
    is_novice = False
    short_name = 'Test DIS'
    long_name = 'Test District'
    code = ''
    start_date = None
    end_date = None
    location = ''
    website = ''
    facebook = ''
    twitter = ''
    email = ''
    phone = ''
    image = None
    description = ''
    notes = ''
    bhs_id = None
    parent = SubFactory('app.factories.InternationalFactory')


class QuartetFactory(EntityFactory):
    name = 'Test Quartet'
    status = Entity.STATUS.active
    kind = Entity.KIND.quartet
    age = None
    is_novice = False
    short_name = 'Test QRT'
    long_name = 'Test Quartet'
    code = ''
    start_date = None
    end_date = None
    location = ''
    website = ''
    facebook = ''
    twitter = ''
    email = ''
    phone = ''
    image = None
    description = ''
    notes = ''
    bhs_id = None
    parent = SubFactory('app.factories.DistrictFactory')


class MemberFactory(DjangoModelFactory):
    status = Member.STATUS.active
    part = None
    start_date = None
    end_date = None
    status = Member.STATUS.new
    entity = SubFactory('app.factories.InternationalFactory')
    person = SubFactory('app.factories.PersonFactory')

    class Meta:
        model = Member


class OfficeFactory(DjangoModelFactory):
    name = 'Test Office'
    status = Office.STATUS.active
    kind = Office.KIND.international
    short_name = 'TEST'
    long_name = 'Test Office'

    class Meta:
        model = Office


class OfficerFactory(DjangoModelFactory):
    status = Officer.STATUS.new
    start_date = None
    end_date = None
    office = SubFactory('app.factories.OfficeFactory')
    person = SubFactory('app.factories.PersonFactory')
    entity = None

    class Meta:
        model = Officer


class AppearanceFactory(DjangoModelFactory):
    status = Appearance.STATUS.new
    num = None
    actual_start = None
    actual_finish = None
    round = SubFactory('app.factories.RoundFactory')
    entry = SubFactory('app.factories.EntryFactory')
    slot = None

    class Meta:
        model = Appearance


class EntryFactory(DjangoModelFactory):
    status = Entry.STATUS.new
    image = None
    men = None
    risers = None
    is_evaluation = True
    is_private = False
    session = SubFactory('app.factories.SessionFactory')
    entity = SubFactory('app.factories.QuartetFactory')
    tenor = None
    lead = None
    baritone = None
    bass = None
    director = None
    codirector = None

    class Meta:
        model = Entry


class PersonFactory(DjangoModelFactory):
    name = 'Test Person'
    status = Person.STATUS.active
    kind = Person.KIND.new
    birth_date = None
    start_date = None
    end_date = None
    location = ''
    website = ''
    facebook = ''
    twitter = ''
    email = ''
    phone = ''
    image = None
    description = ''
    notes = ''
    bhs_id = None
    user = None

    class Meta:
        model = Person


class RepertoryFactory(DjangoModelFactory):
    status = Repertory.STATUS.new
    entity = SubFactory('app.factories.QuartetFactory')
    chart = SubFactory('app.factories.ChartFactory')

    class Meta:
        model = Repertory


class RoundFactory(DjangoModelFactory):
    status = Round.STATUS.new
    kind = Round.KIND.finals
    num = 1
    num_songs = 2
    start_date = None
    end_date = None
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
    is_flagged = False
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
    is_prelims = False
    cursor = None
    current = None
    primary = None
    scoresheet = None
    convention = SubFactory('app.factories.ConventionFactory')

    class Meta:
        model = Session


class SlotFactory(DjangoModelFactory):
    status = Slot.STATUS.new
    num = 1
    location = ''
    round = SubFactory('app.factories.RoundFactory')

    class Meta:
        model = Slot


class SongFactory(DjangoModelFactory):
    status = Song.STATUS.new
    num = 1
    appearance = SubFactory('app.factories.AppearanceFactory')
    chart = None
    submission = None

    class Meta:
        model = Song


class SubmissionFactory(DjangoModelFactory):
    status = Submission.STATUS.new
    title = 'Test Song Title'
    bhs_id = None
    is_medley = False
    is_parody = False
    arrangers = ''
    composers = ''
    holders = ''
    entry = SubFactory('app.factories.EntryFactory')
    repertory = SubFactory('app.factories.RepertoryFactory')

    class Meta:
        model = Submission


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
    email = 'test@barberscore.com'
    password = PostGenerationMethodCall('set_password', 'password')
    is_active = True
    is_staff = False

    class Meta:
        model = User


class AdminFactory(DjangoModelFactory):
    email = 'admin@barberscore.com'
    password = PostGenerationMethodCall('set_password', 'password')
    is_active = True
    is_staff = True

    class Meta:
        model = User
