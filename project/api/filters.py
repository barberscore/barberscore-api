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
    Entry,
    Grantor,
    Group,
    Member,
    Office,
    Officer,
    Organization,
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
            'kind': [
                'exact',
            ],
            'season': [
                'exact',
            ],
            'status': [
                'exact',
            ],
            'organization': [
                'exact',
            ],
            'organization__parent': [
                'exact',
            ],
            'organization__name': [
                'exact',
            ],
            'organization__kind': [
                'exact',
            ],
            'organization__officers__office__short_name': [
                'exact',
            ],
            'organization__officers__person__user': [
                'exact',
            ],
            'organization__officers__office__is_award_manager': [
                'exact',
            ],
            'organization__officers__status': [
                'exact',
                'gt',
            ],
            'organization__grantors__session__convention': [
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
            'organization__officers__person__user': [
                'exact',
            ],
            'assignments__kind': [
                'exact',
            ],
            'assignments__category': [
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
            'is_archived': [
                'exact',
            ],
        }


class GrantorFilter(FilterSet):
    class Meta:
        model = Grantor
        fields = {
            'status': [
                'exact',
            ],
            'organization': [
                'exact',
            ],
            'session': [
                'exact',
            ],
        }


class GroupFilter(FilterSet):
    class Meta:
        model = Group
        fields = {
            'id': [
                'exact',
            ],
            'is_bhs': [
                'exact',
            ],
            'kind': [
                'exact',
                'lt',
                'in',
                'lte',
            ],
            'organization': [
                'exact',
            ],
            'members__person__user': [
                'exact',
            ],
            'nomen': [
                'icontains',
            ],
            'status': [
                'exact',
                'gt',
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
            'group': [
                'exact',
            ],
            'person__user': [
                'exact',
            ],
            'is_admin': [
                'exact',
            ],
            'status': [
                'gte',
                'exact',
            ]
        }


class OfficeFilter(FilterSet):
    class Meta:
        model = Office
        fields = {
            'kind': [
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
        }


class OrganizationFilter(FilterSet):
    class Meta:
        model = Organization
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
            'officers__person__user': [
                'exact',
            ],
            'officers__office__is_award_manager': [
                'exact',
            ],
            'nomen': [
                'icontains',
            ],
            'status': [
                'exact',
                'gt',
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
            'is_bhs': [
                'exact',
            ],
            'user': [
                'exact',
            ],
            'officers__office__kind': [
                'exact',
            ],
            'officers__office__is_judge_manager': [
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
                'lt',
            ],
            'is_archived': [
                'exact',
            ],
            'convention': [
                'exact',
            ],
            'is_invitational': [
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
            'convention__assignments__category': [
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
