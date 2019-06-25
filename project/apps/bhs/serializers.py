
# Third-Party
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_json_api import serializers
from rest_framework.serializers import SerializerMethodField

# Local
from .fields import TimezoneField

from .models import Group
from .models import Member
from .models import Officer
from .models import Person

from .models import Chart
from .models import Repertory


class GroupSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    included_serializers = {
        'repertories': 'apps.bhs.serializers.RepertorySerializer',
        # 'members': 'apps.bhs.serializers.MemberSerializer',
        'officers': 'apps.bhs.serializers.OfficerSerializer',
        # 'entries': 'api.serializers.EntrySerializer',
    }

    image_id = serializers.SerializerMethodField()

    def get_image_id(self, obj):
        if obj.image:
            return obj.image.name
        else:
            return 'missing_image'

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
            'image_id',
            'description',
            'participants',
            'bhs_id',
            'international',
            'district',
            'chapter',
            'tree_sort',
            'parent',
            'children',
            'awards',
            'conventions',
            'entries',
            # 'members',
            'officers',
            'repertories',
            'permissions',
        ]

    class JSONAPIMeta:
        included_resources = [
            'repertories',
            # 'members',
            'officers',
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
        'members': 'apps.bhs.serializers.MemberSerializer',
        'officers': 'apps.bhs.serializers.OfficerSerializer',
        # 'panelists': 'api.serializers.PanelistSerializer',
    }
    image_id = serializers.SerializerMethodField()

    def get_image_id(self, obj):
        if obj.image:
            return obj.image.name
        else:
            return 'missing_image'


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
            'image_id',
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
            'user',
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


class ChartSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    image_id = serializers.SerializerMethodField()

    def get_image_id(self, obj):
        if obj.image:
            return obj.image.name
        else:
            return 'missing_image'

    class Meta:
        model = Chart
        fields = (
            'id',
            'url',
            'status',
            'title',
            'arrangers',
            'composers',
            'lyricists',
            'description',
            'notes',
            'image',
            'image_id',
            'holders',
            'repertories',
            # 'songs',
            'permissions',
        )


class RepertorySerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Repertory
        fields = (
            'id',
            'url',
            'status',
            'group',
            'chart',
            'permissions',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Repertory.objects.all(),
                fields=('group', 'chart'),
                message='This chart already exists in your repertory.',
            )
        ]



