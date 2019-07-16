from django_filters.rest_framework import FilterSet
# Third-Party

# Local
from .models import Group
from .models import Member
from .models import Officer
from .models import Person


class GroupFilterset(FilterSet):
    class Meta:
        model = Group
        fields = {
            'owners': [
                'exact',
            ],
            'status': [
                'exact',
                'gt',
            ],
            'kind': [
                'gt',
            ],
        }


class MemberFilterset(FilterSet):
    class Meta:
        model = Member
        fields = {
            'person__user': [
                'exact',
            ],
            'status': [
                'exact',
            ],
            'group__status': [
                'exact',
            ],
            'group__kind': [
                'gt',
            ],
            'group__parent__kind': [
                'gt',
            ],
        }


class OfficerFilterset(FilterSet):
    class Meta:
        model = Officer
        fields = {
            'person__user': [
                'exact',
            ],
            'group__status': [
                'exact',
            ],
            'status': [
                'exact',
            ],
        }


class PersonFilterset(FilterSet):
    class Meta:
        model = Person
        fields = {
            'user': [
                'exact',
            ],
            'user__username': [
                'exact',
            ],
            'status': [
                'exact',
            ],
        }
