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
    ConventionTable,
    ScoreTable,
)

from .models import (
    Convention,
    Contestant,
    Performance,
    Score,
)

from .forms import (
    ScoreForm,
    ProfileForm,
)


def home(request):
    return render(request, 'home.html', )


@login_required
def score(request, performance):
    s, created = Score.objects.get_or_create(user=request.user, performance_id=performance)
    if request.method == 'POST':
        form = ScoreForm(request.POST, instance=s)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ScoreForm(instance=s)
    return render(request, 'score.html', {'form': form, 'score': s})


def success(request):
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


def contestants(request):
    contestants = get_list_or_404(Contestant)
    table = ContestantTable(contestants)
    RequestConfig(request, paginate={"per_page": 50}).configure(table)
    return render(request, 'table.html', {'contestants': contestants, 'table': table})


def conventions(request):
    conventions = get_list_or_404(Convention)
    table = ConventionTable(conventions)
    RequestConfig(request, paginate={"per_page": 50}).configure(table)
    return render(request, 'table.html', {'conventions': conventions, 'table': table})


def performances(request):
    performances = get_list_or_404(Performance)
    table = PerformanceTable(performances)
    RequestConfig(request, paginate={"per_page": 50}).configure(table)
    return render(request, 'table.html', {'performances': performances, 'table': table})


def scores(request):
    scores = get_list_or_404(Score)
    table = ScoreTable(scores)
    RequestConfig(request, paginate={"per_page": 50}).configure(table)
    return render(request, 'table.html', {'scores': scores, 'table': table})


def contestant(request, contestant):
    contestant = get_object_or_404(Contestant, slug=contestant)
    return render(request, 'contestant.html', {'contestant': contestant})


def convention(request, convention):
    convention = get_object_or_404(Convention, slug=convention)
    # table = ConventionTable(convention)
    # RequestConfig(request, paginate={"per_page": 50}).configure(table)
    return render(request, 'convention.html', {'convention': convention})


def performance(request, performance):
    performance = get_object_or_404(Performance, pk=performance)
    score, is_created = Score.objects.get_or_create(user=request.user, performance=performance)
    if request.method == 'POST':
        form = ScoreForm(request.POST, instance=score)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ScoreForm(instance=score)
    return render(request, 'performance.html', {'form': form, 'performance': performance, 'score': score})
