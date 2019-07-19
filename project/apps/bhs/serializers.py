
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

from .models import Award
from .models import Chart
from .models import Repertory


class AwardSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Award
        fields = [
            'id',
            'name',
            'status',
            'kind',
            'gender',
            'level',
            'season',
            'is_single',
            'threshold',
            'minimum',
            'advance',
            'spots',
            'description',
            'notes',
            'district',
            'division',

            'age',
            'is_novice',

            'size',
            'size_range',
            'scope',
            'scope_range',
            'tree_sort',
            'group_id',
            'permissions',
        ]


class GroupSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    included_serializers = {
        'repertories': 'apps.bhs.serializers.RepertorySerializer',
        # 'members': 'apps.bhs.serializers.MemberSerializer',
        # 'officers': 'apps.bhs.serializers.OfficerSerializer',
    }

    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'status',
            'kind',
            'gender',
            'division',
            'bhs_id',
            'code',
            'website',
            'email',
            'phone',
            'fax_phone',
            'start_date',
            'end_date',
            'location',
            'facebook',
            'twitter',
            'youtube',
            'pinterest',
            'flickr',
            'instagram',
            'soundcloud',
            'image',
            'description',
            'visitor_information',
            'participants',
            'notes',
            'mc_pk',

            'tree_sort',
            'international',
            'district',
            'chapter',
            'is_senior',
            'is_youth',
            'is_divided',

            'owners',
            'parent',
            # 'children',

            'repertories',
            'permissions',

            'nomen',
            'image_id',
        ]

        read_only_fields = [
            'nomen',
            'image_id',
        ]

    class JSONAPIMeta:
        included_resources = [
            'repertories',
            # 'members',
            # 'officers',
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

    class Meta:
        model = Person
        fields = [
            'id',
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
            'description',
            'notes',
            'bhs_id',
            'mc_pk',

            'nomen',
            'full_name',
            'common_name',
            'sort_name',
            'initials',
            'image_id',
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
            'image_id',
            # 'current_through',
            # 'current_status',
            # 'current_district',
        ]


class ChartSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    included_serializers = {
        'repertories': 'apps.bhs.serializers.RepertorySerializer',
    }

    class Meta:
        model = Chart
        fields = [
            'id',
            'status',
            'title',
            'arrangers',
            'composers',
            'lyricists',
            'holders',
            'description',
            'notes',
            'image',

            'nomen',
            'image_id',

            'repertories',
            'permissions',
        ]
        read_only_fields = [
            'nomen',
            'image_id',
        ]

    class JSONAPIMeta:
        included_resources = [
            'repertories',
        ]


class RepertorySerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Repertory
        fields = [
            'id',
            'status',
            'group',
            'chart',
            'permissions',
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=Repertory.objects.all(),
                fields=('group', 'chart'),
                message='This chart already exists in your repertory.',
            )
        ]
