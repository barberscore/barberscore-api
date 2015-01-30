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


class QuartetPerformanceList(ListView):
    model = QuartetPerformance
    context_object_name = 'performances'


class QuartetPerformanceDetail(DetailView):
    model = QuartetPerformance
    context_object_name = 'performance'


def chorus_detail(request, slug):
    chorus = get_object_or_404(Chorus, slug=slug)
    performances = chorus.chorusperformance_set.all()
    return render(
        request,
        'api/chorus_detail.html',
        {'chorus': chorus, 'performances': performances},
    )


def quartet_detail(request, slug):
    quartet = Quartet.objects.get(slug=slug)
    members = quartet.quartetmember_set.all().prefetch_related('singer')
    performances = quartet.quartetperformance_set.all()
    return render(
        request,
        'api/quartet_detail.html',
        {'quartet': quartet, 'members': members, 'performances': performances},
    )
