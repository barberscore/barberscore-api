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


def calculate_scores(performance):
    if performance.mus1:
        song1_score = sum([
            performance.mus1,
            performance.prs1,
            performance.sng1,
        ]) / 1500
        song2_score = sum([
            performance.mus2,
            performance.prs2,
            performance.sng2,
        ]) / 1500
        total_score = sum([
            performance.mus1,
            performance.prs1,
            performance.sng1,
            performance.mus2,
            performance.prs2,
            performance.sng2,
        ]) / 3000
        performance.song1_score = song1_score
        performance.song2_score = song2_score
        performance.total_score = total_score
        performance.save()
    else:
        return None


def create_contest():
    contest = ContestFactory(
        year='2000',
        contest_level=Contest.INTERNATIONAL,
        contest_type=Contest.QUARTET,
    )
    return contest


def create_contestants():
    contestants = ContestantFactory.create_batch(size=40)
    return contestants


def create_performance(contest, contestant, contest_round):
    performance = PerformanceFactory(
        contest=contest,
        contestant=contestant,
        contest_round=contest_round,
    )
    return performance


def create_cut(contest, cutoff, next_round):
    PerformanceFactory.reset_sequence()
    performances = Performance.objects.filter(contest=contest)
    cut = performances.order_by('-total_score')[:cutoff]
    for c in cut:
        create_performance(contest, c.contestant, next_round)
    return
