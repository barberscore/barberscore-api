# import logging
# log = logging.getLogger(__name__)

# from rest_framework import viewsets

# from .models import (
#     Singer,
#     Chorus,
#     Quartet,
# )

# from .serializers import (
#     SingerSerializer,
#     ChorusSerializer,
#     QuartetSerializer,
# )


# class QuartetViewSet(viewsets.ModelViewSet):
#     lookup_field = 'slug'
#     queryset = Quartet.objects.all()
#     serializer_class = QuartetSerializer


# class SingerViewSet(viewsets.ModelViewSet):
#     lookup_field = 'slug'
#     queryset = Singer.objects.all()
#     serializer_class = SingerSerializer


# class ChorusViewSet(viewsets.ModelViewSet):
#     queryset = Chorus.objects.all()
#     serializer_class = ChorusSerializer
#     lookup_field = 'slug'

