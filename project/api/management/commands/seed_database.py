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
        # Create International and Districts
        bhs=OrganizationFactory(
            name='Barbershop Harmony Society',
            short_name='BHS',
            kind=Organization.KIND.international,
        )
        district=OrganizationFactory(
            name='BHS District',
            short_name='DIS',
            parent=bhs,
            kind=Organization.KIND.district,
        )
        division=OrganizationFactory(
            name='BHS Division',
            short_name='DIV',
            parent=district,
            kind=Organization.KIND.division,
        )
        affiliate=OrganizationFactory(
            name='INT Affiliate',
            short_name='INT',
            parent=bhs,
            kind=Organization.KIND.affiliate,
        )
        # Create Core Offices
        scjc_office=OfficeFactory(
            name='Society Chairman of C&J',
            short_name='SCJC',
            is_cj=True,
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
            is_cj=True,
            is_convention_manager=True,
            is_session_manager=True,
            is_organization_manager=True,
            is_award_manager=True,
        )
        ca_office=OfficeFactory(
            name='Contest Administrator',
            short_name='CA',
            is_cj=True,
            is_scoring_manager=True,
        )
        mus_office=OfficeFactory(
            name='Music Judge',
            short_name='MUS',
            is_cj=True,
        )
        per_office=OfficeFactory(
            name='Performance Judge',
            short_name='PER',
            is_cj=True,
        )
        sng_office=OfficeFactory(
            name='Singing Judge',
            short_name='SNG',
            is_cj=True,
        )
        quartet_office=OfficeFactory(
            name='Quartet Representative',
            short_name='QREP',
            is_group_manager=True,
        )
        # Create Core Officers
        scjc_officer=OfficerFactory(
            office=scjc_office,
            person=scjc_person,
            organization=bhs,
            status=Officer.STATUS.active,
        )
        scjc_dis=OfficerFactory(
            office=scjc_office,
            person=scjc_person,
            organization=district,
            status=Officer.STATUS.active,
        )
        scjc_div=OfficerFactory(
            office=scjc_office,
            person=scjc_person,
            organization=division,
            status=Officer.STATUS.active,
        )
        drcj_officer=OfficerFactory(
            office=drcj_office,
            person=drcj_person,
            organization=district,
            status=Officer.STATUS.active,
        )
        drcj_div=OfficerFactory(
            office=drcj_office,
            person=drcj_person,
            organization=division,
            status=Officer.STATUS.active,
        )
        ca_officer=OfficerFactory(
            office=ca_office,
            person=ca_person,
            organization=bhs,
            status=Officer.STATUS.active,
        )
        # Create Charts
        charts = ChartFactory.create_batch(
            size=500,
            status=Chart.STATUS.active,
        )
        # Create Quartets
        quartets = GroupFactory.create_batch(
            size=50,
            kind=Group.KIND.quartet,
            organization=district,
        )
        division_quartets = GroupFactory.create_batch(
            size=20,
            kind=Group.KIND.quartet,
            organization=division,
        )
        groups = Group.objects.filter(
            kind__gte=30,
        )
        for idx, quartet in enumerate(groups):
            i = 1
            while i <= 4:
                if i==1 and idx==0:
                    person = quartet_person
                else:
                    try:
                        person = PersonFactory()
                    except IntegrityError:
                        continue
                MemberFactory(
                    group=quartet,
                    person=person,
                    part=i,
                    status=Member.STATUS.active,
                )
                OfficerFactory(
                    office=quartet_office,
                    group=quartet,
                    person=person,
                    status=Member.STATUS.active,
                )
                i += 1
        for group in groups:
            i = 1
            while i <= 6:
                try:
                    chart = Chart.objects.order_by('?').first()
                    RepertoryFactory(
                        group=group,
                        chart=chart,
                    )
                except IntegrityError:
                    continue
                i += 1
        # Create Judges
        mus_judges=OfficerFactory.create_batch(
            size=30,
            office=mus_office,
            organization=bhs,
            status=Officer.STATUS.active,
        )
        per_judges=OfficerFactory.create_batch(
            size=30,
            office=per_office,
            organization=bhs,
            status=Officer.STATUS.active,
        )
        sng_judges=OfficerFactory.create_batch(
            size=30,
            office=sng_office,
            organization=bhs,
            status=Officer.STATUS.active,
        )
        # Create Awards
        quartet_award=AwardFactory(
            name='International Quartet Championship',
            organization=bhs,
            rounds=3,
        )
        dc_award=AwardFactory(
            name='International Dealers Choice',
            organization=bhs,
            rounds=3,
        )
        international_quartet_district_qualifier=AwardFactory(
            name='International Quartet District Qualifier',
            organization=district,
            rounds=2,
            group=quartet_award,
        )
        district_quartet_championship=AwardFactory(
            name='District Quartet Championship',
            organization=district,
            rounds=2,
        )
        division_quartet_championship=AwardFactory(
            name='Division Quartet Championship',
            organization=division,
            rounds=1,
        )
        district_quartet_division_qualifier=AwardFactory(
            name='District Quartet Division Qualifier',
            organization=division,
            rounds=1,
            group=district_quartet_championship,
        )
        ybqc_award=AwardFactory(
            name='Harmony Foundation Youth Championship',
            organization=bhs,
            rounds=1,
        )
        oy_award=AwardFactory(
            name='Other Youth Award',
            organization=bhs,
            rounds=1,
        )
        # Create Conventions
        convention=ConventionFactory(
            name='International Convention',
            start_date='2017-07-01',
            end_date='2017-07-08',
            organization=bhs,
        )
        convention_ybqc=ConventionFactory(
            name='Youth Harmony Convention',
            organization=bhs,
            start_date='2017-07-02',
            end_date='2017-07-02',
            panel=3
        )
        # Add Assignments
        drcj_assignment=AssignmentFactory(
            category=Assignment.CATEGORY.drcj,
            person=drcj_person,
            convention=convention,
            status=Assignment.STATUS.confirmed,
        )
        ca_assignment=AssignmentFactory(
            category=Assignment.CATEGORY.ca,
            person=ca_person,
            convention=convention,
            status=Assignment.STATUS.confirmed,
        )
        drcj_assignment_ybqc=AssignmentFactory(
            category=Assignment.CATEGORY.drcj,
            person=drcj_person,
            convention=convention_ybqc,
            status=Assignment.STATUS.confirmed,
        )
        ca_assignment_ybqc=AssignmentFactory(
            category=Assignment.CATEGORY.ca,
            person=ca_person,
            convention=convention_ybqc,
            status=Assignment.STATUS.confirmed,
        )
        for judge in mus_judges[:5]:
            AssignmentFactory(
                category=Assignment.CATEGORY.music,
                person=judge.person,
                convention=convention,
                status=Assignment.STATUS.confirmed,
            )
        for judge in per_judges[:5]:
            AssignmentFactory(
                category=Assignment.CATEGORY.performance,
                person=judge.person,
                convention=convention,
                status=Assignment.STATUS.confirmed,
            )
        for judge in sng_judges[:5]:
            AssignmentFactory(
                category=Assignment.CATEGORY.singing,
                person=judge.person,
                convention=convention,
                status=Assignment.STATUS.confirmed,
            )
        for judge in mus_judges[:3]:
            AssignmentFactory(
                category=Assignment.CATEGORY.music,
                person=judge.person,
                convention=convention_ybqc,
                status=Assignment.STATUS.confirmed,
            )
        for judge in per_judges[:3]:
            AssignmentFactory(
                category=Assignment.CATEGORY.performance,
                person=judge.person,
                convention=convention_ybqc,
                status=Assignment.STATUS.confirmed,
            )
        for judge in sng_judges[:3]:
            AssignmentFactory(
                category=Assignment.CATEGORY.singing,
                person=judge.person,
                convention=convention_ybqc,
                status=Assignment.STATUS.confirmed,
            )
        # Create Quartet Session
        quartet_session=SessionFactory(
            convention=convention,
            kind=Session.KIND.quartet,
        )
        ybqc_session=SessionFactory(
            convention=convention_ybqc,
            kind=Session.KIND.quartet,
        )
        # Add Quartet Contest
        quartet_contest = ContestFactory(
            session=quartet_session,
            award=quartet_award,
            is_primary=True,
        )
        dc_contest = ContestFactory(
            session=quartet_session,
            award=dc_award,
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
                status=Entry.STATUS.accepted,
            )
        for quartet in ybqc_quartets:
            EntryFactory(
                session=ybqc_session,
                group=quartet,
                is_evaluation=False,
                status=Entry.STATUS.accepted,
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
