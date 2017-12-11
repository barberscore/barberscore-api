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
    EnrollmentFactory,
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
    Enrollment,
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
    Song,
    User,
    Venue,
)


class Command(BaseCommand):
    help = "Command to sync database with BHS ."

    def handle(self, *args, **options):
        # Create Persons
        admin_person = PersonFactory(
            first_name='Admin',
            last_name='Person',
            email='admin@barberscore.com',
        )
        scjc_person = PersonFactory(
            first_name='SCJC',
            last_name='Person',
            email='scjc@barberscore.com',
        )
        drcj_person = PersonFactory(
            first_name='DRCJ',
            last_name='Person',
            email='drcj@barberscore.com',
        )
        ca_person = PersonFactory(
            first_name='CA',
            last_name='Person',
            email='ca@barberscore.com',
        )
        quartet_admin_person = PersonFactory(
            first_name='Quartet',
            last_name='Admin',
            email='quartet_admin@barberscore.com',
        )
        chorus_admin_person = PersonFactory(
            first_name='Chorus',
            last_name='Admin',
            email='chorus_admin@barberscore.com',
        )
        music_judge_person = PersonFactory(
            first_name='Music',
            last_name='Judge',
            email='music_judge@barberscore.com',
        )
        performance_judge_person = PersonFactory(
            first_name='Performance',
            last_name='Judge',
            email='performance_judge@barberscore.com',
        )
        singing_judge_person = PersonFactory(
            first_name='Singing',
            last_name='Judge',
            email='singing_judge@barberscore.com',
        )
        # Create Users
        admin_user = UserFactory(
            name='{0} {1}'.format(
                admin_person.first_name,
                admin_person.last_name,
            ),
            email=admin_person.email,
            password='password',
            is_staff=True,
            is_active=True,
            auth0_id='email|5a18277f7cd31262971cddfc',
        )
        scjc_user = UserFactory(
            name='{0} {1}'.format(
                scjc_person.first_name,
                scjc_person.last_name,
            ),
            email=scjc_person.email,
            is_active=True,
            auth0_id='email|5a1827707cd31262971cddf8',
        )
        drcj_user = UserFactory(
            name='{0} {1}'.format(
                drcj_person.first_name,
                drcj_person.last_name,
            ),
            email=drcj_person.email,
            is_active=True,
            auth0_id='email|5a12f3607cd31262971bca22',
        )
        ca_user = UserFactory(
            name='{0} {1}'.format(
                ca_person.first_name,
                ca_person.last_name,
            ),
            email=ca_person.email,
            is_active=True,
            auth0_id='email|5a1827777cd31262971cddf9',
        )
        quartet_admin_user = UserFactory(
            name='{0} {1}'.format(
                quartet_admin_person.first_name,
                quartet_admin_person.last_name,
            ),
            email=quartet_admin_person.email,
            is_active=True,
            auth0_id='email|5a12f3627cd31262971bca24',
        )
        chorus_admin_user = UserFactory(
            name='{0} {1}'.format(
                chorus_admin_person.first_name,
                chorus_admin_person.last_name,
            ),
            email=chorus_admin_person.email,
            is_active=True,
            auth0_id='email|5a12f3637cd31262971bca25',
        )
        music_judge_user = UserFactory(
            name='{0} {1}'.format(
                music_judge_person.first_name,
                music_judge_person.last_name,
            ),
            email=music_judge_person.email,
            is_active=True,
            auth0_id='email|5a2ef1717cd312629752490b',
        )
        performance_judge_user = UserFactory(
            name='{0} {1}'.format(
                performance_judge_person.first_name,
                performance_judge_person.last_name,
            ),
            email=performance_judge_person.email,
            is_active=True,
            auth0_id='email|5a2ef1717cd312629752490a',
        )
        singing_judge_user = UserFactory(
            name='{0} {1}'.format(
                singing_judge_person.first_name,
                singing_judge_person.last_name,
            ),
            email=singing_judge_person.email,
            is_active=True,
            auth0_id='email|5a2ef1707cd3126297524909',
        )
        # Create Organizations
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
        # create Venue
        venue = VenueFactory()

        # create Chart
        chart_one = ChartFactory(
            title='Chart One',
        )
        chart_two = ChartFactory(
            title='Chart Two',
        )
        chart_three = ChartFactory(
            title='Chart Three',
        )
        chart_four = ChartFactory(
            title='Chart Four',
        )
        chart_five = ChartFactory(
            title='Chart Five',
        )
        chart_six = ChartFactory(
            title='Chart Six',
        )
        chart_seven = ChartFactory(
            title='Chart Seven',
        )
        chart_eight = ChartFactory(
            title='Chart Eight',
        )
        chart_nine = ChartFactory(
            title='Chart Nine',
        )
        chart_ten = ChartFactory(
            title='Chart Ten',
        )

        # Create Offices
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
        # Create Groups
        quartet_one = GroupFactory(
            name='Quartet One',
            organization=district_alpha,
        )
        # Create chorus
        chorus_one = GroupFactory(
            name='Chorus One',
            organization=chapter_one,
            kind=Group.KIND.chorus,
        )
        # Create enrollments
        enrollment_chorus_admin = EnrollmentFactory(
            organization=chapter_one,
            person=chorus_admin_person,
        )
        # Create members
        member_quartet_admin = MemberFactory(
            part=Member.PART.lead,
            is_admin=True,
            group=quartet_one,
            person=quartet_admin_person,
        )
        member_chorus_admin = MemberFactory(
            part=Member.PART.lead,
            is_admin=True,
            group=chorus_one,
            person=chorus_admin_person,
        )
        # Create repertories
        RepertoryFactory(
            group=quartet_one,
            chart=chart_one,
        )
        RepertoryFactory(
            group=quartet_one,
            chart=chart_two,
        )
        RepertoryFactory(
            group=quartet_one,
            chart=chart_three,
        )
        RepertoryFactory(
            group=quartet_one,
            chart=chart_four,
        )
        RepertoryFactory(
            group=quartet_one,
            chart=chart_five,
        )
        RepertoryFactory(
            group=quartet_one,
            chart=chart_six,
        )
        RepertoryFactory(
            group=chorus_one,
            chart=chart_one,
        )
        RepertoryFactory(
            group=chorus_one,
            chart=chart_two,
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
        mus_judge = OfficerFactory(
            office=mus_office,
            person=music_judge_person,
            organization=international,
            status=Officer.STATUS.active,
        )
        per_judge = OfficerFactory(
            office=per_office,
            person=performance_judge_person,
            organization=international,
            status=Officer.STATUS.active,
        )
        sng_judge = OfficerFactory(
            office=sng_office,
            person=singing_judge_person,
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

        return
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
        # Create assignments
        AssignmentFactory(
            category=Assignment.CATEGORY.drcj,
            convention=district_alpha_fall_convention,
            person=drcj_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.ca,
            convention=district_alpha_fall_convention,
            person=ca_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.music,
            convention=district_alpha_fall_convention,
            person=music_judge_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.performance,
            convention=district_alpha_fall_convention,
            person=performance_judge_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.singing,
            convention=district_alpha_fall_convention,
            person=singing_judge_person,
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

