from django_filters.rest_framework import FilterSet
# Third-Party

# Local
from .models import Session
from .models import Entry


class SessionFilterset(FilterSet):
    class Meta:
        model = Session
        fields = {
            'status': [
                'lt',
                'gt',
                'exact',
            ],
            'owners': [
                'exact',
            ],
            'kind': [
                'exact',
            ],
            'is_invitational': [
                'exact',
            ],
            'convention_id': [
                'exact',
            ],
        }


class EntryFilterset(FilterSet):
    class Meta:
        model = Entry
        fields = {
            'owners': [
                'exact',
            ],
            'status': [
                'exact',
                'gt',
            ],
            'session__status': [
                'exact',
                'lt',
                'gt',
            ],
            'group_id': [
                'exact',
            ],
        }
