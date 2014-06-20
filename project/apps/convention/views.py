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
    """
    Returns details about a particular contestant.
    """
    contestant = get_object_or_404(Contestant, slug=slug)
    performances = contestant.performances.all()
    prev = contestant.next_performance.get_previous_by_stagetime().contestant
    next = contestant.next_performance.get_next_by_stagetime().contestant
    return render(
        request, 'contestant.html', {
            'contestant': contestant,
            'performances': performances,
            'prev': prev,
            'next': next,
        },
    )


def performances(request):
    """
    Returns performances ordered by the program schedule.
    """
    performances = get_list_or_404(
        Performance.objects.select_related('contest', 'contestant').order_by(
            'contest',
            'contest_round',
            'session',
            'appearance',
        )
    )
    return render(request, 'performances.html', {'performances': performances})


def contests(request):
    """
    Returns performances ordered by contest score.
    """
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
    """
    Extends the default Haystack search view.
    """
    response = basic_search(
        request,
        template='search/search.html',
        form_class=ContestantSearchForm,
        results_per_page=100,
    )
    return response
