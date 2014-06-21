import factory

from factory.fuzzy import (
    FuzzyInteger,
    FuzzyChoice,
    FuzzyText,
    FuzzyDecimal,
)

from factory import (
    Sequence,
)

from .models import (
    Contest,
    Contestant,
    Performance,
)

type_list = [x[0] for x in Contest.CONTEST_TYPE_CHOICES]
level_list = [x[0] for x in Contest.CONTEST_LEVEL_CHOICES]


class ContestFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Contest
    FACTORY_DJANGO_GET_OR_CREATE = (
        'year',
        'contest_level',
        'contest_type',
    )

    year = FuzzyInteger(2000, 2014)
    contest_type = FuzzyChoice(type_list)
    contest_level = FuzzyChoice(level_list)


class ContestantFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Contestant
    FACTORY_DJANGO_GET_OR_CREATE = (
        'name',
    )

    name = Sequence(lambda n: 'Contestant {0}'.format(n))
    location = FuzzyText(length=12)
    website = "http://www.google.com"
    email = 'foo@bar.com'
    phone = '7025551212'
    district = "Frank Thorne"
    picture = factory.django.ImageField()
    prelim = FuzzyDecimal(70, 90, 1)
    blurb = "Now is the time for all good men to come to the contest stage."


class QuartetFactory(ContestantFactory):
    contestant_type = Contestant.QUARTET


class PerformanceFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Performance
    contest = factory.SubFactory(ContestFactory)
    contestant = factory.SubFactory(ContestantFactory)
    appearance = Sequence(lambda n: n)


class QuarterFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Performance
    FACTORY_DJANGO_GET_OR_CREATE = (
        'contest',
        'contestant',
        'contest_round',
    )
    song1 = FuzzyText(length=24)
    song2 = FuzzyText(length=24)
    mus1 = FuzzyInteger(350, 400)
    prs1 = FuzzyInteger(350, 400)
    sng1 = FuzzyInteger(350, 400)
    mus2 = FuzzyInteger(350, 400)
    prs2 = FuzzyInteger(350, 400)
    sng2 = FuzzyInteger(350, 400)


class SemiFactory(PerformanceFactory):
    song1 = FuzzyText(length=24)
    song2 = FuzzyText(length=24)
    mus1 = FuzzyInteger(400, 450)
    prs1 = FuzzyInteger(400, 450)
    sng1 = FuzzyInteger(400, 450)
    mus2 = FuzzyInteger(400, 450)
    prs2 = FuzzyInteger(400, 450)
    sng2 = FuzzyInteger(400, 450)


class FinalFactory(PerformanceFactory):
    song1 = FuzzyText(length=24)
    song2 = FuzzyText(length=24)
    mus1 = FuzzyInteger(450, 500)
    prs1 = FuzzyInteger(450, 500)
    sng1 = FuzzyInteger(450, 500)
    mus2 = FuzzyInteger(450, 500)
    prs2 = FuzzyInteger(450, 500)
    sng2 = FuzzyInteger(450, 500)
