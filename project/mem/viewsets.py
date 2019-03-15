from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

# Local
from .models import Person
from .serializers import PersonSerializer

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.order_by('last_name', 'first_name')
    serializer_class = PersonSerializer
    filter_class = None
    filter_backends = [
    ]
    permission_classes = [
        IsAdminUser,
    ]
    resource_name = "person"
