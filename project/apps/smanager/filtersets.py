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
                'exact',
            ],
            'kind': [
                'exact',
            ],
            'is_invitational': [
                'exact',
            ],
            # 'convention__assignments__person__user': [
            #     'exact',
            # ],
            # 'convention__status': [
            #     'exact',
            # ],
            # 'convention__assignments__category': [
            #     'exact',
            # ],
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
