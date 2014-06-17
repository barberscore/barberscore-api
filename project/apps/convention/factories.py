import factory

from django.utils.text import slugify

from .models import (
    Contest,
    Contestant,
    # Performance,
)


class ContestFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Contest


class ContestantFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Contestant
    slug = factory.LazyAttribute(lambda a: slugify(a.name))
