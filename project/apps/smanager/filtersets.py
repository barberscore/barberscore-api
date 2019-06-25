from django_filters.rest_framework import FilterSet
# Third-Party

# Local
from .models import Session


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
            'convention__assignments__person__user': [
                'exact',
            ],
            'convention__status': [
                'exact',
            ],
            'convention__assignments__category': [
                'exact',
            ],
        }
