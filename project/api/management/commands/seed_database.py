# Django
from django.core.management.base import BaseCommand
import json
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from itertools import chain
from optparse import make_option

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
        drcj_user=UserFactory(
            email=drcj_person.email,
            person=drcj_person,
        )
        ca_person=PersonFactory(
            name='CA Person',
            email='ca@barberscore.com',
        )
        ca_user=UserFactory(
            email=ca_person.email,
            person=ca_person,
        )
        bhs=EntityFactory(
            name='Barbershop Harmony Society',
            long_name='Barbershop Harmony Society',
            short_name='BHS',
            kind=Entity.KIND.international,
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
        rep_office=OfficeFactory(
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
        i = 1
        while i <= 3:
            RoundFactory(
                session=quartet_session,
                num=i,
                kind=(4 - i),
            )
            i += 1
        quartet_award=AwardFactory(
            name='International Quartet Championship',
            entity=bhs,
        )
        quartet_contest = ContestFactory(
            session=quartet_session,
            award=quartet_award,
        )
        if options['breakpoint'] == 'Convention':
            return
        quartets = EntityFactory.create_batch(
            size=50,
            kind=Entity.KIND.quartet,
        )
        for quartet in quartets:
            i = 1
            while i <= 4:
                person = PersonFactory()
                MemberFactory(
                    entity=quartet,
                    person=person,
                    part=i,
                )
                OfficerFactory(
                    office=rep_office,
                    entity=quartet,
                    person=person,
                )
                i += 1
        for quartet in quartets:
            i = 1
            while i <= 6:
                RepertoryFactory(
                    entity=quartet,
                )
                i += 1
        for quartet in quartets:
            EntryFactory(
                session=quartet_session,
                entity=quartet,
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
        if options['breakpoint'] == 'Session':
            return
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
        for entry in quartet_session.entries.all().order_by('?'):
            slot = SlotFactory(
                num=i,
                round=quartet_quarters,
            )
            AppearanceFactory(
                round=quartet_quarters,
                entry=entry,
                slot=slot,
            )
            i += 1
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
