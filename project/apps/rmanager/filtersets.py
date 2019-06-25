from django_filters.rest_framework import FilterSet
# Third-Party
from django_fsm_log.models import StateLog

# Local
from .models import Round
from .models import Score


class RoundFilterset(FilterSet):
    class Meta:
        model = Round
        fields = {
            'session__convention__assignments__person__user': [
                'exact',
            ],
        }


class ScoreFilterset(FilterSet):
    class Meta:
        model = Score
        fields = {
            'panelist': [
                'exact',
            ],
            'song__appearance': [
                'exact',
            ],
        }


class StateLogFilterset(FilterSet):
    class Meta:
        model = StateLog
        fields = {
            'object_id': [
                'exact',
            ],
        }

