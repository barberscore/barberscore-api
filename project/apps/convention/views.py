from rest_framework import viewsets

from django.shortcuts import (
    get_list_or_404,
    get_object_or_404,
    render,
)

from .models import (
    Contest,
    Contestant,
    Performance,
)

from .serializers import (
    PerformanceSerializer,
    ContestSerializer,
    ContestantSerializer,
)


class ContestantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Contestant.objects.all()
    serializer_class = ContestantSerializer
    lookup_field = 'slug'


class PerformanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    lookup_field = 'slug'


class ContestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    lookup_field = 'slug'


def contestants(request):
    contestants = get_list_or_404(
        Contestant.objects.all().order_by('name')
    )
    return render(request, 'contestants.html', {'contestants': contestants})


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
