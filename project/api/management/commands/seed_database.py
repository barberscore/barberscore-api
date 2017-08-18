# Django
# Standard Libary
import json
import random
from itertools import chain
from optparse import make_option

from django.core.management.base import BaseCommand
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.db import IntegrityError

# First-Party
from api.factories import (
    AppearanceFactory,
    AssignmentFactory,
    AwardFactory,
    ChartFactory,
    ContestantFactory,
    ContestFactory,
    ConventionFactory,
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
    help="Command to seed convention."
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '-b',
            '--break',
            dest='breakpoint',
            default=None,
            help='Set breakpoint for database seed.',
        )

    def handle(self, *args, **options):
        # Create Admin
        admin=UserFactory(
            email='test@barberscore.com',
            password='password',
            is_staff=True,
            person=None,
        )
        # Create Core Persons
        scjc_person=PersonFactory(
            name='SCJC Person',
            email='scjc@barberscore.com',
        )
        drcj_person=PersonFactory(
            name='DRCJ Person',
            email='drcj@barberscore.com',
        )
        ca_person=PersonFactory(
            name='CA Person',
            email='ca@barberscore.com',
        )
        quartet_person=PersonFactory(
            name='Quartet Person',
            email='quartet@barberscore.com',
        )
        chorus_person=PersonFactory(
            name='Chorus Person',
            email='chorus@barberscore.com',
        )
        # Create Core Users
        scjc_user=UserFactory(
            email=scjc_person.email,
            person=scjc_person,
        )
        drcj_user=UserFactory(
            email=drcj_person.email,
            person=drcj_person,
        )
        ca_user=UserFactory(
            email=ca_person.email,
            person=ca_person,
        )
        quartet_user=UserFactory(
            email=quartet_person.email,
            person=quartet_person,
        )
        chorus_user=UserFactory(
            email=chorus_person.email,
            person=chorus_person,
        )
        # Create International and Districts
        international=OrganizationFactory(
            name='International Organization',
            short_name='INT',
            kind=Organization.KIND.international,
        )
        district_alpha=OrganizationFactory(
            name='District Alpha',
            short_name='ALF',
            parent=international,
            kind=Organization.KIND.district,
        )
        district_beta=OrganizationFactory(
            name='District Beta',
            short_name='BTA',
            parent=international,
            kind=Organization.KIND.district,
        )
        district_beta_division_north=OrganizationFactory(
            name='Division Beta North',
            short_name='BTA ND',
            parent=district_beta,
            kind=Organization.KIND.division,
        )
        district_beta_division_south=OrganizationFactory(
            name='Division Beta South',
            short_name='BTA SD',
            parent=district_beta,
            kind=Organization.KIND.division,
        )
        district_beta_division_east=OrganizationFactory(
            name='Division Beta East',
            short_name='BTA ED',
            parent=district_beta,
            kind=Organization.KIND.division,
        )
        district_beta_division_west=OrganizationFactory(
            name='Division Beta West',
            short_name='BTA WD',
            parent=district_beta,
            kind=Organization.KIND.division,
        )
        affiliate=OrganizationFactory(
            name='Affiliate Organization',
            short_name='AFF',
            parent=international,
            kind=Organization.KIND.affiliate,
        )
        # Create Core Offices
        scjc_office=OfficeFactory(
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
        drcj_office=OfficeFactory(
            name='District Director C&J',
            short_name='DRCJ',
            is_convention_manager=True,
            is_session_manager=True,
            is_organization_manager=True,
            is_award_manager=True,
        )
        ca_office=OfficeFactory(
            name='Contest Administrator',
            short_name='CA',
            is_scoring_manager=True,
            is_judge_manager=True,
        )
        mus_office=OfficeFactory(
            name='Music Judge',
            short_name='MUS',
            is_judge_manager=True,
        )
        per_office=OfficeFactory(
            name='Performance Judge',
            short_name='PER',
            is_judge_manager=True,
        )
        sng_office=OfficeFactory(
            name='Singing Judge',
            short_name='SNG',
            is_judge_manager=True,
        )
        # Create Core Officers
        scjc_officer=OfficerFactory(
            office=scjc_office,
            person=scjc_person,
            organization=international,
            status=Officer.STATUS.active,
        )
        drcj_alpha_officer=OfficerFactory(
            office=drcj_office,
            person=drcj_person,
            organization=district_alpha,
            status=Officer.STATUS.active,
        )
        drcj_beta_officer=OfficerFactory(
            office=drcj_office,
            person=drcj_person,
            organization=district_beta,
            status=Officer.STATUS.active,
        )
        drcj_beta_north_officer=OfficerFactory(
            office=drcj_office,
            person=drcj_person,
            organization=district_beta_division_north,
            status=Officer.STATUS.active,
        )
        drcj_beta_south_officer=OfficerFactory(
            office=drcj_office,
            person=drcj_person,
            organization=district_beta_division_south,
            status=Officer.STATUS.active,
        )
        drcj_beta_east_officer=OfficerFactory(
            office=drcj_office,
            person=drcj_person,
            organization=district_beta_division_east,
            status=Officer.STATUS.active,
        )
        drcj_beta_west_officer=OfficerFactory(
            office=drcj_office,
            person=drcj_person,
            organization=district_beta_division_west,
            status=Officer.STATUS.active,
        )
        ca_officer=OfficerFactory(
            office=ca_office,
            person=ca_person,
            organization=international,
            status=Officer.STATUS.active,
        )
        # Create Charts
        charts = ChartFactory.create_batch(
            size=500,
            status=Chart.STATUS.active,
        )
        # Create Quartets
        quartets = GroupFactory.build_batch(
            size=140,
            kind=Group.KIND.quartet,
        )
        n = 1
        for quartet in quartets:
            if n <= 60:
                quartet.organization = district_alpha
            elif n <= 80:
                quartet.organization = district_beta_division_north
            elif n <= 100:
                quartet.organization = district_beta_division_south
            elif n <= 120:
                quartet.organization = district_beta_division_east
            elif n <= 140:
                quartet.organization = district_beta_division_west
            n += 1
            quartet.save()
            i = 1
            while i <= 4:
                try:
                    MemberFactory(
                        group=quartet,
                        part=i,
                        status=Member.STATUS.active,
                    )
                except IntegrityError:
                    continue
                i += 1
            i = 1
            while i <= 6:
                try:
                    chart = Chart.objects.order_by('?').first()
                    RepertoryFactory(
                        group=quartet,
                        chart=chart,
                    )
                except IntegrityError:
                    continue
                i += 1



        member = Group.objects.filter(organization__name='District Alpha').first().members.get(part=1)
        member.person = quartet_person
        member.is_admin = True
        member.save()
        member = Group.objects.filter(organization__name='Division Beta North').first().members.get(part=1)
        member.person = quartet_person
        member.is_admin = True
        member.save()
        member = Group.objects.filter(organization__name='Division Beta South').first().members.get(part=1)
        member.person = quartet_person
        member.is_admin = True
        member.save()
        member = Group.objects.filter(organization__name='Division Beta East').first().members.get(part=1)
        member.person = quartet_person
        member.is_admin = True
        member.save()
        member = Group.objects.filter(organization__name='Division Beta West').first().members.get(part=1)
        member.person = quartet_person
        member.is_admin = True
        member.save()

        # Create Judges
        mus_judges=OfficerFactory.create_batch(
            size=30,
            office=mus_office,
            organization=international,
            status=Officer.STATUS.active,
        )
        per_judges=OfficerFactory.create_batch(
            size=30,
            office=per_office,
            organization=international,
            status=Officer.STATUS.active,
        )
        sng_judges=OfficerFactory.create_batch(
            size=30,
            office=sng_office,
            organization=international,
            status=Officer.STATUS.active,
        )
        # Create Awards
        international_quartet_championship=AwardFactory(
            name='International Quartet Championship',
            organization=international,
            rounds=3,
            level=Award.LEVEL.championship,
        )
        district_alpha_international_quartet_championship_qualifier=AwardFactory(
            name='District Alpha International Quartet Championship Qualifier',
            organization=district_alpha,
            rounds=2,
            parent=international_quartet_championship,
            level=Award.LEVEL.qualifier,
            season=Award.SEASON.spring,
        )
        district_beta_international_quartet_championship_qualifier=AwardFactory(
            name='District Beta International Quartet Championship Qualifier',
            organization=district_beta,
            rounds=2,
            parent=international_quartet_championship,
            level=Award.LEVEL.qualifier,
            season=Award.SEASON.spring,
        )
        international_chorus_championship=AwardFactory(
            name='International Chorus Championship',
            organization=international,
            rounds=1,
            level=Award.LEVEL.championship,
            kind=Award.KIND.chorus,
        )
        district_alpha_international_chorus_championship_qualifier=AwardFactory(
            name='District Alpha International Chorus Championship Qualifier',
            organization=district_alpha,
            rounds=1,
            parent=international_chorus_championship,
            level=Award.LEVEL.qualifier,
            season=Award.SEASON.fall,
            kind=Award.KIND.chorus,
        )
        district_beta_international_chorus_championship_qualifier=AwardFactory(
            name='District Beta International Chorus Championship Qualifier',
            organization=district_beta,
            rounds=1,
            parent=international_chorus_championship,
            level=Award.LEVEL.qualifier,
            season=Award.SEASON.fall,
            kind=Award.KIND.chorus,
        )
        # international_youth_quartet_championship=AwardFactory(
        #     name='International Youth Quartet Championship',
        #     organization=international,
        #     rounds=1,
        #     level=Award.LEVEL.championship,
        # )
        # international_dc_award=AwardFactory(
        #     name='International Dealers Choice Award',
        #     organization=international,
        #     rounds=3,
        #     level=Award.LEVEL.award,
        # )
        district_alpha_quartet_championship=AwardFactory(
            name='District Alpha Quartet Championship',
            organization=district_alpha,
            rounds=2,
            level=Award.LEVEL.championship,
            season=Award.SEASON.fall,
        )
        district_alpha_chorus_championship=AwardFactory(
            name='District Alpha Chorus Championship',
            organization=district_alpha,
            rounds=1,
            level=Award.LEVEL.championship,
            season=Award.SEASON.spring,
            kind=Award.KIND.chorus,
        )
        district_beta_quartet_championship=AwardFactory(
            name='District Beta Quartet Championship',
            organization=district_beta,
            rounds=2,
            level=Award.LEVEL.championship,
            season=Award.SEASON.fall,
        )
        district_beta_division_north_district_beta_quartet_championship_qualifier=AwardFactory(
            name='BTA Division North District Beta Quartet Championship Qualifier',
            organization=district_beta_division_north,
            rounds=1,
            parent=district_beta_quartet_championship,
            level=Award.LEVEL.qualifier,
            season=Award.SEASON.spring,
        )
        district_beta_division_south_district_beta_quartet_championship_qualifier=AwardFactory(
            name='BTA Division South District Beta Quartet Championship Qualifier',
            organization=district_beta_division_south,
            rounds=1,
            parent=district_beta_quartet_championship,
            level=Award.LEVEL.qualifier,
            season=Award.SEASON.spring,
        )
        district_beta_division_east_district_beta_quartet_championship_qualifier=AwardFactory(
            name='BTA Division East District Beta Quartet Championship Qualifier',
            organization=district_beta_division_east,
            rounds=1,
            parent=district_beta_quartet_championship,
            level=Award.LEVEL.qualifier,
            season=Award.SEASON.spring,
        )
        district_beta_division_west_district_beta_quartet_championship_qualifier=AwardFactory(
            name='BTA Division West District Beta Quartet Championship Qualifier',
            organization=district_beta_division_west,
            rounds=1,
            parent=district_beta_quartet_championship,
            level=Award.LEVEL.qualifier,
            season=Award.SEASON.spring,
        )
        district_beta_chorus_championship=AwardFactory(
            name='District Beta Chorus Championship',
            organization=district_beta,
            rounds=1,
            level=Award.LEVEL.championship,
            season=Award.SEASON.fall,
            kind=Award.KIND.chorus,
        )
        district_beta_division_east_district_beta_chorus_championship_qualifier=AwardFactory(
            name='BTA Division East District Beta Chorus Championship Qualifier',
            organization=district_beta_division_east,
            rounds=1,
            parent=district_beta_chorus_championship,
            level=Award.LEVEL.qualifier,
            season=Award.SEASON.spring,
            kind=Award.KIND.chorus,
        )
        district_beta_division_west_district_beta_chorus_championship_qualifier=AwardFactory(
            name='BTA Division West District Beta Chorus Championship Qualifier',
            organization=district_beta_division_west,
            rounds=1,
            parent=district_beta_chorus_championship,
            level=Award.LEVEL.qualifier,
            season=Award.SEASON.spring,
            kind=Award.KIND.chorus,
        )
        district_beta_division_north_quartet_championship=AwardFactory(
            name='BTA Division North Quartet Championship',
            organization=district_beta_division_north,
            rounds=1,
            level=Award.LEVEL.championship,
            season=Award.SEASON.spring,
        )
        district_beta_division_south_quartet_championship=AwardFactory(
            name='BTA Division South Quartet Championship',
            organization=district_beta_division_south,
            rounds=1,
            level=Award.LEVEL.championship,
            season=Award.SEASON.spring,
        )
        district_beta_division_east_quartet_championship=AwardFactory(
            name='BTA Division East Quartet Championship',
            organization=district_beta_division_east,
            rounds=1,
            level=Award.LEVEL.championship,
            season=Award.SEASON.spring,
        )
        district_beta_division_west_quartet_championship=AwardFactory(
            name='BTA Division West Quartet Championship',
            organization=district_beta_division_west,
            rounds=1,
            level=Award.LEVEL.championship,
            season=Award.SEASON.spring,
        )
        district_beta_division_north_chorus_championship=AwardFactory(
            name='BTA Division North Chorus Championship',
            organization=district_beta_division_north,
            rounds=1,
            level=Award.LEVEL.championship,
            season=Award.SEASON.spring,
            kind=Award.KIND.chorus,
        )
        district_beta_division_south_chorus_championship=AwardFactory(
            name='BTA Division South Chorus Championship',
            organization=district_beta_division_south,
            rounds=1,
            level=Award.LEVEL.championship,
            season=Award.SEASON.spring,
            kind=Award.KIND.chorus,
        )
        district_beta_division_east_chorus_championship=AwardFactory(
            name='BTA Division East Chorus Championship',
            organization=district_beta_division_east,
            rounds=1,
            level=Award.LEVEL.championship,
            season=Award.SEASON.spring,
            kind=Award.KIND.chorus,
        )
        district_beta_division_west_chorus_championship=AwardFactory(
            name='BTA Division West Chorus Championship',
            organization=district_beta_division_west,
            rounds=1,
            level=Award.LEVEL.championship,
            season=Award.SEASON.spring,
            kind=Award.KIND.chorus,
        )
        # Create Conventions and Sessions

        # international_convention=ConventionFactory(
        #     name='International Convention',
        #     start_date='2017-07-01',
        #     end_date='2017-07-08',
        #     organization=international,
        # )
        # international_convention_quartet_session = international_convention.sessions.create(kind=Session.KIND.quartet)
        # international_convention_chorus_session = international_convention.sessions.create(kind=Session.KIND.chorus)
        #
        # international_youth_convention=ConventionFactory(
        #     name='International Youth Convention',
        #     organization=international,
        #     start_date='2017-07-02',
        #     end_date='2017-07-02',
        #     panel=3,
        # )
        # international_youth_convention_quartet_session = international_youth_convention.sessions.create(kind=Session.KIND.quartet)
        # international_youth_convention_chorus_session = international_youth_convention.sessions.create(kind=Session.KIND.chorus)

        district_alpha_fall_convention=ConventionFactory(
            name='District Alpha Fall Convention',
            start_date='2017-10-01',
            end_date='2017-10-02',
            organization=district_alpha,
            panel=3,
            season=Convention.SEASON.fall,
        )
        district_alpha_spring_convention=ConventionFactory(
            name='District Alpha Spring Convention',
            start_date='2018-05-01',
            end_date='2018-05-02',
            organization=district_alpha,
            panel=3,
            season=Convention.SEASON.spring,
        )
        district_beta_fall_convention=ConventionFactory(
            name='District Beta Fall Convention',
            start_date='2017-09-01',
            end_date='2017-09-02',
            organization=district_beta,
            panel=3,
            season=Convention.SEASON.fall,
        )
        district_beta_division_north_spring_convention=ConventionFactory(
            name='BTA Division North Spring Convention',
            start_date='2018-03-01',
            end_date='2018-03-01',
            organization=district_beta,
            year=2018,
            panel=2,
            season=Convention.SEASON.spring,
        )
        district_beta_division_south_spring_convention=ConventionFactory(
            name='BTA Division South Spring Convention',
            start_date='2018-04-01',
            end_date='2018-04-01',
            organization=district_beta,
            year=2018,
            panel=2,
            season=Convention.SEASON.spring,
        )
        district_beta_division_east_west_spring_convention=ConventionFactory(
            name='BTA Division East & West Spring Convention',
            start_date='2018-04-01',
            end_date='2018-04-01',
            organization=district_beta,
            year=2018,
            panel=2,
            season=Convention.SEASON.spring,
        )

        # Add Sessions
        district_alpha_fall_convention_quartet_session = SessionFactory(
            convention=district_alpha_fall_convention,
            kind=Session.KIND.quartet,
        )
        district_alpha_fall_convention_chorus_session = SessionFactory(
            convention=district_alpha_fall_convention,
            kind=Session.KIND.chorus,
        )

        district_alpha_spring_convention_quartet_session = SessionFactory(
            convention=district_alpha_spring_convention,
            kind=Session.KIND.quartet,
        )
        district_alpha_spring_convention_chorus_session = SessionFactory(
            convention=district_alpha_spring_convention,
            kind=Session.KIND.chorus,
        )

        district_beta_fall_convention_quartet_session = SessionFactory(
            convention=district_beta_fall_convention,
            kind=Session.KIND.quartet,
        )
        district_beta_fall_convention_chorus_session = SessionFactory(
            convention=district_beta_fall_convention,
            kind=Session.KIND.chorus,
        )

        district_beta_division_north_spring_convention_quartet_session = SessionFactory(
            convention=district_beta_division_north_spring_convention,
            kind=Session.KIND.quartet,
        )
        district_beta_division_north_spring_convention_chorus_session = SessionFactory(
            convention=district_beta_division_north_spring_convention,
            kind=Session.KIND.chorus,
        )

        district_beta_division_south_spring_convention_quartet_session = SessionFactory(
            convention=district_beta_division_south_spring_convention,
            kind=Session.KIND.quartet,
        )
        district_beta_division_south_spring_convention_chorus_session = SessionFactory(
            convention=district_beta_division_south_spring_convention,
            kind=Session.KIND.chorus,
        )

        district_beta_division_east_west_spring_convention_quartet_session = SessionFactory(
            convention=district_beta_division_east_west_spring_convention,
            kind=Session.KIND.quartet,
        )
        district_beta_division_east_west_spring_convention_chorus_session = SessionFactory(
            convention=district_beta_division_east_west_spring_convention,
            kind=Session.KIND.chorus,
        )

        # Add Assignments
        conventions = Convention.objects.all()
        for convention in conventions:
            convention.assignments.create(
                status=Assignment.STATUS.active,
                category=Assignment.CATEGORY.drcj,
                kind=Assignment.KIND.official,
                person=drcj_person,
            )
            js = Officer.objects.filter(office__short_name='CA').order_by('?')[:2]
            for j in js:
                convention.assignments.create(
                    status=Assignment.STATUS.active,
                    category=Assignment.CATEGORY.admin,
                    kind=Assignment.KIND.official,
                    person=j.person,
                )
            js = Officer.objects.filter(office__short_name='MUS').order_by('?')[:convention.panel]
            for j in js:
                convention.assignments.create(
                    status=Assignment.STATUS.active,
                    category=Assignment.CATEGORY.music,
                    kind=Assignment.KIND.official,
                    person=j.person,
                )
            js = Officer.objects.filter(office__short_name='PER').order_by('?')[:convention.panel]
            for j in js:
                convention.assignments.create(
                    status=Assignment.STATUS.active,
                    category=Assignment.CATEGORY.performance,
                    kind=Assignment.KIND.official,
                    person=j.person,
                )
            js = Officer.objects.filter(office__short_name='SNG').order_by('?')[:convention.panel]
            for j in js:
                convention.assignments.create(
                    status=Assignment.STATUS.active,
                    category=Assignment.CATEGORY.singing,
                    kind=Assignment.KIND.official,
                    person=j.person,
                )

        # Convention New
        if options['breakpoint'] == 'conventions_created':
            return

        # Add Grantors
        GrantorFactory(
            organization=district_alpha,
            session=district_alpha_fall_convention_quartet_session,
        )
        GrantorFactory(
            organization=district_alpha,
            session=district_alpha_fall_convention_chorus_session,
        )
        GrantorFactory(
            organization=district_alpha,
            session=district_alpha_spring_convention_quartet_session,
        )
        GrantorFactory(
            organization=district_alpha,
            session=district_alpha_spring_convention_chorus_session,
        )
        GrantorFactory(
            organization=district_beta,
            session=district_beta_fall_convention_quartet_session,
        )
        GrantorFactory(
            organization=district_beta,
            session=district_beta_fall_convention_chorus_session,
        )
        GrantorFactory(
            organization=district_beta_division_north,
            session=district_beta_division_north_spring_convention_quartet_session,
        )
        GrantorFactory(
            organization=district_beta_division_north,
            session=district_beta_division_north_spring_convention_chorus_session,
        )
        GrantorFactory(
            organization=district_beta_division_south,
            session=district_beta_division_south_spring_convention_quartet_session,
        )
        GrantorFactory(
            organization=district_beta_division_south,
            session=district_beta_division_south_spring_convention_chorus_session,
        )
        GrantorFactory(
            organization=district_beta_division_east,
            session=district_beta_division_east_west_spring_convention_quartet_session,
        )
        GrantorFactory(
            organization=district_beta_division_east,
            session=district_beta_division_east_west_spring_convention_chorus_session,
        )
        GrantorFactory(
            organization=district_beta_division_west,
            session=district_beta_division_east_west_spring_convention_quartet_session,
        )
        GrantorFactory(
            organization=district_beta_division_west,
            session=district_beta_division_east_west_spring_convention_chorus_session,
        )
        # Add Contests
        for convention in conventions:
            for session in convention.sessions.all():
                for grantor in session.grantors.all():
                    for award in grantor.organization.awards.all():
                        session.contests.create(
                            award=award,
                        )

        # Publish Conventions
        district_alpha_fall_convention.publish()
        district_alpha_fall_convention.save()
        district_alpha_spring_convention.publish()
        district_alpha_spring_convention.save()
        district_beta_fall_convention.publish()
        district_beta_fall_convention.save()
        district_beta_division_north_spring_convention.publish()
        district_beta_division_north_spring_convention.save()
        district_beta_division_south_spring_convention.publish()
        district_beta_division_south_spring_convention.save()
        district_beta_division_east_west_spring_convention.publish()
        district_beta_division_east_west_spring_convention.save()

        if options['breakpoint'] == 'conventions_published':
            return

        # Open the Session for Entries
        quartet_session.open()
        quartet_session.save()
        # Enter 50 Quartets at Random
        quartets = Group.objects.filter(
            kind=Group.KIND.quartet,
        ).order_by('?')[:50]
        youth_quartets = Group.objects.filter(
            kind=Group.KIND.quartet,
        ).order_by('?')[:20]
        # Create Quartet Entries
        for quartet in quartets:
            EntryFactory(
                session=quartet_session,
                group=quartet,
                is_evaluation=False,
                status=Entry.STATUS.approved,
            )
        for quartet in youth_quartets:
            EntryFactory(
                session=youth_session,
                group=quartet,
                is_evaluation=False,
                status=Entry.STATUS.approved,
            )
        # Add Participants to Entries
        for entry in quartet_session.entries.all():
            for member in entry.group.members.all():
                ParticipantFactory(
                    entry=entry,
                    member=member,
                )
        for entry in youth_session.entries.all():
            for member in entry.group.members.all():
                ParticipantFactory(
                    entry=entry,
                    member=member,
                )
        # Add Contests to Entries
        for entry in quartet_session.entries.all():
            ContestantFactory(
                entry=entry,
                contest=quartet_contest,
            )
        for entry in youth_session.entries.all():
            ContestantFactory(
                entry=entry,
                contest=youth_contest,
            )
        for entry in quartet_session.entries.all().order_by('?')[:10]:
            ContestantFactory(
                entry=entry,
                contest=dc_contest,
            )
        for entry in youth_session.entries.all().order_by('?')[:10]:
            ContestantFactory(
                entry=entry,
                contest=oy_contest,
            )
        # Close Session
        quartet_session.close()
        quartet_session.save()
        youth_session.close()
        youth_session.save()
        if options['breakpoint'] == 'session_closed':
            return
        # Verify Session
        quartet_session.verify()
        quartet_session.save()
        youth_session.verify()
        youth_session.save()

        # youth
        youth_session.start()
        youth_session.save()
        if options['breakpoint'] == 'youth_started':
            return
        # Get the first round
        youth_finals = youth_session.rounds.get(num=1)
        # Start the round
        youth_finals.start()
        youth_finals.save()
        # Score the round
        for appearance in youth_finals.appearances.filter(
            status=Appearance.STATUS.published,
        ):
            appearance.start()
            for song in appearance.songs.all():
                song.chart = appearance.entry.group.repertories.order_by('?').first().chart
                song.save()
            appearance.finish()
            for song in appearance.songs.all():
                center = random.randint(60,70)
                for score in song.scores.all():
                    offset = random.randint(-5,5)
                    score.points = center + offset
                    score.save()
            appearance.confirm()
            appearance.save()
        if options['breakpoint'] == 'youth_scored':
            return
        youth_finals.finish()
        youth_finals.announce()
        youth_finals.save()

        # Start Session
        quartet_session.start()
        quartet_session.save()
        if options['breakpoint'] == 'session_started':
            return

        # Get the first round
        quartet_quarters = quartet_session.rounds.get(num=1)
        # Start the round
        quartet_quarters.start()
        quartet_quarters.save()
        # Score the round
        for appearance in quartet_quarters.appearances.filter(
            status=Appearance.STATUS.published,
        ):
            appearance.start()
            for song in appearance.songs.all():
                song.chart = appearance.entry.group.repertories.order_by('?').first().chart
                song.save()
            appearance.finish()
            for song in appearance.songs.all():
                center = random.randint(70,80)
                for score in song.scores.all():
                    offset = random.randint(-5,5)
                    score.points = center + offset
                    score.save()
            appearance.confirm()
            appearance.save()
        if options['breakpoint'] == 'quarters_scored':
            return
        quartet_quarters.finish()
        quartet_quarters.announce()
        quartet_quarters.save()
        quartet_semis = quartet_session.rounds.get(num=2)
        quartet_semis.start()
        quartet_semis.save()
        # Score the round
        for appearance in quartet_semis.appearances.filter(
            status=Appearance.STATUS.published,
        ):
            appearance.start()
            for song in appearance.songs.all():
                song.chart = appearance.entry.group.repertories.order_by('?').first().chart
                song.save()
            appearance.finish()
            for song in appearance.songs.all():
                center = random.randint(75,85)
                for score in song.scores.all():
                    offset = random.randint(-5,5)
                    score.points = center + offset
                    score.save()
            appearance.confirm()
            appearance.save()
        if options['breakpoint'] == 'semis_scored':
            return
        quartet_semis.finish()
        quartet_semis.announce()
        quartet_semis.save()
        quartet_finals = quartet_session.rounds.get(num=3)
        quartet_finals.start()
        quartet_finals.save()
        # Score the round
        for appearance in quartet_finals.appearances.filter(
            status=Appearance.STATUS.published,
        ):
            appearance.start()
            for song in appearance.songs.all():
                song.chart = appearance.entry.group.repertories.order_by('?').first().chart
                song.save()
            appearance.finish()
            for song in appearance.songs.all():
                center = random.randint(80,90)
                for score in song.scores.all():
                    offset = random.randint(-3,3)
                    score.points = center + offset
                    score.save()
            appearance.confirm()
            appearance.save()
        if options['breakpoint'] == 'finals_scored':
            return
