
# Third-Party
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
        # 'officers': 'apps.bhs.serializers.OfficerSerializer',
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
            'owners',
            # 'members',
            # 'officers',
            'repertories',
            'permissions',
        ]

    class JSONAPIMeta:
        included_resources = [
            'repertories',
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
    image_id = serializers.SerializerMethodField()

    def get_image_id(self, obj):
        if obj.image:
            return obj.image.name
        return 'missing_image'

    class Meta:
        model = Person
        fields = [
            'id',
            'url',
            'status',
            'prefix',
            'first_name',
            'middle_name',
            'last_name',
            'nick_name',
            'suffix',
            'birth_date',
            'spouse',
            'location',
            'part',
            'mon',
            'gender',
            'district',
            'is_deceased',
            'is_honorary',
            'is_suspended',
            'is_expelled',
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
            'notes',
            'bhs_id',
            'mc_pk',

            'nomen',
            'full_name',
            'common_name',
            'sort_name',
            'initials',
            # 'current_through',
            # 'current_status',
            # 'current_district',

            'user',
            'permissions',
        ]
        read_only_fields = [
            'nomen',
            'full_name',
            'common_name',
            'sort_name',
            'initials',
            # 'current_through',
            # 'current_status',
            # 'current_district',
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
