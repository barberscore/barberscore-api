import watson

from django.shortcuts import render

from django.views.generic import (
    ListView,
    DetailView,
)

from apps.api.models import (
    Convention,
    Contest,
    District,
    Singer,
    Chorus,
    Quartet,
    ChorusPerformance,
    QuartetPerformance,
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
        'search.html',
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


class ContestDetail(DetailView):
    model = Contest
    context_object_name = 'contest'


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


class ChorusPerformanceList(ListView):
    model = ChorusPerformance
    context_object_name = 'performances'


class ChorusPerformanceDetail(DetailView):
    model = ChorusPerformance
    context_object_name = 'performance'


class QuartetPerformanceList(ListView):
    model = QuartetPerformance
    context_object_name = 'performances'


class QuartetPerformanceDetail(DetailView):
    model = QuartetPerformance
    context_object_name = 'performance'
