# Third-Party
from django_filters import rest_framework as filters

# Local
from .models import (
    Award,
    Catalog,
    Contestant,
    Convention,
    Group,
    Judge,
    Organization,
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
            'drcj__user': [
                'exact',
            ],
        }


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
            'roles__person__user': [
                'exact',
            ],
        }


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
            'person__user': [
                'exact',
            ],
        }


class OrganizationFilter(filters.FilterSet):
    class Meta:
        model = Organization
        fields = {
            'nomen': [
                'icontains',
            ],
            'representative__user': [
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
            'group': [
                'exact',
            ],
            'group__roles__person__user': [
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
            'judges__category': [
                'exact',
            ],
            'judges__status': [
                'exact',
            ],
            'judges__kind': [
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
            'performers__group__roles__person__user': [
                'exact',
            ],
            'assignments__person__user': [
                'exact',
            ],
            'convention__drcj__user': [
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
