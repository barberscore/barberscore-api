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
    Note,
)

from .forms import (
    ContestantSearchForm,
    NoteForm,
    ProfileForm,
)


def contestant(request, slug):
    """
    Returns details about a particular contestant.
    """
    contestant = get_object_or_404(Contestant, slug=slug)
    performances = contestant.performances.all()
    prev = contestant.next_performance.get_previous_by_stagetime().contestant
    next = contestant.next_performance.get_next_by_stagetime().contestant
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
        '-contest_round',
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
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile details updated.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'form': form})
