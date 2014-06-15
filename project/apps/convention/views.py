from haystack.views import basic_search

from django.shortcuts import (
    get_list_or_404,
    get_object_or_404,
    render,
)

from .models import (
    Contestant,
    Performance,
)

from .forms import (
    ContestantSearchForm,
)


def contestant(request, slug):
    contestant = get_object_or_404(Contestant, slug=slug)
    return render(request, 'contestant.html', {'contestant': contestant})


def performances(request):
    performances = get_list_or_404(
        Performance.objects.all().order_by(
            'session',
            'appearance',
        )
    )
    return render(request, 'performances.html', {'performances': performances})


def contests(request):
    performances = Performance.objects.exclude(place=None).order_by(
        'contest__contest_type',
        'place',
    )

    return render(
        request,
        'contests.html',
        {'performances': performances}
    )


def search(request):
    response = basic_search(
        request,
        template='search/search.html',
        form_class=ContestantSearchForm,
        results_per_page=100,
    )
    return response
