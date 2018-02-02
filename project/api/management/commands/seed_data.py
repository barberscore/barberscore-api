# Django
from django.core.management.base import BaseCommand

# First-Party
from api.factories import AppearanceFactory
from api.factories import AssignmentFactory
from api.factories import AwardFactory
from api.factories import ChartFactory
from api.factories import CompetitorFactory
from api.factories import ContestantFactory
from api.factories import ContestFactory
from api.factories import ConventionFactory
from api.factories import EnrollmentFactory
from api.factories import EntryFactory
from api.factories import GrantorFactory
from api.factories import GroupFactory
from api.factories import MemberFactory
from api.factories import OfficeFactory
from api.factories import OfficerFactory
from api.factories import OrganizationFactory
from api.factories import PanelistFactory
from api.factories import ParticipantFactory
from api.factories import PersonFactory
from api.factories import RepertoryFactory
from api.factories import RoundFactory
from api.factories import ScoreFactory
from api.factories import SessionFactory
from api.factories import SongFactory
from api.factories import UserFactory
from api.factories import VenueFactory
from api.models import Appearance
from api.models import Assignment
from api.models import Award
from api.models import Chart
from api.models import Competitor
from api.models import Contest
from api.models import Contestant
from api.models import Convention
from api.models import Enrollment
from api.models import Entry
from api.models import Grantor
from api.models import Group
from api.models import Member
from api.models import Office
from api.models import Officer
from api.models import Organization
from api.models import Panelist
from api.models import Participant
from api.models import Person
from api.models import Repertory
from api.models import Round
from api.models import Score
from api.models import Session
from api.models import Song
from api.models import User
from api.models import Venue


