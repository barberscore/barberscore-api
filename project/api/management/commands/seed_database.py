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
        drch_user=UserFactory(
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
        district_north=OrganizationFactory(
            name='District North',
            short_name='NTH',
            parent=international,
            kind=Organization.KIND.district,
        )
        district_south=OrganizationFactory(
            name='District South',
            short_name='STH',
            parent=international,
            kind=Organization.KIND.district,
        )
        division_east=OrganizationFactory(
            name='Division South East',
            short_name='STH ED',
            parent=district_south,
            kind=Organization.KIND.division,
        )
        division_west=OrganizationFactory(
            name='Division South West',
            short_name='STH WD',
            parent=district_south,
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
        drcj_north_officer=OfficerFactory(
            office=drcj_office,
            person=drcj_person,
            organization=district_north,
            status=Officer.STATUS.active,
        )
        drcj_south_officer=OfficerFactory(
            office=drcj_office,
            person=drcj_person,
            organization=district_south,
            status=Officer.STATUS.active,
        )
        drcj_south_east_officer=OfficerFactory(
            office=drcj_office,
            person=drcj_person,
            organization=division_east,
            status=Officer.STATUS.active,
        )
        drcj_south_west_officer=OfficerFactory(
            office=drcj_office,
            person=drcj_person,
            organization=division_west,
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
            size=90,
            kind=Group.KIND.quartet,
        )
        n = 1
        for quartet in quartets:
            if n <= 50:
                quartet.organization = district_north
            elif n <= 70:
                quartet.organization = division_west
            elif n <= 90:
                quartet.organization = division_east
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



        member = Group.objects.filter(organization__name='District North').first().members.get(part=1)
        member.person = quartet_person
        member.save()
        member = Group.objects.filter(organization__name='Division South East').first().members.get(part=1)
        member.person = quartet_person
        member.save()
        member = Group.objects.filter(organization__name='Division South East').first().members.get(part=1)
        member.person = quartet_person
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
        international_dc_award=AwardFactory(
            name='International Dealers Choice Award',
            organization=international,
            rounds=3,
            level=Award.LEVEL.award,
        )
        district_north_quartet_championship=AwardFactory(
            name='District North Quartet Championship',
            organization=district_north,
            rounds=2,
            level=Award.LEVEL.championship,
            season=Award.SEASON.fall,
        )
        district_south_quartet_championship=AwardFactory(
            name='District South Quartet Championship',
            organization=district_south,
            rounds=2,
            level=Award.LEVEL.championship,
            season=Award.SEASON.fall,
        )
        division_west_quartet_championship=AwardFactory(
            name='Division West Quartet Championship',
            organization=division_west,
            rounds=1,
            level=Award.LEVEL.championship,
            season=Award.SEASON.spring,
        )
        division_east_quartet_championship=AwardFactory(
            name='Division East Quartet Championship',
            organization=division_east,
            rounds=1,
            level=Award.LEVEL.championship,
            season=Award.SEASON.spring,
        )
        district_north_international_quartet_championship_qualifier=AwardFactory(
            name='District North International Quartet Championship Qualifier',
            organization=district_north,
            rounds=2,
            parent=international_quartet_championship,
            level=Award.LEVEL.qualifier,
            season=Award.SEASON.spring,
        )
        district_south_international_quartet_championship_qualifier=AwardFactory(
            name='District South International Quartet Championship Qualifier',
            organization=district_south,
            rounds=2,
            parent=international_quartet_championship,
            level=Award.LEVEL.qualifier,
            season=Award.SEASON.spring,
        )
        division_west_district_south_quartet_championship_qualifier=AwardFactory(
            name='Division West District South Quartet Championship Qualifier',
            organization=division_west,
            rounds=1,
            parent=district_south_quartet_championship,
            level=Award.LEVEL.qualifier,
            season=Award.SEASON.spring,
        )
        division_east_district_south_quartet_championship_qualifier=AwardFactory(
            name='Division West District South Quartet Championship Qualifier',
            organization=division_east,
            rounds=1,
            parent=district_south_quartet_championship,
            level=Award.LEVEL.qualifier,
            season=Award.SEASON.spring,
        )
        # Create Conventions and Sessions
        international_convention=ConventionFactory(
            name='International Convention',
            start_date='2017-07-01',
            end_date='2017-07-08',
            organization=international,
        )
        international_convention.sessions.create(kind=Session.KIND.quartet)
        international_convention.sessions.create(kind=Session.KIND.chorus)
        international_convention_ybqc=ConventionFactory(
            name='Youth Harmony Convention',
            organization=international,
            start_date='2017-07-02',
            end_date='2017-07-02',
            panel=3,
        )
        international_convention_ybqc.sessions.create(kind=Session.KIND.quartet)
        international_convention_ybqc.sessions.create(kind=Session.KIND.chorus)
        district_north_fall_convention=ConventionFactory(
            name='District North Fall Convention',
            start_date='2017-10-01',
            end_date='2017-10-02',
            organization=district_north,
            panel=3,
            season=Convention.SEASON.fall,
        )
        district_north_fall_convention.sessions.create(kind=Session.KIND.quartet)
        district_north_fall_convention.sessions.create(kind=Session.KIND.chorus)
        district_south_fall_convention=ConventionFactory(
            name='District South Fall Convention',
            start_date='2017-09-01',
            end_date='2017-09-02',
            organization=district_south,
            panel=3,
            season=Convention.SEASON.fall,
        )
        district_south_fall_convention.sessions.create(kind=Session.KIND.quartet)
        district_south_fall_convention.sessions.create(kind=Session.KIND.chorus)
        division_east_spring_convention=ConventionFactory(
            name='Division East Spring Convention',
            start_date='2018-03-01',
            end_date='2018-03-01',
            organization=division_east,
            year=2018,
            panel=2,
            season=Convention.SEASON.spring,
        )
        division_east_spring_convention.sessions.create(kind=Session.KIND.quartet)
        division_east_spring_convention.sessions.create(kind=Session.KIND.chorus)
        division_west_spring_convention=ConventionFactory(
            name='Division West Spring Convention',
            start_date='2018-04-01',
            end_date='2018-04-01',
            organization=division_west,
            year=2018,
            panel=2,
            season=Convention.SEASON.spring,
        )
        division_west_spring_convention.sessions.create(kind=Session.KIND.quartet)
        division_west_spring_convention.sessions.create(kind=Session.KIND.chorus)
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
        if options['breakpoint'] == 'convention_new':
            return
        # Add Quartet Contest
        quartet_contest = ContestFactory(
            session=quartet_session,
            award=international_quartet_championship,
            is_primary=True,
        )
        dc_contest = ContestFactory(
            session=quartet_session,
            award=international_dc_award,
        )
        ybqc_contest = ContestFactory(
            session=ybqc_session,
            award=ybqc_award,
            is_primary=True,
        )
        oy_contest = ContestFactory(
            session=ybqc_session,
            award=oy_award,
        )
        # Publish Convention
        convention.publish()
        convention.save()
        convention_ybqc.publish()
        convention_ybqc.save()
        if options['breakpoint'] == 'convention_published':
            return
        # Open the Session for Entries
        quartet_session.open()
        quartet_session.save()
        # Enter 50 Quartets at Random
        quartets = Group.objects.filter(
            kind=Group.KIND.quartet,
        ).order_by('?')[:50]
        ybqc_quartets = Group.objects.filter(
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
        for quartet in ybqc_quartets:
            EntryFactory(
                session=ybqc_session,
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
        for entry in ybqc_session.entries.all():
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
        for entry in ybqc_session.entries.all():
            ContestantFactory(
                entry=entry,
                contest=ybqc_contest,
            )
        for entry in quartet_session.entries.all().order_by('?')[:10]:
            ContestantFactory(
                entry=entry,
                contest=dc_contest,
            )
        for entry in ybqc_session.entries.all().order_by('?')[:10]:
            ContestantFactory(
                entry=entry,
                contest=oy_contest,
            )
        # Close Session
        quartet_session.close()
        quartet_session.save()
        ybqc_session.close()
        ybqc_session.save()
        if options['breakpoint'] == 'session_closed':
            return
        # Verify Session
        quartet_session.verify()
        quartet_session.save()
        ybqc_session.verify()
        ybqc_session.save()

        # YBQC
        ybqc_session.start()
        ybqc_session.save()
        if options['breakpoint'] == 'ybqc_started':
            return
        # Get the first round
        ybqc_finals = ybqc_session.rounds.get(num=1)
        # Start the round
        ybqc_finals.start()
        ybqc_finals.save()
        # Score the round
        for appearance in ybqc_finals.appearances.filter(
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
        if options['breakpoint'] == 'ybqc_scored':
            return
        ybqc_finals.finish()
        ybqc_finals.announce()
        ybqc_finals.save()

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
