from django.test import TestCase

from nose import (
    with_setup,
)

from nose.tools import (
    eq_ as eq,
    ok_ as ok,
)

from rest_assured.testcases import (
    BaseRESTAPITestCase,
    ReadRESTAPITestCaseMixin,
    ReadWriteRESTAPITestCaseMixin,
)

from apps.api.models import (
    Award,
    Organization,
    Session,
)


from apps.api.factories import (
    AdminFactory,
    AwardFactory,
    CertificationFactory,
    ChapterFactory,
    ChartFactory,
    ContestantFactory,
    ContestFactory,
    ConventionFactory,
    OrganizationFactory,
    JudgeFactory,
    MemberFactory,
    PerformanceFactory,
    PerformerFactory,
    PersonFactory,
    GroupFactory,
    RoleFactory,
    RoundFactory,
    ScoreFactory,
    SessionFactory,
    SongFactory,
    SubmissionFactory,
    VenueFactory,
    TenorFactory,
    QuartetFactory,
    DistrictFactory,
    SpringConventionFactory,
)


# Public CRUD Tests
class AwardPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
    base_name = 'award'
    factory_class = AwardFactory


class CertificationPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
    base_name = 'certification'
    factory_class = CertificationFactory


class ChapterPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
    base_name = 'chapter'
    factory_class = ChapterFactory


class ChartPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
    base_name = 'chart'
    factory_class = ChartFactory


class ContestantPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
    base_name = 'contestant'
    factory_class = ContestantFactory


class ContestPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
    base_name = 'contest'
    factory_class = ContestFactory


class ConventionPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
    base_name = 'convention'
    factory_class = ConventionFactory


class OrganizationPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
    base_name = 'organization'
    factory_class = OrganizationFactory


class JudgePublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
    base_name = 'judge'
    factory_class = JudgeFactory


class MemberPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
    base_name = 'member'
    factory_class = MemberFactory


class PerformancePublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
    base_name = 'performance'
    factory_class = PerformanceFactory


class PerformerPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
    base_name = 'performer'
    factory_class = PerformerFactory


class PersonPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
    base_name = 'person'
    factory_class = PersonFactory


class GroupPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
    base_name = 'group'
    factory_class = GroupFactory


class RolePublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
    base_name = 'role'
    factory_class = RoleFactory


class RoundPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
    base_name = 'round'
    factory_class = RoundFactory


class ScorePublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
    base_name = 'score'
    factory_class = ScoreFactory
    user_factory = AdminFactory


class SessionPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
    base_name = 'session'
    factory_class = SessionFactory


class SongPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
    base_name = 'song'
    factory_class = SongFactory


class SubmissionPublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
    base_name = 'submission'
    factory_class = SubmissionFactory


class VenuePublicTest(ReadRESTAPITestCaseMixin, BaseRESTAPITestCase):
    base_name = 'venue'
    factory_class = VenueFactory


# Admin CRUD Tests
class ChartAdminTest(ReadWriteRESTAPITestCaseMixin, BaseRESTAPITestCase):
    base_name = 'chart'
    factory_class = ChartFactory
    user_factory = AdminFactory
    create_data = {'title': 'The Older Songs'}
    update_data = {'title': 'The Oldest Songs'}


# Round Tests

# def setup_car_spring():
#     venue = VenueFactory()
#     bhs = InternationalFactory()
#     car_district = DistrictFactory(
#         name='Cardinal District',
#         short_name='CAR',
#         long_name='Cardinal',
#     )
#     convention = SpringConventionFactory(
#         venue=venue,
#         organization=car_district,
#     )
#     quartet_session = SessionFactory(
#         kind=Session.KIND.quartet,
#         convention=convention,
#     )
#     chorus_session = SessionFactory(
#         kind=Session.KIND.chorus,
#         convention=convention,
#     )
#     quartet_qualifier = AwardFactory(
#         kind=Award.KIND.quartet,
#         championship_season=Award.SEASON.international,
#         championship_rounds=3,
#         is_primary=True,
#         is_qualification_required=True,
#         qualifier_season=Award.SEASON.spring,
#         qualifier_rounds=2,
#         threshold=76,
#         minimum=70,
#         advance=73,
#         organization=bhs,
#     )
#     quartet_qualifier = AwardFactory(
#         kind=Award.KIND.quartet,
#         season=Award.SEASON.spring,
#         championship_rounds=2,
#         is_primary=True,
#         organization=car_district,
#     )
#     quartet_contest = ContestFactory(
#         session=quartet_session,
#         award=quartet_qualifier,
#     )

#     chorus_contest = ContestFactory(
#         session=chorus_session,
#         award=chorus_qualifier
#     )


# @with_setup(setup_car_spring)
# def test_district_quartet():
#     assert True