class Command(BaseCommand):
    help = "Command to sync database with BHS ."

    def handle(self, *args, **options):
        # Create Users
        admin_user = UserFactory(
            id='c7fc3e26-1489-46a5-93a2-7be50a01c56c',
            name='Admin Person',
            email='admin@barberscore.com',
            password='password',
            is_staff=True,
            is_active=True,
            auth0_id='email|5a18277f7cd31262971cddfc',
        )
        scjc_user = UserFactory(
            id='a3be3d43-c5d3-4aec-973a-d42c00c72256',
            name='SCJC Person',
            email='scjc@barberscore.com',
            is_active=True,
            auth0_id='email|5a1827707cd31262971cddf8',
        )
        drcj_user = UserFactory(
            id='55ef12a3-576d-496b-a70b-c3126f62caa2',
            name='DRCJ Person',
            email='drcj@barberscore.com',
            is_active=True,
            auth0_id='email|5a12f3607cd31262971bca22',
        )
        ca_user = UserFactory(
            id='7cfdac82-ca9f-46dc-9c7b-c9054908cb7c',
            name='CA Person',
            email='ca@barberscore.com',
            is_active=True,
            auth0_id='email|5a1827777cd31262971cddf9',
        )
        quartet_admin_user = UserFactory(
            id='afa2d19b-1099-4a77-bc8c-04b06a6896a0',
            name='Quartet Person',
            email='quartet_admin@barberscore.com',
            is_active=True,
            auth0_id='email|5a12f3627cd31262971bca24',
        )
        chorus_admin_user = UserFactory(
            id='bd32c1e6-4c61-4f7f-bee5-e843d80bb9ad',
            name='Chorus Person',
            email='chorus_admin@barberscore.com',
            is_active=True,
            auth0_id='email|5a12f3637cd31262971bca25',
        )
        music_judge_user = UserFactory(
            id='55204faf-d4c6-4b88-9bed-3721db42ccf3',
            name='Music Person',
            email='music_judge@barberscore.com',
            is_active=True,
            auth0_id='email|5a2ef1717cd312629752490b',
        )
        performance_judge_user = UserFactory(
            id='8e326a1a-5bb9-4a29-98f9-c7f704870f43',
            name='Performance Person',
            email='performance_judge@barberscore.com',
            is_active=True,
            auth0_id='email|5a2ef1717cd312629752490a',
        )
        singing_judge_user = UserFactory(
            id='fb6bb161-69f0-49ff-ba51-3a4721220566',
            name='Singing Person',
            email='singing_judge@barberscore.com',
            is_active=True,
            auth0_id='email|5a2ef1707cd3126297524909',
        )
        # Create Persons
        admin_person = PersonFactory(
            first_name='Admin',
            last_name='Person',
            email='admin@barberscore.com',
            user=admin_user,
        )
        scjc_person = PersonFactory(
            first_name='SCJC',
            last_name='Person',
            email='scjc@barberscore.com',
            user=scjc_user,
        )
        drcj_person = PersonFactory(
            first_name='DRCJ',
            last_name='Person',
            email='drcj@barberscore.com',
            user=drcj_user,
        )
        ca_person = PersonFactory(
            first_name='CA',
            last_name='Person',
            email='ca@barberscore.com',
            user=ca_user,
        )
        quartet_admin_person = PersonFactory(
            first_name='Quartet',
            last_name='Admin',
            email='quartet_admin@barberscore.com',
            user=quartet_admin_user,
        )
        quartet_tenor_person = PersonFactory(
            first_name='Quartet',
            last_name='Tenor',
        )
        quartet_baritone_person = PersonFactory(
            first_name='Quartet',
            last_name='Baritone',
        )
        quartet_bass_person = PersonFactory(
            first_name='Quartet',
            last_name='Bass',
        )
        chorus_admin_person = PersonFactory(
            first_name='Chorus',
            last_name='Admin',
            email='chorus_admin@barberscore.com',
            user=chorus_admin_user,
        )
        music_judge_person = PersonFactory(
            first_name='Music',
            last_name='Judge',
            email='music_judge@barberscore.com',
            user=music_judge_user,
        )
        performance_judge_person = PersonFactory(
            first_name='Performance',
            last_name='Judge',
            email='performance_judge@barberscore.com',
            user=performance_judge_user,
        )
        singing_judge_person = PersonFactory(
            first_name='Singing',
            last_name='Judge',
            email='singing_judge@barberscore.com',
            user=singing_judge_user,
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
            title='Chart 1',
        )
        chart_two = ChartFactory(
            title='Chart 2',
        )
        chart_three = ChartFactory(
            title='Chart 3',
        )
        chart_four = ChartFactory(
            title='Chart 4',
        )
        chart_five = ChartFactory(
            title='Chart 5',
        )
        chart_six = ChartFactory(
            title='Chart 6',
        )
        chart_seven = ChartFactory(
            title='Chart 7',
        )
        chart_eight = ChartFactory(
            title='Chart 8',
        )
        chart_nine = ChartFactory(
            title='Chart 9',
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
        international_quartet_championship = AwardFactory(
            name='International Quartet Championship',
            organization=international,
            rounds=1,
            level=Award.LEVEL.championship,
            kind=Award.KIND.quartet,
            season=Award.SEASON.summer,
        )
        international_chorus_championship = AwardFactory(
            name='International Chorus Championship',
            organization=international,
            rounds=1,
            level=Award.LEVEL.championship,
            kind=Award.KIND.chorus,
            season=Award.SEASON.summer,
        )
        district_alpha_quartet_championship = AwardFactory(
            name='District Alpha Quartet Championship',
            organization=district_alpha,
            rounds=2,
            level=Award.LEVEL.championship,
            season=Award.SEASON.fall,
        )
        district_alpha_international_quartet_championship_qualifier = AwardFactory(
            name='District Alpha International Quartet Championship Qualifier',
            organization=district_alpha,
            rounds=2,
            parent=international_quartet_championship,
            level=Award.LEVEL.qualifier,
            season=Award.SEASON.spring,
            kind=Award.KIND.quartet,
            advance=76.0,
        )
        district_alpha_international_chorus_championship_qualifier = AwardFactory(
            name='District Alpha International Chorus Championship Qualifier',
            organization=district_alpha,
            rounds=1,
            parent=international_chorus_championship,
            level=Award.LEVEL.qualifier,
            season=Award.SEASON.fall,
            kind=Award.KIND.chorus,
            advance=73.0,
        )
        international_senior_quartet_championship = AwardFactory(
            name='International Senior Quartet Championship',
            organization=international,
            rounds=1,
            level=Award.LEVEL.championship,
            kind=Award.KIND.quartet,
            season=Award.SEASON.midwinter,
        )

        # Create conventions
        international_midwinter_convention = ConventionFactory(
            name='International Midwinter Convention',
            organization=international,
            panel=3,
            season=Convention.SEASON.midwinter,
        )
        GrantorFactory(
            organization=international,
            convention=international_midwinter_convention,
        )
        district_alpha_fall_convention = ConventionFactory(
            name='District Alpha Fall Convention',
            organization=district_alpha,
            panel=3,
            season=Convention.SEASON.fall,
        )
        GrantorFactory(
            organization=district_alpha,
            convention=district_alpha_fall_convention,
        )
        district_alpha_spring_convention = ConventionFactory(
            name='District Alpha Spring Convention',
            organization=district_alpha,
            panel=3,
            season=Convention.SEASON.spring,
        )
        GrantorFactory(
            organization=district_alpha,
            convention=district_alpha_spring_convention,
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
        AssignmentFactory(
            category=Assignment.CATEGORY.drcj,
            convention=district_alpha_spring_convention,
            person=drcj_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.ca,
            convention=district_alpha_spring_convention,
            person=ca_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.music,
            convention=district_alpha_spring_convention,
            person=music_judge_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.performance,
            convention=district_alpha_spring_convention,
            person=performance_judge_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.singing,
            convention=district_alpha_spring_convention,
            person=singing_judge_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.drcj,
            convention=international_midwinter_convention,
            person=drcj_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.ca,
            convention=international_midwinter_convention,
            person=ca_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.music,
            convention=international_midwinter_convention,
            person=music_judge_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.performance,
            convention=international_midwinter_convention,
            person=performance_judge_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.singing,
            convention=international_midwinter_convention,
            person=singing_judge_person,
        )
        international_midwinter_convention_quartet_session = SessionFactory(
            convention=international_midwinter_convention,
            kind=Session.KIND.quartet,
            num_rounds=1,
            is_invitational=True,
        )
        district_alpha_fall_convention_quartet_session = SessionFactory(
            convention=district_alpha_fall_convention,
            kind=Session.KIND.quartet,
            num_rounds=2,
        )
        district_alpha_spring_convention_quartet_session = SessionFactory(
            convention=district_alpha_spring_convention,
            kind=Session.KIND.quartet,
            num_rounds=2,
        )
        district_alpha_fall_convention_chorus_session = SessionFactory(
            convention=district_alpha_fall_convention,
            kind=Session.KIND.chorus,
            num_rounds=1,
        )
        # Create Groups
        quartet_1 = GroupFactory(
            name='Quartet 1',
            kind=Group.KIND.quartet,
            organization=district_alpha,
            international=international.code,
            district=district_alpha.code,
        )
        quartet_2 = GroupFactory(
            name='Quartet 2',
            kind=Group.KIND.quartet,
            organization=district_alpha,
            international=international.code,
            district=district_alpha.code,
        )
        quartet_3 = GroupFactory(
            name='Quartet 3',
            kind=Group.KIND.quartet,
            organization=district_alpha,
            international=international.code,
            district=district_alpha.code,
        )
        # Create chorus
        chorus_one = GroupFactory(
            name='Chorus One',
            kind=Group.KIND.chorus,
            organization=chapter_one,
            international=international.code,
            district=district_alpha.code,
            chapter=chapter_one.name,
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
            group=quartet_1,
            person=quartet_admin_person,
        )
        member_quartet_tenor = MemberFactory(
            part=Member.PART.tenor,
            is_admin=False,
            group=quartet_1,
            person=quartet_tenor_person,
        )
        member_quartet_baritone = MemberFactory(
            part=Member.PART.baritone,
            is_admin=False,
            group=quartet_1,
            person=quartet_baritone_person,
        )
        member_quartet_bass = MemberFactory(
            part=Member.PART.bass,
            is_admin=False,
            group=quartet_1,
            person=quartet_bass_person,
        )
        member_chorus_admin = MemberFactory(
            part=Member.PART.lead,
            is_admin=True,
            group=chorus_one,
            person=chorus_admin_person,
        )
        member_quartet_2_admin = MemberFactory(
            part=Member.PART.lead,
            is_admin=True,
            group=quartet_2,
            person=quartet_admin_person,
        )
        member_quartet_2_tenor = MemberFactory(
            part=Member.PART.tenor,
            is_admin=False,
            group=quartet_2,
            person=quartet_tenor_person,
        )
        member_quartet_2_baritone = MemberFactory(
            part=Member.PART.baritone,
            is_admin=False,
            group=quartet_2,
            person=quartet_baritone_person,
        )
        member_quartet_2_bass = MemberFactory(
            part=Member.PART.bass,
            is_admin=False,
            group=quartet_2,
            person=quartet_bass_person,
        )
        member_quartet_3_admin = MemberFactory(
            part=Member.PART.lead,
            is_admin=True,
            group=quartet_3,
            person=quartet_admin_person,
        )
        member_quartet_3_tenor = MemberFactory(
            part=Member.PART.tenor,
            is_admin=False,
            group=quartet_3,
            person=quartet_tenor_person,
        )
        member_quartet_3_baritone = MemberFactory(
            part=Member.PART.baritone,
            is_admin=False,
            group=quartet_3,
            person=quartet_baritone_person,
        )
        member_quartet_3_bass = MemberFactory(
            part=Member.PART.bass,
            is_admin=False,
            group=quartet_3,
            person=quartet_bass_person,
        )
        # Create repertories
        RepertoryFactory(
            group=quartet_1,
            chart=chart_one,
        )
        RepertoryFactory(
            group=quartet_1,
            chart=chart_two,
        )
        RepertoryFactory(
            group=quartet_1,
            chart=chart_three,
        )
        RepertoryFactory(
            group=quartet_1,
            chart=chart_four,
        )
        RepertoryFactory(
            group=quartet_1,
            chart=chart_five,
        )
        RepertoryFactory(
            group=quartet_1,
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
        RepertoryFactory(
            group=quartet_2,
            chart=chart_one,
        )
        RepertoryFactory(
            group=quartet_2,
            chart=chart_two,
        )
        RepertoryFactory(
            group=quartet_2,
            chart=chart_three,
        )
        RepertoryFactory(
            group=quartet_2,
            chart=chart_four,
        )
        RepertoryFactory(
            group=quartet_2,
            chart=chart_five,
        )
        RepertoryFactory(
            group=quartet_2,
            chart=chart_six,
        )

        RepertoryFactory(
            group=quartet_3,
            chart=chart_one,
        )
        RepertoryFactory(
            group=quartet_3,
            chart=chart_two,
        )
        RepertoryFactory(
            group=quartet_3,
            chart=chart_three,
        )
        RepertoryFactory(
            group=quartet_3,
            chart=chart_four,
        )
        RepertoryFactory(
            group=quartet_3,
            chart=chart_five,
        )
        RepertoryFactory(
            group=quartet_3,
            chart=chart_six,
        )

        # SCJC BREAKPOINT

        # Contests created via signal.
        international_midwinter_convention.publish()
        international_midwinter_convention.save()
        district_alpha_fall_convention.publish()
        district_alpha_fall_convention.save()
        district_alpha_spring_convention.publish()
        district_alpha_spring_convention.save()

        # Open sessions
        international_midwinter_convention_quartet_session.open()
        international_midwinter_convention_quartet_session.save()
        district_alpha_fall_convention_quartet_session.open()
        district_alpha_fall_convention_quartet_session.save()
        district_alpha_spring_convention_quartet_session.open()
        district_alpha_spring_convention_quartet_session.save()
        district_alpha_fall_convention_chorus_session.open()
        district_alpha_fall_convention_chorus_session.save()

        # Add entries
        senior_entry = EntryFactory(
            session=international_midwinter_convention_quartet_session,
            group=quartet_1,
        )
        senior_2_entry = EntryFactory(
            session=international_midwinter_convention_quartet_session,
            group=quartet_2,
        )
        senior_3_entry = EntryFactory(
            session=international_midwinter_convention_quartet_session,
            group=quartet_3,
        )
        quartet_entry = EntryFactory(
            session=district_alpha_fall_convention_quartet_session,
            group=quartet_1,
        )
        quartet_2_entry = EntryFactory(
            session=district_alpha_fall_convention_quartet_session,
            group=quartet_2,
        )
        quartet_3_entry = EntryFactory(
            session=district_alpha_fall_convention_quartet_session,
            group=quartet_3,
        )
        spring_quartet_entry = EntryFactory(
            session=district_alpha_spring_convention_quartet_session,
            group=quartet_1,
        )
        spring_quartet_2_entry = EntryFactory(
            session=district_alpha_spring_convention_quartet_session,
            group=quartet_2,
        )
        spring_quartet_3_entry = EntryFactory(
            session=district_alpha_spring_convention_quartet_session,
            group=quartet_3,
        )
        chorus_entry = EntryFactory(
            session=district_alpha_fall_convention_chorus_session,
            group=chorus_one,
        )

        # Approve entries
        senior_entry.approve()
        senior_entry.save()
        senior_2_entry.approve()
        senior_2_entry.save()
        senior_3_entry.approve()
        senior_3_entry.save()
        quartet_entry.approve()
        quartet_entry.save()
        quartet_2_entry.approve()
        quartet_2_entry.save()
        quartet_3_entry.approve()
        quartet_3_entry.save()
        spring_quartet_entry.approve()
        spring_quartet_entry.save()
        spring_quartet_2_entry.approve()
        spring_quartet_2_entry.save()
        spring_quartet_3_entry.approve()
        spring_quartet_3_entry.save()
        chorus_entry.approve()
        chorus_entry.save()

        # Close sessions
        international_midwinter_convention_quartet_session.close()
        international_midwinter_convention_quartet_session.save()
        district_alpha_fall_convention_quartet_session.close()
        district_alpha_fall_convention_quartet_session.save()
        district_alpha_spring_convention_quartet_session.close()
        district_alpha_spring_convention_quartet_session.save()
        district_alpha_fall_convention_chorus_session.close()
        district_alpha_fall_convention_chorus_session.save()

        # Verify sessions
        international_midwinter_convention_quartet_session.verify()
        international_midwinter_convention_quartet_session.save()
        district_alpha_fall_convention_quartet_session.verify()
        district_alpha_fall_convention_quartet_session.save()
        district_alpha_spring_convention_quartet_session.verify()
        district_alpha_spring_convention_quartet_session.save()
        district_alpha_fall_convention_chorus_session.verify()
        district_alpha_fall_convention_chorus_session.save()

        # Start sessions
        international_midwinter_convention_quartet_session.start()
        international_midwinter_convention_quartet_session.save()
        district_alpha_spring_convention_quartet_session.start()
        district_alpha_spring_convention_quartet_session.save()
        district_alpha_fall_convention_quartet_session.start()
        district_alpha_fall_convention_quartet_session.save()
        district_alpha_fall_convention_chorus_session.start()
        district_alpha_fall_convention_chorus_session.save()

        # DRCJ BREAKPOINT

        # Start First Round
        international_midwinter_convention_quartet_session_round_one = international_midwinter_convention_quartet_session.rounds.earliest()
        district_alpha_fall_convention_quartet_session_round_one = district_alpha_fall_convention_quartet_session.rounds.earliest()
        district_alpha_spring_convention_quartet_session_round_one = district_alpha_spring_convention_quartet_session.rounds.earliest()
        district_alpha_fall_convention_chorus_session_round_one = district_alpha_fall_convention_chorus_session.rounds.earliest()

        international_midwinter_convention_quartet_session_round_one.start()
        international_midwinter_convention_quartet_session_round_one.save()
        district_alpha_fall_convention_quartet_session_round_one.start()
        district_alpha_fall_convention_quartet_session_round_one.save()
        district_alpha_spring_convention_quartet_session_round_one.start()
        district_alpha_spring_convention_quartet_session_round_one.save()
        district_alpha_fall_convention_chorus_session_round_one.start()
        district_alpha_fall_convention_chorus_session_round_one.save()

        s = 70
        for appearance in international_midwinter_convention_quartet_session_round_one.appearances.order_by('num'):
            appearance.start()
            appearance.save()
            song_one = appearance.songs.earliest()
            song_two = appearance.songs.latest()
            song_one.chart = Chart.objects.get(title='Chart 1')
            song_two.chart = Chart.objects.get(title='Chart 2')
            song_one.save()
            song_two.save()
            appearance.finish()
            appearance.save()
            s += 5
            for song in appearance.songs.all():
                for score in song.scores.all():
                    score.points = s
                    score.save()
            appearance.confirm()
            appearance.save()

        s = 70
        for appearance in district_alpha_fall_convention_quartet_session_round_one.appearances.order_by('num'):
            appearance.start()
            appearance.save()
            song_one = appearance.songs.earliest()
            song_two = appearance.songs.latest()
            song_one.chart = Chart.objects.get(title='Chart 1')
            song_two.chart = Chart.objects.get(title='Chart 2')
            song_one.save()
            song_two.save()
            appearance.finish()
            appearance.save()
            s += 5
            for song in appearance.songs.all():
                for score in song.scores.all():
                    score.points = s
                    score.save()
            appearance.confirm()
            appearance.save()

        s = 70
        for appearance in district_alpha_spring_convention_quartet_session_round_one.appearances.order_by('num'):
            appearance.start()
            appearance.save()
            song_one = appearance.songs.earliest()
            song_two = appearance.songs.latest()
            song_one.chart = Chart.objects.get(title='Chart 1')
            song_two.chart = Chart.objects.get(title='Chart 2')
            song_one.save()
            song_two.save()
            appearance.finish()
            appearance.save()
            s += 5
            for song in appearance.songs.all():
                for score in song.scores.all():
                    score.points = s
                    score.save()
            appearance.confirm()
            appearance.save()

        return
        international_midwinter_convention_quartet_session_round_one.review()
        international_midwinter_convention_quartet_session_round_one.save()
        district_alpha_fall_convention_quartet_session_round_one.review()
        district_alpha_fall_convention_quartet_session_round_one.save()
