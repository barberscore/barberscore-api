from __future__ import division

from django.shortcuts import (
    render,
    redirect,
    get_list_or_404,
)

from django.contrib.auth.decorators import login_required

from django_tables2 import RequestConfig

from apps.bbs.models import (
    Performance,
)

from .tables import (
    RatingTable,
    EnterRatingTable,
    PredictionTable,
)

from .models import (
    Rating,
    Prediction,
)

from .forms import (
    RatingForm,
    PredictionForm,
)


@login_required
def ratings(request):
    # ratings = get_list_or_404(Rating)
    performances = Performance.objects.filter(contest__is_complete=False)
    performance_table = EnterRatingTable(performances)
    ratings = Rating.objects.filter(user=request.user)
    if ratings:
        table = RatingTable(ratings)
        RequestConfig(request, paginate={"per_page": 50}).configure(table)
        return render(request, 'ratings.html', {'ratings': ratings, 'table': table, 'performance_table': performance_table})
    else:
        return render(request, 'no_ratings.html', {'performance_table': performance_table})


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


@login_required
def prediction(request):
    prediction, created = Prediction.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = PredictionForm(request.POST, instance=prediction)
        if form.is_valid():
            form.save()
            return redirect('prediction')
    else:
        form = PredictionForm(instance=prediction)
    return render(request, 'prediction.html', {'form': form, 'prediction': prediction})


def predictions(request):
    predictions = get_list_or_404(Prediction)
    table = PredictionTable(predictions)
    RequestConfig(request, paginate={"per_page": 50}).configure(table)
    return render(request, 'predictions.html', {'predictions': predictions, 'table': table})
