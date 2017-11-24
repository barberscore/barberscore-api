from django.core.management.base import BaseCommand
# First-Party
from api.factories import (
    AppearanceFactory,
    AssignmentFactory,
    AwardFactory,
    ChartFactory,
    ContestantFactory,
    ContestFactory,
    ConventionFactory,
    CompetitorFactory,
    EntryFactory,
    GrantorFactory,
    GroupFactory,
    MemberFactory,
    OfficeFactory,
    OfficerFactory,
    OrganizationFactory,
    PanelistFactory,
    ParticipantFactory,
    PersonFactory,
    RepertoryFactory,
    RoundFactory,
    ScoreFactory,
    SessionFactory,
    SlotFactory,
    SongFactory,
    UserFactory,
    VenueFactory,
)
from api.models import (
    Appearance,
    Assignment,
    Award,
    Chart,
    Contest,
    Contestant,
    Convention,
    Competitor,
    Entry,
    Grantor,
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


class Command(BaseCommand):
    help = "Command to seed convention."

    def handle(self, *args, **options):
        # Create Admin
        admin_user = UserFactory(
            name='Admin Person',
            email='test@barberscore.com',
            password='password',
            is_staff=True,
            is_active=True,
        )
        admin_person = PersonFactory(
            first_name='Admin',
            last_name='Person',
            email='test@barberscore.com',
            status=Person.STATUS.active,
            user=admin_user,
        )
        # Create Core Users
        scjc_user = UserFactory(
            name='SCJC Person',
            email='scjs@barberscore.com',
            is_active=True,
        )
        drcj_user = UserFactory(
            name='DRCJ Person',
            email='drcj@barberscore.com',
            is_active=True,
        )
        ca_user = UserFactory(
            name='CA Person',
            email='ca@barberscore.com',
            is_active=True,
        )
        quartet_user = UserFactory(
            name='Quartet Person',
            email='quartet@barberscore.com',
            is_active=True,
        )
        chorus_user = UserFactory(
            name='Chorus Person',
            email='chorus@barberscore.com',
            is_active=True,
        )
        scjc_person = PersonFactory(
            first_name='SCJC',
            last_name='Person',
            email='scjc@barberscore.com',
            status=Person.STATUS.active,
            user=scjc_user,
        )
        drcj_person = PersonFactory(
            first_name='DRCJ',
            last_name='Person',
            email='drcj@barberscore.com',
            status=Person.STATUS.active,
            user=drcj_user,
        )
        ca_person = PersonFactory(
            first_name='CA',
            last_name='Person',
            email='ca@barberscore.com',
            status=Person.STATUS.active,
            user=ca_user,
        )
        quartet_person = PersonFactory(
            first_name='Quartet',
            last_name='Person',
            email='quartet@barberscore.com',
            status=Person.STATUS.active,
            user=quartet_user,
        )
        chorus_person = PersonFactory(
            first_name='Chorus',
            last_name='Person',
            email='chorus@barberscore.com',
            status=Person.STATUS.active,
            user=chorus_user,
        )
        # Create International and Districts
        international = OrganizationFactory(
            name='International Organization',
            code='INT',
            kind=Organization.KIND.international,
        )
        district_alpha = OrganizationFactory(
            name='District Alpha',
            code='ALF',
            parent=international,
            kind=Organization.KIND.district,
        )
        chapter_one = OrganizationFactory(
            name='Chapter One',
            code='A-001',
            parent=district_alpha,
            kind=Organization.KIND.chapter,
        )
        # Create Core Offices
        scjc_office = OfficeFactory(
            name='Society Chairman of C&J',
            short_name='SCJC',
            is_convention_manager=True,
            is_session_manager=True,
            is_scoring_manager=True,
            is_organization_manager=True,
            is_group_manager=True,
            is_person_manager=True,
            is_award_manager=True,
            is_judge_manager=True,
            is_chart_manager=True,
        )
        drcj_office = OfficeFactory(
            name='District Director C&J',
            short_name='DRCJ',
            is_convention_manager=True,
            is_session_manager=True,
            is_organization_manager=True,
            is_award_manager=True,
        )
        ca_office = OfficeFactory(
            name='Contest Administrator',
            short_name='CA',
            is_scoring_manager=True,
            is_judge_manager=True,
        )
        mus_office = OfficeFactory(
            name='Music Judge',
            short_name='MUS',
            is_judge_manager=True,
        )
        per_office = OfficeFactory(
            name='Performance Judge',
            short_name='PER',
            is_judge_manager=True,
        )
        sng_office = OfficeFactory(
            name='Singing Judge',
            short_name='SNG',
            is_judge_manager=True,
        )
        # Create Core Officers
        scjc_officer = OfficerFactory(
            office=scjc_office,
            person=scjc_person,
            organization=international,
            status=Officer.STATUS.active,
        )
        drcj_alpha_officer = OfficerFactory(
            office=drcj_office,
            person=drcj_person,
            organization=district_alpha,
            status=Officer.STATUS.active,
        )
        ca_officer = OfficerFactory(
            office=ca_office,
            person=ca_person,
            organization=international,
            status=Officer.STATUS.active,
        )
        mus_judges = OfficerFactory.create_batch(
            size=5,
            office=mus_office,
            organization=international,
            status=Officer.STATUS.active,
        )
        per_judges = OfficerFactory.create_batch(
            size=5,
            office=per_office,
            organization=international,
            status=Officer.STATUS.active,
        )
        sng_judges = OfficerFactory.create_batch(
            size=5,
            office=sng_office,
            organization=international,
            status=Officer.STATUS.active,
        )
        # Create Awards
        international_chorus_championship = AwardFactory(
            name='International Chorus Championship',
            organization=international,
            rounds=1,
            level=Award.LEVEL.championship,
            kind=Award.KIND.chorus,
        )
        district_alpha_quartet_championship = AwardFactory(
            name='District Alpha Quartet Championship',
            organization=district_alpha,
            rounds=2,
            level=Award.LEVEL.championship,
            season=Award.SEASON.fall,
        )
        district_alpha_international_chorus_championship_qualifier = AwardFactory(
            name='District Alpha International Chorus Championship Qualifier',
            organization=district_alpha,
            rounds=1,
            parent=international_chorus_championship,
            level=Award.LEVEL.qualifier,
            season=Award.SEASON.fall,
            kind=Award.KIND.chorus,
        )

        # Create conventions
        district_alpha_fall_convention = ConventionFactory(
            name='District Alpha Fall Convention',
            start_date='2017-10-01',
            end_date='2017-10-02',
            organization=district_alpha,
            panel=3,
            season=Convention.SEASON.fall,
        )
        GrantorFactory(
            organization=district_alpha,
            convention=district_alpha_fall_convention,
        )
        district_alpha_fall_convention_quartet_session = SessionFactory(
            convention=district_alpha_fall_convention,
            kind=Session.KIND.quartet,
            num_rounds=2,
        )
        district_alpha_fall_convention_chorus_session = SessionFactory(
            convention=district_alpha_fall_convention,
            kind=Session.KIND.chorus,
            num_rounds=1,
        )
        # Create quartet
        quartet_one = GroupFactory(
            name='Quartet One',
            organization=district_alpha,
        )
        # Overwrite user
        member = quartet_one.members.first()
        member.person = quartet_person
        member.is_admin = True
        member.save()

        # Create chorus
        chorus_one = GroupFactory(
            name='Chorus One',
            organization=chapter_one,
            kind=Group.KIND.chorus,
        )
        # Overwrite user
        member = chorus_one.members.first()
        member.person = chorus_person
        member.is_admin = True
        member.save()

