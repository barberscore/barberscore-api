# Third-Party
from django_filters.rest_framework import (
    FilterSet,
    OrderingFilter,
)

# Local
from .models import (
    Award,
    Chart,
    Contestant,
    Convention,
    Entity,
    Entry,
    Member,
    Office,
    Officer,
    Panelist,
    Participant,
    Person,
    Round,
    Score,
    Session,
    Venue,
)


class AwardFilter(FilterSet):
    class Meta:
        model = Award
        fields = {
            'nomen': [
                'icontains',
            ],
            'is_qualifier': [
                'exact',
            ],
            'kind': [
                'exact',
            ],
            'season': [
                'exact',
            ],
            'status': [
                'exact',
            ],
            'entity': [
                'exact',
            ],
            'entity__parent': [
                'exact',
            ],
            'entity__name': [
                'exact',
            ],
            'entity__kind': [
                'exact',
            ],
            'entity__officers__office__short_name': [
                'exact',
            ],
            'entity__officers__person__user': [
                'exact',
            ],
        }


class ChartFilter(FilterSet):
    class Meta:
        model = Chart
        fields = {
            'nomen': [
                'icontains',
            ],
            'status': [
                'exact',
                'gte',
            ],
        }


class ContestantFilter(FilterSet):
    class Meta:
        model = Contestant
        fields = {
            'nomen': [
                'icontains',
            ],
        }


class ConventionFilter(FilterSet):
    class Meta:
        model = Convention
        fields = {
            'status': [
                'exact',
                'lt',
            ],
            'year': [
                'exact',
            ],
            'assignments__person__user': [
                'exact',
            ],
            'assignments__kind': [
                'exact',
            ],
        }


class EntityFilter(FilterSet):
    class Meta:
        model = Entity
        fields = {
            'id': [
                'exact',
            ],
            'kind': [
                'exact',
                'lt',
                'in',
                'lte',
            ],
            'parent': [
                'exact',
            ],
            'members__person__user': [
                'exact',
            ],
            'officers__person__user': [
                'exact',
            ],
            'parent__officers__person__user': [
                'exact',
            ],
            'nomen': [
                'icontains',
            ],
            'status': [
                'exact',
                'gt',
            ],
            'officers__office__is_award_manager': [
                'exact',
            ],
            'parent__officers__office__is_award_manager': [
                'exact',
            ],
        }


class EntryFilter(FilterSet):
    class Meta:
        model = Entry
        fields = {
            'nomen': [
                'icontains',
            ],
        }


class PanelistFilter(FilterSet):
    class Meta:
        model = Panelist
        fields = {
            'nomen': [
                'icontains',
            ],
        }


class ParticipantFilter(FilterSet):
    class Meta:
        model = Participant
        fields = {
            'nomen': [
                'icontains',
            ],
        }


class MemberFilter(FilterSet):
    class Meta:
        model = Member
        fields = {
            'entity': [
                'exact',
            ],
        }


class OfficeFilter(FilterSet):
    class Meta:
        model = Office
        fields = {
            'kind': [
                'exact',
            ],
            'is_cj': [
                'exact',
            ],
        }


class OfficerFilter(FilterSet):
    ordering = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('person__name', 'personName'),
            ('office__name', 'officeName'),
        ),

        # labels do not need to retain order
        field_labels={
            'person__name': 'Person',
            'office__name': 'Office',
        }
    )

    class Meta:
        model = Officer
        fields = {
            'nomen': [
                'icontains',
            ],
            'office__short_name': [
                'exact',
            ],
            'office__kind': [
                'exact',
            ],
            'office__is_cj': [
                'exact',
            ],
        }


class PersonFilter(FilterSet):
    class Meta:
        model = Person
        fields = {
            'nomen': [
                'icontains',
            ],
            'status': [
                'exact',
            ],
            'user': [
                'exact',
            ],
            'officers__office__kind': [
                'exact',
            ],
        }


class RoundFilter(FilterSet):
    class Meta:
        model = Round
        fields = {
            'session__convention__status': [
                'exact',
            ],
            'session__convention__assignments__person__user': [
                'exact',
            ],
            'session__convention__year': [
                'exact',
            ],
            'status': [
                'exact',
                'lt',
            ],
        }


class ScoreFilter(FilterSet):
    class Meta:
        model = Score
        fields = {
            'song__appearance': [
                'exact',
            ],
        }


class SessionFilter(FilterSet):
    class Meta:
        model = Session
        fields = {
            'status': [
                'exact',
            ],
            'convention': [
                'exact',
            ],
            'convention__status': [
                'exact',
            ],
            'nomen': [
                'icontains',
            ],
            'convention__assignments__person__user': [
                'exact',
            ],
            'convention__assignments__kind': [
                'exact',
            ],
        }


class VenueFilter(FilterSet):
    class Meta:
        model = Venue
        fields = {
            'nomen': [
                'icontains',
            ],
        }
