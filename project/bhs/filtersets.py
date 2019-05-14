from django_filters.rest_framework import FilterSet
# Third-Party
from django_fsm_log.models import StateLog

# Local
from .models import Member
from .models import Officer


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

# class GroupFilter(FilterSet):
#     class Meta:
#         model = Group
#         fields = {
#             'kind': [
#                 'gt',
#             ],
#             'officers__person__user': [
#                 'exact',
#             ],
#             'officers__status': [
#                 'exact',
#             ],
#             'members__person__user': [
#                 'exact',
#             ],
#             'members__status': [
#                 'exact',
#             ],
#             'status': [
#                 'exact',
#             ],
#         }


