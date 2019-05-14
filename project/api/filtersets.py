from django_filters.rest_framework import FilterSet
# Third-Party
from django_fsm_log.models import StateLog

# Local
from .models import Assignment
from .models import Convention
from .models import Round
from .models import Score
from .models import Session
from .models import User


class AssignmentFilterset(FilterSet):
    class Meta:
        model = Assignment
        fields = {
            'person__user': [
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
            'assignments__person__user': [
                'exact',
            ],
            'assignments__status': [
                'exact',
            ],
            'status': [
                'exact',
            ],
        }


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
