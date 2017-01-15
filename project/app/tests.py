# Third-Party
# from nose import with_setup
# Standard Libary
import random
from datetime import datetime

import pytz
from factory.fuzzy import (
    FuzzyDateTime,
    FuzzyInteger,
)

# Django
from django.core import management
from django.db import IntegrityError

# First-Party
# # First-Party
from app.factories import (
    AdminFactory,
    AssignmentFactory,
    AwardFactory,
    BaritoneFactory,
    BassFactory,
    ChapterFactory,
    ChorusFactory,
    ContestantFactory,
    ContestFactory,
    ConventionFactory,
    DistrictChapterFactory,
    DistrictChorusAwardFactory,
    DistrictFactory,
    DistrictQuartetAwardFactory,
    DistrictSeniorsAwardFactory,
    DistrictYouthAwardFactory,
    GroupFactory,
    InternationalChorusAwardFactory,
    InternationalFactory,
    InternationalQuartetAwardFactory,
    InternationalSeniorsAwardFactory,
    InternationalYouthAwardFactory,
    JudgeFactory,
    LeadFactory,
    MemberFactory,
    OfficialAdminJudgeFactory,
    OfficialMusicJudgeFactory,
    OfficialPresentationJudgeFactory,
    OfficialSingingJudgeFactory,
    OrganizationFactory,
    PerformanceFactory,
    PerformerFactory,
    PersonFactory,
    PublicFactory,
    QuartetFactory,
    RoleFactory,
    RoundFactory,
    ScoreFactory,
    SessionFactory,
    SlotFactory,
    SongFactory,
    SpringConventionFactory,
    SubmissionFactory,
    SummerConventionFactory,
    TenorFactory,
    VenueFactory,
)
from app.models import (
    Assignment,
    Award,
    Contest,
    Contestant,
    Convention,
    Judge,
    Organization,
    Performance,
    Performer,
    Round,
    Score,
    Session,
    Song,
    Submission,
)


# from nose.tools import eq_ as eq
# from nose.tools import ok_ as ok
# from rest_assured.testcases import (
#     BaseRESTAPITestCase,
#     ReadRESTAPITestCaseMixin,
#     ReadWriteRESTAPITestCaseMixin,
# )

# # Django
# from django.test import SimpleTestCase




# # # Public CRUD Tests
# # class AwardPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'award'
# #     factory_class = InternationalQuartetAwardFactory


# # class JudgePublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'judge'
# #     factory_class = JudgeFactory


# # class ChapterPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'chapter'
# #     factory_class = ChapterFactory


# # class ChartPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'chart'
# #     factory_class = ChartFactory


# # class ContestantPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'contestant'
# #     factory_class = ContestantFactory


# # class ContestPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'contest'
# #     factory_class = ContestFactory


# # class ConventionPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'convention'
# #     factory_class = ConventionFactory


# # class OrganizationPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'organization'
# #     factory_class = OrganizationFactory


# # class AssignmentPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'assignment'
# #     factory_class = AssignmentFactory


# # class MemberPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'member'
# #     factory_class = MemberFactory


# # class PerformancePublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'performance'
# #     factory_class = PerformanceFactory


# # class PerformerPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'performer'
# #     factory_class = PerformerFactory


# # class PersonPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'person'
# #     factory_class = PersonFactory


# # class GroupPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'group'
# #     factory_class = GroupFactory


# # class RolePublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'role'
# #     factory_class = RoleFactory


# # class RoundPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'round'
# #     factory_class = RoundFactory


# # class ScorePublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'score'
# #     factory_class = ScoreFactory
# #     user_factory = AdminFactory


# # class SessionPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'session'
# #     factory_class = InternationalQuartetSessionFactory


# # class SongPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'song'
# #     factory_class = SongFactory


# # class SubmissionPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'submission'
# #     factory_class = SubmissionFactory


# # class VenuePublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'venue'
# #     factory_class = VenueFactory


# # # Admin CRUD Tests
# # class ChartAdminTest(ReadWriteRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'chart'
# #     factory_class = ChartFactory
# #     user_factory = AdminFactory
# #     create_data = {'title': 'The Older Songs'}
# #     update_data = {'title': 'The Oldest Songs'}


# Round Tests
def tear_down():
    management.call_command('flush', verbosity=0, interactive=False)
    return


def build_admin():
    AdminFactory()
    return


