# Django
# Standard Libary
import json
from itertools import chain
from optparse import make_option

from django.core.management.base import BaseCommand
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder

# First-Party
from api.factories import (
    AppearanceFactory,
    AssignmentFactory,
    AwardFactory,
    ChartFactory,
    ContestantFactory,
    ContestFactory,
    ConventionFactory,
    EntityFactory,
    EntryFactory,
    MemberFactory,
    OfficeFactory,
    OfficerFactory,
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
    Entity,
    Entry,
    Member,
    Office,
    Officer,
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
        admin=UserFactory(
            email='test@barberscore.com',
            password='password',
            is_staff=True,
            person=None,
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
        bhs=EntityFactory(
            name='Barbershop Harmony Society',
            long_name='Barbershop Harmony Society',
            short_name='BHS',
            kind=Entity.KIND.international,
        )
        district=EntityFactory(
            name='BHS District',
            long_name='BHS District',
            short_name='DIS',
            parent=bhs,
            kind=Entity.KIND.district,
        )
        affiliate=EntityFactory(
            name='INT Affiliate',
            long_name='INT Affiliate',
            short_name='INT',
            parent=bhs,
            kind=Entity.KIND.affiliate,
        )
        drcj_office=OfficeFactory(
            name='District Director C&J',
            long_name='District Director C&J',
            short_name='DRCJ',
            is_cj=True,
            is_drcj=True,
        )
        ca_office=OfficeFactory(
            name='Contest Administrator',
            long_name='Contest Administrator',
            short_name='CA',
            is_cj=True,
            is_ca=True,
        )
        mus_office=OfficeFactory(
            name='Music Judge',
            long_name='Music Judge',
            short_name='MUS',
            is_cj=True,
        )
        per_office=OfficeFactory(
            name='Performance Judge',
            long_name='Performance Judge',
            short_name='PER',
            is_cj=True,
        )
        sng_office=OfficeFactory(
            name='Singing Judge',
            long_name='Singing Judge',
            short_name='SNG',
            is_cj=True,
        )
        quartet_office=OfficeFactory(
            name='Quartet Representative',
            long_name='Quartet Representative',
            short_name='QREP',
            is_rep=True,
        )
        drcj_officer=OfficerFactory(
            office=drcj_office,
            person=drcj_person,
            entity=bhs,
            status=Officer.STATUS.active,
        )
        ca_officer=OfficerFactory(
            office=ca_office,
            person=ca_person,
            entity=bhs,
            status=Officer.STATUS.active,
        )
        charts = ChartFactory.create_batch(
            size=300,
        )
        quartets = EntityFactory.create_batch(
            size=50,
            kind=Entity.KIND.quartet,
        )
        for idx, quartet in enumerate(quartets):
            i = 1
            while i <= 4:
                if i==1 and idx==0:
                    person = quartet_person
                else:
                    person = PersonFactory()
                MemberFactory(
                    entity=quartet,
                    person=person,
                    part=i,
                    status=Member.STATUS.active,
                )
                OfficerFactory(
                    office=quartet_office,
                    entity=quartet,
                    person=person,
                    status=Member.STATUS.active,
                )
                i += 1


        mus_judges=OfficerFactory.create_batch(
            size=5,
            office=mus_office,
            entity=bhs,
            status=Officer.STATUS.active,
        )
        per_judges=OfficerFactory.create_batch(
            size=5,
            office=per_office,
            entity=bhs,
            status=Officer.STATUS.active,
        )
        sng_judges=OfficerFactory.create_batch(
            size=5,
            office=sng_office,
            entity=bhs,
            status=Officer.STATUS.active,
        )
        convention=ConventionFactory(
            name='International Convention',
            entity=bhs,
        )
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
        for judge in mus_judges:
            AssignmentFactory(
                category=Assignment.CATEGORY.music,
                person=judge.person,
                convention=convention,
                status=Assignment.STATUS.confirmed,
            )
        for judge in per_judges:
            AssignmentFactory(
                category=Assignment.CATEGORY.performance,
                person=judge.person,
                convention=convention,
                status=Assignment.STATUS.confirmed,
            )
        for judge in sng_judges:
            AssignmentFactory(
                category=Assignment.CATEGORY.singing,
                person=judge.person,
                convention=convention,
                status=Assignment.STATUS.confirmed,
            )
        quartet_session=SessionFactory(
            convention=convention,
            kind=Session.KIND.quartet,
        )
        quartet_award=AwardFactory(
            name='International Quartet Championship',
            entity=bhs,
        )
        quartet_contest = ContestFactory(
            session=quartet_session,
            award=quartet_award,
        )
        # Convention Breakpoint
        if options['breakpoint'] == 'Convention':
            return
        quartet_session.open()
        quartet_session.save()
        quartets = Entity.objects.filter(
            kind=Entity.KIND.quartet,
        ).order_by('?')[:50]
        for quartet in quartets:
            i = 1
            charts = list(Chart.objects.order_by('?')[:6])
            while i <= 6:
                RepertoryFactory(
                    entity=quartet,
                    chart=charts.pop(),
                )
                i += 1
        for quartet in quartets:
            EntryFactory(
                session=quartet_session,
                entity=quartet,
                representing=district,
                is_evaluation=False,
                status=Entry.STATUS.accepted,
            )

        for entry in quartet_session.entries.all():
            ContestantFactory(
                entry=entry,
                contest=quartet_contest,
            )
            for member in entry.entity.members.all():
                ParticipantFactory(
                    entry=entry,
                    member=member,
                )
        quartet_session.close()
        quartet_session.save()
        # Session Breakpoint
        if options['breakpoint'] == 'Session':
            return
        quartet_session.verify()
        quartet_quarters = quartet_session.rounds.get(num=1)
        for assignment in convention.assignments.filter(
            category__gt=Panelist.CATEGORY.aca,
        ):
            PanelistFactory(
                kind=assignment.kind,
                category=assignment.category,
                round=quartet_quarters,
                person=assignment.person,
            )
        i = 1
        # for entry in quartet_session.entries.all().order_by('?'):
        #     slot = SlotFactory(
        #         num=i,
        #         round=quartet_quarters,
        #     )
        #     AppearanceFactory(
        #         round=quartet_quarters,
        #         entry=entry,
        #         slot=slot,
        #         num=i,
        #     )
        #     i += 1
        for appearance in quartet_quarters.appearances.all():
            i = 1
            while i <= appearance.round.num_songs:
                song = SongFactory(
                    num=i,
                    appearance=appearance,
                )
                i += 1
                for panelist in quartet_quarters.panelists.all().order_by('kind'):
                    ScoreFactory(
                        category=panelist.category,
                        kind=panelist.kind,
                        song=song,
                        panelist=panelist,
                    )
