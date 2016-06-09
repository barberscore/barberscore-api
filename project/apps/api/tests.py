# Third-Party
# from nose import with_setup
from factory.fuzzy import FuzzyInteger
from django.core import management
from django.db import IntegrityError
# from nose.tools import eq_ as eq
# from nose.tools import ok_ as ok
# from rest_assured.testcases import (
#     BaseRESTAPITestCase,
#     ReadRESTAPITestCaseMixin,
#     ReadWriteRESTAPITestCaseMixin,
# )

# # Django
# from django.test import SimpleTestCase

# # First-Party
from apps.api.factories import (
    AdminFactory,
    AwardFactory,
    CertificationFactory,
    ChapterFactory,
    ChartFactory,
    ChorusFactory,
    ContestantFactory,
    ContestFactory,
    ConventionFactory,
    DistrictFactory,
    GroupFactory,
    InternationalChorusAwardFactory,
    InternationalFactory,
    InternationalQuartetAwardFactory,
    JudgeFactory,
    MemberFactory,
    OfficialAdminCertificationFactory,
    OrganizationFactory,
    PerformanceFactory,
    PerformerFactory,
    PersonFactory,
    QuartetFactory,
    RoleFactory,
    RoundFactory,
    ScoreFactory,
    SessionFactory,
    SongFactory,
    SpringConventionFactory,
    SubmissionFactory,
    SummerConventionFactory,
    TenorFactory,
    VenueFactory,
)
from apps.api.models import (
    Award,
    Certification,
    Contest,
    Contestant,
    Judge,
    Convention,
    Organization,
    Performance,
    Performer,
    Round,
    Score,
    Session,
    Song,
    Submission,
)


# # # Public CRUD Tests
# # class AwardPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'award'
# #     factory_class = InternationalQuartetAwardFactory


# # class CertificationPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'certification'
# #     factory_class = CertificationFactory


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


# # class JudgePublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
# #     base_name = 'judge'
# #     factory_class = JudgeFactory


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


def build_international():
    build_admin()
    venue = VenueFactory()
    bhs = InternationalFactory()
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
    admins = OfficialAdminCertificationFactory.create_batch(3)
    for admin in admins:
        JudgeFactory(
            session=quartet_session,
            certification=admin,
            category=Judge.CATEGORY.admin,
            kind=Judge.KIND.official,
            status=Judge.STATUS.validated,
        )
        JudgeFactory(
            session=chorus_session,
            certification=admin,
            category=Judge.CATEGORY.admin,
            kind=Judge.KIND.official,
            status=Judge.STATUS.validated,
        )
    categories = [
        'music',
        'presentation',
        'singing',
    ]
    chorus_judges = []
    quartet_judges = []
    for category in categories:
        i = 1
        while i <= 5:
            certification = CertificationFactory(
                status=Certification.STATUS.active,
                category=getattr(Certification.CATEGORY, category),
            )
            quartet_judge = JudgeFactory(
                session=quartet_session,
                certification=certification,
                category=getattr(Judge.CATEGORY, category),
                kind=Judge.KIND.official,
                slot=i,
                status=Judge.STATUS.validated,
            )
            quartet_judges.append(quartet_judge)
            chorus_judge = JudgeFactory(
                session=chorus_session,
                certification=certification,
                category=getattr(Judge.CATEGORY, category),
                kind=Judge.KIND.official,
                slot=i,
                status=Judge.STATUS.validated,
            )
            chorus_judges.append(chorus_judge)
            i += 1
    quartet_contest = ContestFactory(
        session=quartet_session,
        award=quartet_award,
        status=Contest.STATUS.validated,
    )
    chorus_contest = ContestFactory(
        session=chorus_session,
        award=chorus_award,
        status=Contest.STATUS.validated,
    )
    chorus_finals = RoundFactory(
        kind=Round.KIND.finals,
        num=1,
        session=chorus_session,
        status=Round.STATUS.validated,
    )
    # RoundFactory(
    #     kind=Round.KIND.finals,
    #     num=3,
    #     session=quartet_session,
    #     status=Round.STATUS.new,
    # )
    # RoundFactory(
    #     kind=Round.KIND.semis,
    #     num=2,
    #     session=quartet_session,
    #     status=Round.STATUS.new,
    # )
    quartet_quarters = RoundFactory(
        kind=Round.KIND.quarters,
        num=1,
        session=quartet_session,
        status=Round.STATUS.validated,
    )
    quartet_session.current = quartet_quarters
    quartet_session.primary = quartet_contest
    quartet_session.save()
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
        )
        s = 1
        while s <= 4:
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
        performance = PerformanceFactory(
            performer=performer,
            round=quartet_quarters,
            slot=i,
            status=Performance.STATUS.validated,
        )
        t = 1
        while t <= 2:
            song = SongFactory(
                performance=performance,
                order=t,
                status=Song.STATUS.validated,
            )
            for judge in quartet_judges:
                ScoreFactory(
                    song=song,
                    judge=judge,
                    category=judge.category,
                    kind=judge.kind,
                    status=Score.STATUS.validated,
                )
            t += 1
        i += 1
    choruses = ChorusFactory.create_batch(20)
    i = 1
    for chorus in choruses:
        performer = PerformerFactory(
            session=chorus_session,
            group=chorus,
            status=Performer.STATUS.validated,
        )
        s = 1
        while s <= 4:
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
        performance = PerformanceFactory(
            performer=performer,
            round=chorus_finals,
            slot=i,
            status=Performance.STATUS.validated,
        )
        t = 1
        while t <= 2:
            song = SongFactory(
                performance=performance,
                order=t,
                status=Song.STATUS.validated,
            )
            for judge in chorus_judges:
                ScoreFactory(
                    song=song,
                    judge=judge,
                    category=judge.category,
                    kind=judge.kind,
                    status=Score.STATUS.validated,
                )
            t += 1
        i += 1


def score_performance(performance):
    performance.start()
    performance.center = FuzzyInteger(50, 95).fuzz()
    i = 1
    for song in performance.songs.all():
        song.submission = performance.performer.submissions.all()[i]
        for score in song.scores.all():
            score.points = performance.center + FuzzyInteger(-4, 4).fuzz()
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


# @with_setup(setup_international)
# def test_stub():
#     assert True
