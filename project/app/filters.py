# Third-Party
from django_filters import rest_framework as filters

# Local
from .models import (
    Award,
    Catalog,
    Contestant,
    Convention,
    Performer,
    Person,
    Session,
    Submission,
    Venue,
)


class AwardFilter(filters.FilterSet):
    class Meta:
        model = Award
        fields = {
            'nomen': [
                'icontains',
            ],
        }


class CatalogFilter(filters.FilterSet):
    class Meta:
        model = Catalog
        fields = {
            'title': [
                'icontains',
            ],
        }


class ContestantFilter(filters.FilterSet):
    class Meta:
        model = Contestant
        fields = {
            'nomen': [
                'icontains',
            ],
        }


class ConventionFilter(filters.FilterSet):
    class Meta:
        model = Convention
        fields = {
            'status': [
                'exact',
            ],
            'year': [
                'exact',
            ],
            'kind': [
                'exact',
            ],
            'assignments__person__user': [
                'exact',
            ],
        }


class PerformerFilter(filters.FilterSet):
    class Meta:
        model = Performer
        fields = {
            'nomen': [
                'icontains',
            ],
            'entity__memberships__person__user': [
                'exact',
            ],
        }


class PersonFilter(filters.FilterSet):
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
            'memberships__officers__office__kind': [
                'exact',
            ],
        }


class SessionFilter(filters.FilterSet):
    class Meta:
        model = Session
        fields = {
            'status': [
                'exact',
            ],
            'convention': [
                'exact',
            ],
            'nomen': [
                'icontains',
            ],
            'convention__assignments__person__user': [
                'exact',
            ],
        }


class SubmissionFilter(filters.FilterSet):
    class Meta:
        model = Submission
        fields = {
            'status': [
                'exact',
            ],
        }


class VenueFilter(filters.FilterSet):
    class Meta:
        model = Venue
        fields = {
            'nomen': [
                'icontains',
            ],
        }
