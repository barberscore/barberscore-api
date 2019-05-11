
# Third-Party
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_json_api import serializers

# Local
from .fields import TimezoneField

from .models import Group
from .models import Member
from .models import Officer
from .models import Person


class GroupSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    included_serializers = {
        # 'repertories': 'api.serializers.RepertorySerializer',
        'members': 'api.serializers.MemberSerializer',
        'officers': 'api.serializers.OfficerSerializer',
        # 'entries': 'api.serializers.EntrySerializer',
    }

    class Meta:
        model = Group
        fields = [
            'id',
            'url',
            'name',
            'status',
            'kind',
            'gender',
            'is_senior',
            'is_youth',
            'division',
            'code',
            'start_date',
            'end_date',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'image',
            'description',
            'participants',
            'bhs_id',
            'international',
            'district',
            'chapter',
            'tree_sort',
            'parent',
            'children',
            # 'awards',
            # 'conventions',
            # 'entries',
            'members',
            'officers',
            # 'repertories',
            'permissions',
        ]

    class JSONAPIMeta:
        included_resources = [
            # 'repertories',
            # 'members',
            # 'officers',
            # 'entries',
        ]

    # def to_representation(self, instance):
    #     if instance.kind <= 30:
    #         self.fields.pop('members')
    #     return super().to_representation(instance)


class MemberSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Member
        fields = [
            'id',
            'url',
            'status',
            'part',
            'start_date',
            'end_date',
            'group',
            'person',
            'permissions',
        ]


class OfficerSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Officer
        fields = [
            'id',
            'url',
            'status',
            'start_date',
            'end_date',
            'office',
            'person',
            'group',
            'permissions',
        ]

        validators = [
            UniqueTogetherValidator(
                queryset=Officer.objects.all(),
                fields=('person', 'office'),
                message='This person already holds this office.',
            )
        ]


class PersonSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    included_serializers = {
        # 'assignments': 'api.serializers.AssignmentSerializer',
        'members': 'api.serializers.MemberSerializer',
        'officers': 'api.serializers.OfficerSerializer',
        # 'panelists': 'api.serializers.PanelistSerializer',
    }

    class Meta:
        model = Person
        fields = (
            'id',
            'url',
            'first_name',
            'middle_name',
            'last_name',
            'nick_name',
            'status',
            'birth_date',
            'spouse',
            'location',
            'part',
            'website',
            'email',
            'address',
            'home_phone',
            'work_phone',
            'cell_phone',
            'airports',
            'image',
            'description',
            'gender',
            'bhs_id',
            'current_through',
            'current_status',
            'current_district',
            'full_name',
            'common_name',
            'sort_name',
            # 'assignments',
            'members',
            'officers',
            # 'panelists',
            # 'user',
            'permissions',
        )
        read_only_fields = [
            'common_name',
            'full_name',
            'sort_name',
        ]

    class JSONAPIMeta:
        included_resources = [
            # 'assignments',
            # 'members',
            # 'officers',
            # 'panelists',
        ]
