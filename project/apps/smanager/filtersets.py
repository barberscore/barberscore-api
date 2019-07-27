from django_filters.rest_framework import FilterSet
# Third-Party

# Local
from .models import Session
from .models import Entry


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

class SessionFilterset(FilterSet):
    class Meta:
        model = Session
        fields = {
            'status': [
                'exact',
            ],
            'kind': [
                'exact',
            ],
            'is_invitational': [
                'exact',
            ],
        }


class EntryFilterset(FilterSet):
    class Meta:
        model = Entry
        fields = {
            'status': [
                'exact',
            ],
            'session__status': [
                'exact',
                'lt',
            ],
            'group_id': [
                'exact',
            ],
        }
