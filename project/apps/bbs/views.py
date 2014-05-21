from __future__ import division

from django.shortcuts import (
    render,
    get_object_or_404,
    get_list_or_404)

from .models import (
    Contest,
    Contestant,
    Score,
)


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def contests(request):
    contests = get_list_or_404(Contest)
    return render(request, 'contests.html', {'contests': contests})


def contestants(request):
    contestants = get_list_or_404(Contestant)
    return render(request, 'contestants.html', {'contestants': contestants})


def quartets(request):
    quartets = get_list_or_404(Contestant, contestant_type=1)
    return render(request, 'quartets.html', {'quartets': quartets})


def choruses(request):
    choruses = get_list_or_404(Contestant, contestant_type=2)  # need constants
    return render(request, 'choruses.html', {'choruses': choruses})


def scores(request):
    scores = get_list_or_404(Score)
    return render(request, 'scores.html', {'scores': scores})


def contest(request, slug):
    contest = get_object_or_404(Contest, slug__iexact=slug)
    return render(request, 'contest.html', {'contest': contest})


def contestant(request, slug):
    contestant = get_object_or_404(Contestant, slug__iexact=slug)
    return render(request, 'contestant.html', {'contestant': contestant})


def score(request, slug):
    score = get_object_or_404(Score, slug__iexact=slug)
    return render(request, 'score.html', {'score': score})
