# from nose.tools import with_setup

# from apps.convention.factories import (
#     ContestFactory,
#     ContestantFactory,
#     PerformanceFactory,
# )

# from apps.convention.models import (
#     Contest,
#     Contestant,
#     Performance,
# )

# from factory.fuzzy import (
#     FuzzyText,
#     FuzzyInteger,
# )


# def simple():
#     contest = ContestFactory(
#         year='2014',
#         contest_level=Contest.INTERNATIONAL,
#         contest_type=Contest.QUARTET,
#     )

#     contestant = ContestantFactory(
#         name='Testifour',
#     )

#     PerformanceFactory(
#         contest=contest,
#         contestant=contestant,
#     )


# @with_setup(simple)
# def test_simple_test_case():
#     performance = Performance.objects.all()[0]
#     assert performance.__unicode__() == 'Testifour, Finals'


# def build_contest(contest):
#     contest = ContestFactory(
#         year='2000',
#         contest_level=Contest.INTERNATIONAL,
#         contest_type=Contest.SENIOR,
#     )

#     contestants = Contestant.objects.filter(
#         performances__contest=contest
#     )
#     for contestant in contestants:
#         PerformanceFactory(
#             contest=contest,
#             contestant=contestant,
#             song1=FuzzyText(),
#             mus1=FuzzyInteger(400, 500),
#             prs1=FuzzyInteger(400, 500),
#             sng1=FuzzyInteger(400, 500),
#             song2=FuzzyText(),
#             mus2=FuzzyInteger(400, 500),
#             prs2=FuzzyInteger(400, 500),
#             sng2=FuzzyInteger(400, 500),
#     )
