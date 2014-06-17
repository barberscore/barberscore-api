from nose.tools import with_setup

from apps.convention.factories import (
    ContestFactory,
    ContestantFactory,
    PerformanceFactory,
)

from apps.convention.models import (
    Contest,
    Contestant,
    Performance,
)


def simple():
    contest = ContestFactory(
        year='2014',
        contest_level=Contest.INTERNATIONAL,
        contest_type=Contest.QUARTET,
    )

    contestant = ContestantFactory(
        name='Testifour',
    )

    PerformanceFactory(
        contest=contest,
        contestant=contestant,
    )


@with_setup(simple)
def test_simple_test_case():
    performance = Performance.objects.all()[0]
    assert performance.__unicode__() == 'Testifour, Finals'
