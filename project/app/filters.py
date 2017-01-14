# Third-Party
from django_filters import rest_framework as filters
from django_filters import STRICTNESS

# Local
from .models import (
    Catalog,
    Contestant,
    Convention,
    Group,
    Judge,
    Performer,
    Person,
    Session,
    Submission,
    Venue,
)


class CatalogFilter(filters.FilterSet):
    class Meta:
        model = Catalog
        fields = {
            'title': [
                'icontains',
            ],
        }
        strict = STRICTNESS.RAISE_VALIDATION_ERROR


class ContestantFilter(filters.FilterSet):
    class Meta:
        model = Contestant
        fields = {
            'nomen': [
                'icontains',
            ],
        }
        strict = STRICTNESS.RAISE_VALIDATION_ERROR


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
        }
        strict = STRICTNESS.RAISE_VALIDATION_ERROR


class GroupFilter(filters.FilterSet):
    class Meta:
        model = Group
        fields = {
            'nomen': [
                'icontains',
            ],
            'kind': [
                'exact',
            ],
            'status': [
                'exact',
            ],
        }
        strict = STRICTNESS.RAISE_VALIDATION_ERROR


class JudgeFilter(filters.FilterSet):
    class Meta:
        model = Judge
        fields = {
            'nomen': [
                'icontains',
            ],
            'category': [
                'exact',
            ],
        }
        strict = STRICTNESS.RAISE_VALIDATION_ERROR


class PerformerFilter(filters.FilterSet):
    class Meta:
        model = Performer
        fields = {
            'nomen': [
                'icontains',
            ],
            'group': [
                'exact',
            ],
        }
        strict = STRICTNESS.RAISE_VALIDATION_ERROR


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
        }
        strict = STRICTNESS.RAISE_VALIDATION_ERROR


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
        }
        strict = STRICTNESS.RAISE_VALIDATION_ERROR


class SubmissionFilter(filters.FilterSet):
    class Meta:
        model = Submission
        fields = {
            'status': [
                'exact',
            ],
        }
        strict = STRICTNESS.RAISE_VALIDATION_ERROR


class VenueFilter(filters.FilterSet):
    class Meta:
        model = Venue
        fields = {
            'nomen': [
                'icontains',
            ],
        }
        strict = STRICTNESS.RAISE_VALIDATION_ERROR
