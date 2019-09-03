from django_filters.rest_framework import FilterSet
# Third-Party

# Local
from .models import Group
from .models import Chart
from .models import Person
from .models import Convention


class ConventionFilterset(FilterSet):
    class Meta:
        model = Convention
        fields = {
            # 'assignments__user': [
            #     'exact',
            # ],
            'persons__owners': [
                'exact',
            ],
            'owners': [
                'exact',
            ],
            'status': [
                'exact',
            ],
        }

class GroupFilterset(FilterSet):
    class Meta:
        model = Group
        fields = {
            'owners': [
                'exact',
            ],
            'status': [
                'exact',
                'gt',
            ],
            'kind': [
                'gt',
            ],
        }

class PersonFilterset(FilterSet):
    class Meta:
        model = Person
        fields = {
            # 'user': [
            #     'exact',
            # ],
            # 'user__username': [
            #     'exact',
            # ],
            'status': [
                'exact',
            ],
        }


class ChartFilterset(FilterSet):
    class Meta:
        model = Chart
        fields = {
            'status': [
                'exact',
            ],
        }
