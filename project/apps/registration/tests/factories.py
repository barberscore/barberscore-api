


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
from apps.registration.models import Repertory
from apps.registration.models import Assignment
from apps.registration.models import Contest
from apps.registration.models import Entry
from apps.registration.models import Session

from rest_framework_jwt.models import User



class AssignmentFactory(DjangoModelFactory):
    # status = Assignment.STATUS.active
    kind = Assignment.KIND.official
    # convention = SubFactory('factories.ConventionFactory')
    session = SubFactory('apps.registration.tests.factories.SessionFactory')

    class Meta:
        model = Assignment


class ContestFactory(DjangoModelFactory):
    # status = Contest.STATUS.included
    session = SubFactory('apps.registration.tests.factories.SessionFactory')
    # award = SubFactory('factories.AwardFactory')

    class Meta:
        model = Contest


class EntryFactory(DjangoModelFactory):
    status = Entry.STATUS.new
    is_evaluation = True
    is_private = False
    session = SubFactory('apps.registration.tests.factories.SessionFactory')
    # group = SubFactory('factories.GroupFactory')

    class Meta:
        model = Entry


class RepertoryFactory(DjangoModelFactory):
    # status = Repertory.STATUS.active
    # group = SubFactory('factories.GroupFactory')
    entry = SubFactory('apps.registration.tests.factories.EntryFactory')

    class Meta:
        model = Repertory


class SessionFactory(DjangoModelFactory):
    status = Session.STATUS.new
    kind = Session.KIND.quartet
    name = "International Championship"
    district = Session.DISTRICT.bhs
    is_invitational = False
    num_rounds = 2
    # convention = SubFactory('factories.ConventionFactory')

    class Meta:
        model = Session

    # @post_generation
    # def create_rounds(self, create, extracted, **kwargs):
    #     if create:
    #         for i in range(self.num_rounds):
    #             num = i + 1
    #             kind = self.num_rounds - i
    #             RoundFactory(
    #                 session=self,
    #                 num=num,
    #                 kind=kind,
    #             )


@mute_signals(pre_delete, pre_save, m2m_changed)
class UserFactory(DjangoModelFactory):
    name = Faker('name_male')
    email = Faker('email')
    password = PostGenerationMethodCall('set_password', 'password')
    is_staff = False

    class Meta:
        model = User
