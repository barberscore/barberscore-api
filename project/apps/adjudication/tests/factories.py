


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
from django_fsm.signals import post_transition

# First-Party
from apps.adjudication.models import Appearance
from apps.adjudication.models import Outcome
from apps.adjudication.models import Panelist
from apps.adjudication.models import Round
from apps.adjudication.models import Score
from apps.adjudication.models import Song

from rest_framework_jwt.models import User


@mute_signals(post_transition)
class AppearanceFactory(DjangoModelFactory):
    status = Appearance.STATUS.new
    num = 1
    actual_start = None
    actual_finish = None
    round = SubFactory('apps.adjudication.tests.factories.RoundFactory')
    # group = SubFactory('factories.GroupFactory')

    class Meta:
        model = Appearance


class OutcomeFactory(DjangoModelFactory):
    round = SubFactory('apps.adjudication.tests.factories.RoundFactory')
    # award = SubFactory('factories.AwardFactory')

    class Meta:
        model = Outcome


@mute_signals(post_transition)
class PanelistFactory(DjangoModelFactory):
    status = Panelist.STATUS.new
    kind = Panelist.KIND.official
    category = Panelist.CATEGORY.drcj
    round = SubFactory('apps.adjudication.tests.factories.RoundFactory')
    # person = SubFactory('factories.PersonFactory')

    class Meta:
        model = Panelist


@mute_signals(post_transition)
class RoundFactory(DjangoModelFactory):
    status = Round.STATUS.new
    kind = Round.KIND.finals
    num = 1

    class Meta:
        model = Round


class ScoreFactory(DjangoModelFactory):
    status = Score.STATUS.new
    points = FuzzyInteger(50, 90)
    song = SubFactory('apps.adjudication.tests.factories.SongFactory')
    panelist = SubFactory('apps.adjudication.tests.factories.PanelistFactory')

    class Meta:
        model = Score


class SongFactory(DjangoModelFactory):
    status = Song.STATUS.new
    num = 1
    appearance = SubFactory('apps.adjudication.tests.factories.AppearanceFactory')
    # chart = None

    class Meta:
        model = Song


@mute_signals(pre_delete, pre_save, m2m_changed)
class UserFactory(DjangoModelFactory):
    username = Faker('uuid4')
    password = PostGenerationMethodCall('set_password', 'password')
    is_staff = False

    class Meta:
        model = User
