from django_filters.rest_framework import FilterSet

# Local
from .models import Assignment
from .models import Convention

class AssignmentFilterset(FilterSet):
    class Meta:
        model = Assignment
        fields = {
            'user': [
                'exact',
            ],
            'status': [
                'exact',
            ],
            'convention__status': [
                'exact',
            ],
        }


class ConventionFilterset(FilterSet):
    class Meta:
        model = Convention
        fields = {
            'assignments__user': [
                'exact',
            ],
            'assignments__status': [
                'exact',
            ],
            'status': [
                'exact',
            ],
        }
