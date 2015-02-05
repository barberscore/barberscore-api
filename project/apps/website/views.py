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


class ConventionDetail(DetailView):
    model = Convention
    context_object_name = 'convention'


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


# class ChorusPerformanceList(ListView):
#     model = ChorusPerformance
#     context_object_name = 'performances'


# class QuartetPerformanceList(ListView):
#     model = QuartetPerformance
#     context_object_name = 'performances'


# class QuartetPerformanceDetail(DetailView):
#     model = QuartetPerformance
#     context_object_name = 'performance'


def contest_detail(request, slug):
    contest = get_object_or_404(Contest, slug=slug)
    # performances = contest.performances.all()
    return render(
        request,
        'api/contest_detail.html',
        {
            'contest': contest,
            # 'performances': performances
        },
    )


def chorus_detail(request, slug):
    chorus = get_object_or_404(Group, slug=slug)
    performances = chorus.performances.all()
    return render(
        request,
        'api/chorus_detail.html',
        {
            'chorus': chorus,
            'performances': performances
        },
    )


def quartet_detail(request, slug):
    quartet = Quartet.objects.get(slug=slug)
    members = quartet.members.all().prefetch_related("singer")
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
