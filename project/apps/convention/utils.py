from __future__ import division

from .factories import (
    ContestFactory,
    ContestantFactory,
    PerformanceFactory,
)

from .models import (
    Contest,
    Contestant,
    Performance,
)

from factory.fuzzy import (
    FuzzyText,
    FuzzyInteger,
)


def create_contest():
    contest = ContestFactory(
        year='2000',
        contest_level=Contest.INTERNATIONAL,
        contest_type=Contest.QUARTET,
    )
    return contest


def create_quarters(contest):
    contestants = ContestantFactory.create_batch(size=40)
    appearance = 1
    for contestant in contestants:
        PerformanceFactory(
            contest=contest,
            contestant=contestant,
            contest_round=Performance.QUARTERS,
            appearance=appearance,
        )
        appearance += 1
    return


def place_quarter_cutoff(contest):
    place = 40
    performances = Performance.objects.filter(
        contest=contest).order_by('-appearance')[:20]
    for p in performances:
        p.place = place
        p.save()
        place -= 1
    return


def score_quarters(contest):
    score = 400
    performances = Performance.objects.filter(
        contest=contest).exclude(place=None).order_by('-appearance')
    for p in performances:
        p.mus1, p.prs1, p.sng1 = score, score, score
        p.mus2, p.prs2, p.sng2 = score, score, score
        p.save()
        score += 1
    return


def create_semis(contest):
    contestants = Contestant.objects.filter(
        performances__contest=contest,
        performances__contest_round=Performance.QUARTERS,
        performances__place=None,
    )
    appearance = 1
    for contestant in contestants:
        PerformanceFactory(
            contest=contest,
            contestant=contestant,
            contest_round=Performance.SEMIS,
            appearance=appearance,
        )
        appearance += 1
    return


def place_semi_cutoff(contest):
    place = 20
    performances = Performance.objects.filter(
        contest=contest, contest_round=Performance.SEMIS).order_by('-appearance')[:10]
    for p in performances:
        p.place = place
        p.save()
        place -= 1
    return


def score_semis(contest):
    score = 450
    performances = Performance.objects.filter(
        contest=contest, ).exclude(place=None).order_by('-appearance')
    for p in performances:
        p.mus1, p.prs1, p.sng1 = score, score, score
        p.mus2, p.prs2, p.sng2 = score, score, score
        p.save()
        score += 1
        q = Performance.objects.get(
            contestant=p.contestant,
            contest_round=Performance.QUARTERS)
        q.mus1 = p.mus1
        q.prs1 = p.prs1
        q.sng1 = p.sng1
        q.mus2 = p.mus2
        q.prs2 = p.prs2
        q.sng2 = p.sng2
        q.save()
    return


def create_finals(contest):
    contestants = Contestant.objects.filter(
        performances__contest=contest,
        performance__contest_round=Performance.SEMIS,
        performances__place=None,
    )
    appearance = 1
    for contestant in contestants:
        PerformanceFactory(
            contest=contest,
            contestant=contestant,
            contest_round=Performance.FINALS,
            appearance=appearance,
        )
        appearance += 1
    return


def score_finals(contest):
    score = 475
    performances = Performance.objects.filter(
        contest=contest).order_by('-appearance')
    for p in performances:
        p.mus1, p.prs1, p.sng1 = score, score, score
        p.mus2, p.prs2, p.sng2 = score, score, score
        p.save()
        score += 1
    return
