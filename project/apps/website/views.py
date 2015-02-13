from __future__ import division

import watson

from django.shortcuts import (
    render,
    get_object_or_404,
)

from django.views.generic import (
    ListView,
    DetailView,
)

from apps.api.models import (
    Convention,
    Contest,
    District,
    Singer,
    Group,
    Chorus,
    Quartet,
    Performance,
    # ChorusPerformance,
    # QuartetPerformance,
)


def home(request):
    return render(
        request,
        'home.html',
    )


def search(request):
    term = request.GET.get('q', None)
    if term:
        results = watson.search(term)
    else:
        results = None
    return render(
        request,
        'api/search.html',
        {'results': results}
    )


class ChorusList(ListView):
    model = Chorus
    context_object_name = 'choruses'


class ChorusDetail(DetailView):
    model = Chorus
    context_object_name = 'chorus'


class ConventionList(ListView):
    model = Convention
    context_object_name = 'conventions'


class QuartetList(ListView):
    model = Quartet
    context_object_name = 'quartets'


class QuartetDetail(DetailView):
    model = Quartet
    context_object_name = 'quartet'


class ContestList(ListView):
    model = Contest
    context_object_name = 'contests'


class DistrictList(ListView):
    model = District
    context_object_name = 'districts'


class DistrictDetail(DetailView):
    model = District
    context_object_name = 'district'


class SingerList(ListView):
    model = Singer
    context_object_name = 'singers'


class SingerDetail(DetailView):
    model = Singer
    context_object_name = 'singer'


class PerformanceList(ListView):
    model = Performance
    context_object_name = 'performances'


def contest_detail(request, slug):
    contest = get_object_or_404(Contest, slug=slug)
    performances = contest.performances.all().order_by('round', 'place')
    return render(
        request,
        'api/contest_detail.html',
        {
            'contest': contest,
            'performances': performances
        },
    )


def chorus_detail(request, slug):
    chorus = get_object_or_404(Chorus, slug=slug)
    performances = chorus.performances.all()
    return render(
        request,
        'api/chorus_detail.html',
        {
            'chorus': chorus,
            'performances': performances
        },
    )


def convention_detail(request, slug):
    convention = get_object_or_404(Convention, slug=slug)
    return render(
        request,
        'api/convention_detail.html',
        {
            'convention': convention,
        },
    )


def quartet_detail(request, slug):
    quartet = get_object_or_404(Quartet, slug=slug)
    members = quartet.members.all()
    performances = quartet.performances.all()

    return render(
        request,
        'api/quartet_detail.html',
        {
            'quartet': quartet,
            'members': members,
            'performances': performances
        },
    )


def performance_detail(request, id):
    performance = get_object_or_404(Performance, pk=id)
    return render(
        request,
        'api/performance_detail.html',
        {
            'performance': performance,
        },
    )