def build_primitives():
    AdminFactory()
    user = PublicFactory(
        email='joe@barberscore.com',
        name='Joe District',
    )
    representative = PersonFactory(
        name='Joe District',
        user=user,
    )
    bhs = InternationalFactory()
    district = DistrictFactory(
        parent=bhs,
        representative=representative,
    )
    InternationalQuartetAwardFactory(
        organization=bhs,
    )
    InternationalChorusAwardFactory(
        organization=bhs,
    )
    InternationalSeniorsAwardFactory(
        organization=bhs,
    )
    InternationalYouthAwardFactory(
        organization=bhs,
    )
    DistrictQuartetAwardFactory(
        organization=district,
    )
    DistrictChorusAwardFactory(
        organization=district,
    )
    DistrictSeniorsAwardFactory(
        organization=district,
    )
    DistrictYouthAwardFactory(
        organization=district,
    )

    OfficialAdminJudgeFactory.create_batch(5)
    OfficialMusicJudgeFactory.create_batch(10)
    OfficialPresentationJudgeFactory.create_batch(10)
    OfficialSingingJudgeFactory.create_batch(10)

    chapters = DistrictChapterFactory.create_batch(
        20,
        organization=district,
    )

    for chapter in chapters:
        ChorusFactory(
            organization=district,
            chapter=chapter,
        )

    persons = PersonFactory.create_batch(
        1000,
        chapter=random.choice(chapters),
    )
    quartets = QuartetFactory.create_batch(100)
    for quartet in quartets:
        TenorFactory(
            group=quartet,
            person=persons.pop()
        )
        LeadFactory(
            group=quartet,
            person=persons.pop()
        )
        BaritoneFactory(
            group=quartet,
            person=persons.pop()
        )
        BassFactory(
            group=quartet,
            person=persons.pop()
        )

    VenueFactory.create_batch(10)
    return


