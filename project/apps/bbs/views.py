from __future__ import division

from django.shortcuts import (
    render,
    get_object_or_404,
    get_list_or_404)

from django_tables2 import RequestConfig

from .tables import (
    ContestantTable,
    ContestTable,
    ScoreTable
)

from .models import (
    Contest,
    Contestant,
    Score,
)


def home(request):
    return render(request, 'home.html', )


def contests(request):
    contests = get_list_or_404(Contest)
    table = ContestTable(contests)
    RequestConfig(request, paginate={"per_page": 50}).configure(table)
    return render(request, 'contests.html', {'contests': contests, 'table': table})


def contestants(request):
    contestants = get_list_or_404(Contestant)
    table = ContestantTable(contestants)
    RequestConfig(request, paginate={"per_page": 50}).configure(table)
    return render(request, 'contestants.html', {'contestants': contestants, 'table': table})


def quartets(request):
    contestants = get_list_or_404(Contestant, contestant_type=1)  # need constants
    table = ContestantTable(contestants)
    RequestConfig(request, paginate={"per_page": 50}).configure(table)
    return render(request, 'contestants.html', {'contestants': contestants, 'table': table})


def choruses(request):
    contestants = get_list_or_404(Contestant, contestant_type=2)  # need constants
    table = ContestantTable(contestants)
    RequestConfig(request, paginate={"per_page": 50}).configure(table)
    return render(request, 'contestants.html', {'contestants': contestants, 'table': table})


def scores(request):
    scores = get_list_or_404(Score)
    table = ScoreTable(scores)
    RequestConfig(request, paginate={"per_page": 50}).configure(table)
    return render(request, 'scores.html', {'scores': scores, 'table': table})


def contest(request, slug):
    contest = get_object_or_404(Contest, slug__iexact=slug)
    return render(request, 'contest.html', {'contest': contest})


def contestant(request, slug):
    contestant = get_object_or_404(Contestant, slug__iexact=slug)
    return render(request, 'contestant.html', {'contestant': contestant})


def score(request, slug):
    score = get_object_or_404(Score, slug__iexact=slug)
    return render(request, 'score.html', {'score': score})
