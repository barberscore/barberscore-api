from rest_assured.testcases import (
    BaseRESTAPITestCase,
    ReadRESTAPITestCaseMixin,
    ReadWriteRESTAPITestCaseMixin,
)

from .factories import (
    AdminFactory,
    AwardFactory,
    CertificationFactory,
    ChapterFactory,
    ChartFactory,
    ContestantFactory,
    ContestFactory,
    ConventionFactory,
    OrganizationFactory,
    # DistrictFactory,
    # InternationalFactory,
    JudgeFactory,
    MemberFactory,
    PerformanceFactory,
    PerformerFactory,
    PersonFactory,
    GroupFactory,
    # QuartetFactory,
    RoleFactory,
    # TenorFactory,
    RoundFactory,
    ScoreFactory,
    SessionFactory,
    SongFactory,
    SubmissionFactory,
    VenueFactory,
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
