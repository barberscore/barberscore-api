from __future__ import division

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    get_list_or_404)

from django.contrib.auth.decorators import login_required

from django_tables2 import RequestConfig

from apps.bbs.models import (
    Performance,
)

from .tables import (
    RatingTable,
)

from .models import (
    Rating,
)

from .forms import (
    RatingForm,
)


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
