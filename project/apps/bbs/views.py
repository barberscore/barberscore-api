from __future__ import division

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    get_list_or_404)

from django.contrib.auth.decorators import login_required

from django_tables2 import RequestConfig

from .tables import (
    PerformanceTable,
    ContestantTable,
    # ContestTable,
    RatingTable,
)

from .models import (
    Contest,
    Contestant,
    Performance,
    Rating,
    Singer,
)

from .forms import (
    RatingForm,
    ProfileForm,
)


def home(request):
    return render(request, 'home.html')


def success(request):
    return render(request, 'success.html')


def submit_and_next(request):
    return render(request, 'success.html')


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})
 # ##############


def contestants(request):
    contestants = get_list_or_404(Contestant)
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


@login_required
def ratings(request):
    # ratings = get_list_or_404(Rating)
    ratings = Rating.objects.filter(user=request.user)
    if ratings:
        table = RatingTable(ratings)
        RequestConfig(request, paginate={"per_page": 50}).configure(table)
        return render(request, 'ratings.html', {'ratings': ratings, 'table': table})
    else:
        return render(request, 'no_ratings.html')

# ###########


def contestant(request, contestant):
    contestant = get_object_or_404(Contestant, slug=contestant)
    performances = Performance.objects.filter(contestant=contestant).order_by('stage_time')
    singers = Singer.objects.filter(contestant=contestant)
    return render(request, 'contestant.html', {'contestant': contestant, 'performances': performances, 'singers': singers})


def contest(request, contest, contest_round):
    contest = get_object_or_404(Contest, slug=contest)
    performances = Performance.objects.filter(
        contest=contest,
        contest_round__iexact=contest_round).order_by('slot')
    if performances:
        table = PerformanceTable(performances)
        RequestConfig(request, paginate={"per_page": 50}).configure(table)
        return render(request, 'contest.html', {'contest': contest, 'performances': performances, 'table': table})
    else:
        return render(request, 'no_performances.html', {'contest': contest, 'contest_round': contest_round})


def performance(request, performance):
    performance = get_object_or_404(Performance, slug=performance)
    return render(request, 'performance.html', {'performance': performance})


@login_required
def rating(request, performance):
    performance = Performance.objects.get(slug__iexact=performance)
    next_performance = performance.get_next_by_stage_time()
    rating, created = Rating.objects.get_or_create(user=request.user, performance=performance)
    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()
            return redirect('rating', next_performance.slug)
    else:
        form = RatingForm(instance=rating)
    return render(request, 'rating.html', {'form': form, 'rating': rating, 'performance': performance})