def build_international():
    build_admin()
    venue = VenueFactory(
        location='Bridgestone Arena',
        city='Nashville',
        state='Tennessee',
    )
    bhs = InternationalFactory()
    district_organization = DistrictFactory(
        parent=bhs,
    )
    quartet_award = InternationalQuartetAwardFactory(
        organization=bhs,
    )
    chorus_award = InternationalChorusAwardFactory(
        organization=bhs,
    )
    convention = SummerConventionFactory(
        organization=bhs,
        venue=venue,
        status=Convention.STATUS.validated,
    )
    quartet_session = SessionFactory(
        kind=Session.KIND.quartet,
        convention=convention,
        status=Session.STATUS.validated,
        num_rounds=3,
    )
    chorus_session = SessionFactory(
        kind=Session.KIND.chorus,
        convention=convention,
        status=Session.STATUS.validated,
        num_rounds=1,
    )
    admins = OfficialAdminJudgeFactory.create_batch(3)
    for admin in admins:
        AssignmentFactory(
            session=quartet_session,
            judge=admin,
            category=Assignment.CATEGORY.admin,
            kind=Assignment.KIND.official,
            status=Assignment.STATUS.validated,
        )
        AssignmentFactory(
            session=chorus_session,
            judge=admin,
            category=Assignment.CATEGORY.admin,
            kind=Assignment.KIND.official,
            status=Assignment.STATUS.validated,
        )
    categories = [
        'music',
        'presentation',
        'singing',
    ]
    chorus_assignments = []
    quartet_assignments = []
    for category in categories:
        i = 1
        while i <= 5:
            judge = JudgeFactory(
                status=Judge.STATUS.active,
                category=getattr(Judge.CATEGORY, category),
            )
            quartet_assignment = AssignmentFactory(
                session=quartet_session,
                judge=judge,
                category=getattr(Assignment.CATEGORY, category),
                kind=Assignment.KIND.official,
                slot=i,
                status=Assignment.STATUS.validated,
            )
            quartet_assignments.append(quartet_assignment)
            chorus_assignment = AssignmentFactory(
                session=chorus_session,
                judge=judge,
                category=getattr(Assignment.CATEGORY, category),
                kind=Assignment.KIND.official,
                slot=i,
                status=Assignment.STATUS.validated,
            )
            chorus_assignments.append(chorus_assignment)
            i += 1
    quartet_contest = ContestFactory(
        session=quartet_session,
        award=quartet_award,
        status=Contest.STATUS.validated,
        num_rounds=3,
    )
    chorus_contest = ContestFactory(
        session=chorus_session,
        award=chorus_award,
        status=Contest.STATUS.validated,
        num_rounds=1,
    )
    quartet_quarters = quartet_session.rounds.get(num=1)
    quartet_session.current = quartet_quarters
    quartet_session.primary = quartet_contest
    quartet_session.save()
    chorus_finals = chorus_session.rounds.get(num=1)
    chorus_session.current = chorus_finals
    chorus_session.primary = chorus_contest
    chorus_session.save()
    quartets = QuartetFactory.create_batch(50)
    i = 1
    for quartet in quartets:
        performer = PerformerFactory(
            session=quartet_session,
            group=quartet,
            status=Performer.STATUS.validated,
            representing=district_organization,
            prelim=FuzzyInteger(50, 95).fuzz(),
        )
        s = 1
        while s <= 6:
            try:
                SubmissionFactory(
                    performer=performer,
                    status=Submission.STATUS.validated,
                )
            except IntegrityError:
                SubmissionFactory(
                    performer=performer,
                    status=Submission.STATUS.validated,
                )
            s += 1
        ContestantFactory(
            contest=quartet_contest,
            performer=performer,
            status=Contestant.STATUS.validated,
        )
        slot = SlotFactory(
            round=quartet_quarters,
            num=i,
            onstage=FuzzyDateTime(
                datetime(2016, 7, 1, tzinfo=venue.timezone),
                datetime(2016, 7, 2, tzinfo=venue.timezone),
            )
        )
        PerformanceFactory(
            performer=performer,
            round=quartet_quarters,
            slot=slot,
            num=i,
            status=Performance.STATUS.validated,
        )
        i += 1
    quartet_quarters.status = Round.STATUS.validated
    quartet_quarters.save()
    choruses = ChorusFactory.create_batch(20)
    i = 1
    for chorus in choruses:
        performer = PerformerFactory(
            session=chorus_session,
            group=chorus,
            status=Performer.STATUS.validated,
            representing=district_organization,
            prelim=FuzzyInteger(50, 95).fuzz(),
        )
        s = 1
        while s <= 2:
            try:
                SubmissionFactory(
                    performer=performer,
                    status=Submission.STATUS.validated,
                )
            except IntegrityError:
                SubmissionFactory(
                    performer=performer,
                    status=Submission.STATUS.validated,
                )
            s += 1
        ContestantFactory(
            contest=chorus_contest,
            performer=performer,
            status=Contestant.STATUS.validated,
        )
        slot = SlotFactory(
            round=chorus_finals,
            num=i,
            onstage=FuzzyDateTime(
                datetime(2016, 7, 2, tzinfo=venue.timezone),
                datetime(2016, 7, 3, tzinfo=venue.timezone),
            ),
        )
        PerformanceFactory(
            slot=slot,
            performer=performer,
            round=chorus_finals,
            num=i,
            status=Performance.STATUS.validated,
        )
        i += 1
    chorus_finals.status = Round.STATUS.validated
    chorus_finals.save()


def score_performance(performance):
    performance.start()
    center = performance.performer.prelim
    i = (performance.round.num * 2) - 2
    for song in performance.songs.all():
        song.submission = performance.performer.submissions.order_by('id')[i]
        for score in song.scores.all():
            score.points = center + FuzzyInteger(-4, 4).fuzz()
            score.save()
        song.save()
        i += 1
    performance.finish()
    performance.save()
    return


def score_round(round):
    for performance in round.performances.all():
        score_performance(performance)
    return


def finish_session(session):
    for round in session.rounds.order_by('-kind'):
        score_round(round)
        round.finish()
        round.save()
    return


def calculate_session(session):
    for performer in session.performers.all():
        for performance in performer.performances.all():
            for song in performance.songs.all():
                song.calculate()
                song.save()
            performance.calculate()
            performance.save()
        performer.calculate()
        performer.save()
    return


def calculate_performer(performer):
    for performance in performer.performances.all():
        for song in performance.songs.all():
            song.calculate()
            song.save()
        performance.calculate()
        performance.save()
    performer.calculate()
    performer.save()
    return


def complete_convention(convention):
    for session in convention.sessions.all():
        finish_session(session)
        calculate_session(session)
        session.save()

# @with_setup(setup_international)
# def test_stub():
#     assert True
