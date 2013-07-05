from __future__ import division

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    get_list_or_404)

from django_tables2 import RequestConfig

from .tables import (
    PerformanceTable,
    ContestantTable,
    # ContestTable,
    ScoreTable
)

from .models import (
    Contest,
    Contestant,
    Performance,
    Singer,
)


def home(request):
    scores = Contest.objects.filter(is_complete=True).order_by('date')
    schedules = Contest.objects.filter(is_complete=False).order_by('date')
    return render(request, 'home.html', {'scores': scores, 'schedules': schedules})


def success(request):
    return render(request, 'success.html')


def submit_and_next(request):
    return render(request, 'success.html')


def contestants(request):
    contestants = get_list_or_404(Contestant)
        # next_performance_slug = performance.get_next_by_stage_time()
        # prior_performance_slug
    # return redirect('rating', next_performance.slug)
    table = ContestantTable(contestants)
    RequestConfig(request, paginate={"per_page": 50}).configure(table)
    return render(request, 'contestants.html', {'contestants': contestants, 'table': table})


def contests(request):
    return render(request, 'contests.html')


def performances(request):
    performances = Performance.objects.all()
    if performances:
        table = PerformanceTable(performances)
        RequestConfig(request, paginate={"per_page": 50}).configure(table)
        return render(request, 'performances.html', {'performances': performances, 'table': table})
    else:
        return render(request, 'no_performances.html')


def contestant(request, contestant):
    contestant = get_object_or_404(Contestant, slug=contestant)
    performances = Performance.objects.filter(contestant=contestant).order_by('stage_time')
    singers = Singer.objects.filter(contestant=contestant)
    return render(request, 'contestant.html', {'contestant': contestant, 'performances': performances, 'singers': singers})


def contest(request, contest):
    contest = get_object_or_404(Contest, slug=contest)
    performances = Performance.objects.filter(
        contest=contest).order_by('slot')
    if performances:
        table = PerformanceTable(performances)
        RequestConfig(request, paginate={"per_page": 50}).configure(table)
        return render(request, 'contest.html', {'contest': contest, 'performances': performances, 'table': table})
    else:
        return render(request, 'no_performances.html', {'contest': contest})


def performance(request, performance):
    performance = get_object_or_404(Performance, slug=performance)
    return render(request, 'performance.html', {'performance': performance})


def score(request, contest):
    contest = get_object_or_404(Contest, slug=contest)
    performances = Performance.objects.filter(
        contest=contest).exclude(is_complete=False).order_by('place')
    if performances:
        table = ScoreTable(performances)
        RequestConfig(request, paginate={"per_page": 50}).configure(table)
        return render(request, 'contest.html', {'contest': contest, 'performances': performances, 'table': table})
    else:
        return render(request, 'no_performances.html', {'contest': contest})
