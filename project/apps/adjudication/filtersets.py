from django_filters.rest_framework import FilterSet
# Third-Party

# Local
from .models import Round
from .models import Score


class RoundFilterset(FilterSet):
    class Meta:
        model = Round
        fields = {
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

