from django_filters.rest_framework import FilterSet
# Third-Party
from django_fsm_log.models import StateLog

# Local

from .models import User

class StateLogFilterset(FilterSet):
    class Meta:
        model = StateLog
        fields = {
            'object_id': [
                'exact',
            ],
        }


class UserFilterset(FilterSet):
    class Meta:
        model = User
        fields = {
            'username': [
                'exact',
            ],
        }
