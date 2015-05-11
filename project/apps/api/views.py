import logging
log = logging.getLogger(__name__)

import watson

from rest_framework import (
    mixins,
    viewsets,
    # filters,
)

from .models import (
    Convention,
    Chorus,
    Quartet,
)

from .serializers import (
    ConventionSerializer,
    ChorusSerializer,
    QuartetSerializer,
    SearchSerializer,
)


class SearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = SearchSerializer

    def get_queryset(self, *args, **kwargs):
        request = self.request
        term = request.GET.get('q', None)
        if term:
            queryset = watson.search(term)
        else:
            queryset = None
        print queryset
        return queryset


class ConventionViewSet(viewsets.ModelViewSet):
    queryset = Convention.objects.filter(
        name__in=[
            'Philadelphia 2010',
            'Kansas City 2011',
            'Portland 2012',
            'Toronto 2013',
            'Las Vegas 2014',
            'Pittsburgh 2015',
        ]
    ).prefetch_related('contests__contestants__performances')
    serializer_class = ConventionSerializer
    lookup_field = 'slug'


class ChorusViewSet(viewsets.ModelViewSet):
    queryset = Chorus.objects.all().prefetch_related('contestants__performances')
    serializer_class = ChorusSerializer
    lookup_field = 'slug'
    filter_fields = (
        'name',
    )


class QuartetViewSet(viewsets.ModelViewSet):
    queryset = Quartet.objects.all()
    serializer_class = QuartetSerializer
    lookup_field = 'slug'
    filter_fields = (
        'name',
    )
