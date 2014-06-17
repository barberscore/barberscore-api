import factory

from .models import (
    Contest,
    Contestant,
    Performance,
)


class ContestFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Contest
    FACTORY_DJANGO_GET_OR_CREATE = (
        'year',
        'contest_level',
        'contest_type',
    )


class ContestantFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Contestant
    FACTORY_DJANGO_GET_OR_CREATE = (
        'name',
    )


class PerformanceFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Performance
    contest = factory.SubFactory(ContestFactory)
    contestant = factory.SubFactory(ContestantFactory)
