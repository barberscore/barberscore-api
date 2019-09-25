


# Standard Library
import datetime
import rest_framework_jwt
# Third-Party
from factory import Faker  # post_generation,
from factory import Iterator
from factory import LazyAttribute
from factory import PostGenerationMethodCall
from factory import RelatedFactory
from factory import Sequence
from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.django import mute_signals
from factory.fuzzy import FuzzyInteger

# Django
from django.db.models.signals import pre_delete
from django.db.models.signals import pre_save
from django.db.models.signals import m2m_changed

# First-Party


from apps.bhs.models import Award
from apps.bhs.models import Chart
from apps.bhs.models import Group
from apps.bhs.models import Person
from apps.bhs.models import Convention

from rest_framework_jwt.models import User



class AwardFactory(DjangoModelFactory):
    name = Faker('word')
    status = Award.STATUS.active
    kind = Award.KIND.quartet
    level = Award.LEVEL.championship
    season = Award.SEASON.spring
    is_single = False
    threshold = None
    minimum = None

    class Meta:
        model = Award


class ChartFactory(DjangoModelFactory):
    status = Chart.STATUS.active
    title = Faker('word')
    arrangers = Faker('name_male')

    class Meta:
        model = Chart


class ConventionFactory(DjangoModelFactory):
    name = Faker('city')
    district = Convention.DISTRICT.bhs
    status = Convention.STATUS.new
    season = Convention.SEASON.spring
    panel = Convention.PANEL.quintiple
    year = 2017
    open_date = datetime.date(2017, 6, 1)
    close_date = datetime.date(2017, 6, 30)
    start_date = datetime.date(2017, 7, 1)
    end_date = datetime.date(2017, 7, 8)
    venue_name = "Grand Ole Opry"
    location = "Nashville, TN"
    timezone = 'US/Central'

    class Meta:
        model = Convention

    # @post_generation
    # def create_assignments(self, create, extracted, **kwargs):
    #     if create:
    #         AssignmentFactory(
    #             convention=self,
    #             category=Assignment.CATEGORY.drcj,
    #         )
    #         AssignmentFactory(
    #             convention=self,
    #             category=Assignment.CATEGORY.ca,
    #         )
    #         for i in range(self.panel):
    #             AssignmentFactory(
    #                 convention=self,
    #                 category=Assignment.CATEGORY.music,
    #             )
    #             AssignmentFactory(
    #                 convention=self,
    #                 category=Assignment.CATEGORY.performance,
    #             )
    #             AssignmentFactory(
    #                 convention=self,
    #                 category=Assignment.CATEGORY.singing,
    #             )


class GroupFactory(DjangoModelFactory):
    name = Faker('company')
    status = Group.STATUS.active
    kind = Group.KIND.quartet
    district = Group.DISTRICT.fwd
    code = ''
    website = ''
    image = ''
    description = ''
    notes = ''
    bhs_id = Sequence(lambda x: x)

    class Meta:
        model = Group

    # @post_generation
    # def create_members(self, create, extracted, **kwargs):
    #     if create:
    #         if self.kind == self.KIND.quartet:
    #             size = 4
    #         else:
    #             size = 20
    #         for i in range(size):
    #             MemberFactory.create(group=self)

    # @post_generation
    # def create_repertories(self, create, extracted, **kwargs):
    #     if create:
    #         for i in range(6):
    #             RepertoryFactory.create(group=self)


class PersonFactory(DjangoModelFactory):
    name = Faker('name_male')
    first_name = Faker('first_name_male')
    last_name = Faker('last_name_male')
    status = Person.STATUS.active
    email = None
    image = ''
    description = ''
    notes = ''
    bhs_id = Sequence(lambda x: '1{0:05d}'.format(x))

    class Meta:
        model = Person


@mute_signals(pre_delete, pre_save, m2m_changed)
class UserFactory(DjangoModelFactory):
    name = Faker('name_male')
    email = Faker('email')
    password = PostGenerationMethodCall('set_password', 'password')
    is_staff = False

    class Meta:
        model = User
