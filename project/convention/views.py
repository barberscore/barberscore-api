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

# from django.core.exceptions import (
#     DoesNotExist,
# )

from .models import (
    Contestant,
    Performance,
    Note,
)

from .forms import (
    ContestantSearchForm,
    NoteForm,
    ProfileForm,
)

from noncense.forms import (
    NameForm,
)


def contestant(request, slug):
    """
    Returns details about a particular contestant.
    """
    contestant = get_object_or_404(Contestant, slug=slug)
    performances = contestant.performances.all()
    try:
        prev = contestant.next_performance.get_previous_by_stagetime().contestant
    except Performance.DoesNotExist:
        prev = None
    try:
        next = contestant.next_performance.get_next_by_stagetime().contestant
    except Performance.DoesNotExist:
        next = None
    if request.user.is_authenticated():
        note, created = Note.objects.get_or_create(
            contestant=contestant,
            profile=request.user.profile,
        )
    else:
        note = None

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                """Note saved.""",
            )
    else:
        form = NoteForm(instance=note)
    return render(
        request, 'contestant.html', {
            'contestant': contestant,
            'performances': performances,
            'prev': prev,
            'next': next,
            'form': form,
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
            place=None
        ).exclude(
            contest_round=Performance.QUARTERS,
        ).order_by(
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


@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileForm(request.POST, prefix='p', instance=request.user.profile)
        u_form = NameForm(request.POST, prefix='u', instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, 'Profile details updated.')
            return redirect('profile')
    else:
        p_form = ProfileForm(prefix='p', instance=request.user.profile)
        u_form = NameForm(prefix='u', instance=request.user)
    return render(
        request,
        'profile.html', {
            'p_form': p_form,
            'u_form': u_form,
        }
    )
