from __future__ import division

from haystack.views import basic_search

from django.shortcuts import (
    get_list_or_404,
    get_object_or_404,
    render,
    redirect,
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import (
    Contestant,
    Performance,
    Contest,
)

from .forms import (
    ContestantSearchForm,
)

from noncense.forms import (
    NameForm,
)


def contestant(request, slug):
    """
    Returns details about a particular contestant.
    """
    contestant = get_object_or_404(Contestant, slug=slug)
    performances = contestant.performances.order_by('-contest_round')

    return render(
        request, 'contestant.html', {
            'contestant': contestant,
            'performances': performances,
        },
    )


def performances(request):
    """
    Returns performances ordered by the program schedule.
    """
    performances = get_list_or_404(
        Performance.objects.select_related(
            'contest', 'contestant'
        ).filter(
            place=None,
            contest_round=Performance.FINALS,
        ).order_by(
            'contest',
            'contest_round',
            'session',
            'appearance',
        )
    )
    return render(request, 'performances.html', {'performances': performances})


def contests(request):
    # RENAME TO SCORES
    """
    Returns performances ordered by contest score.
    """
    performances = Performance.objects.select_related(
        'contest', 'contestant',
    ).exclude(
        place=None,
    ).order_by(
        'contest__contest_type',
        '-contest_round',
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
        template='search.html',
        form_class=ContestantSearchForm,
        results_per_page=100,
    )
    return response
