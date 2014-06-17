import factory

from .models import (
    Contest,
    Contestant,
    Performance,
)


class ContestFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Contest


class ContestantFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Contestant


class PerformanceFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Performance
    contest = factory.SubFactory(ContestFactory)
    contestant = factory.SubFactory(ContestantFactory)
