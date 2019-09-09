
# Third-Party
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework_json_api import serializers
from rest_framework_json_api.relations import ResourceRelatedField
from django.contrib.auth import get_user_model

# Local
from .fields import TimezoneField

from .models import Award
from .models import Chart
from .models import Convention
from .models import Group
from .models import Person

User = get_user_model()

class AwardSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Award
        fields = [
            'id',
            # 'nomen',
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
            'permissions',
        ]

        read_only_fields = [
            # 'nomen',
        ]


class ChartSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    included_serializers = {
    }

    class Meta:
        model = Chart
        fields = [
            'id',
            'nomen',
            'status',
            'title',
            'arrangers',
            'image_id',
            'groups',
            'permissions',
        ]
        read_only_fields = [
            'nomen',
            'image_id',
        ]


class ConventionSerializer(serializers.ModelSerializer):
    timezone = TimezoneField(allow_null=True)
    permissions = DRYPermissionsField()

    class Meta:
        model = Convention
        fields = [
            'id',
            'nomen',
            'status',
            'name',
            'district',
            'season',
            'panel',
            'year',
            'open_date',
            'close_date',
            'start_date',
            'end_date',
            'venue_name',
            'location',
            'timezone',
            'description',
            'divisions',
            'kinds',

            'image_id',
            'persons',
            'owners',
            'permissions',
        ]
        read_only_fields = [
            'nomen'
            'image_id',
        ]

    class JSONAPIMeta:
        included_resources = [
        ]


    def validate(self, data):
        return data


class GroupSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    included_serializers = {
        'charts': 'apps.bhs.serializers.ChartSerializer',
        # 'members': 'apps.bhs.serializers.MemberSerializer',
        # 'officers': 'apps.bhs.serializers.OfficerSerializer',
    }

    class Meta:
        model = Group
        fields = [
            'id',
            'nomen',
            'name',
            'status',
            'kind',
            'gender',
            'district',
            'division',
            'bhs_id',
            'code',
            'is_senior',
            'is_youth',
            'image_id',
            'description',

            'source_id',

            'owners',
            'charts',
            'permissions',

        ]

        read_only_fields = [
            'nomen',
            'image_id',
        ]


class PersonSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    # owners = ResourceRelatedField(
    #     queryset=User.objects,
    #     many=True,
    #     read_only=False,
    #     related_link_lookup_field='username',
    # )

    # owners = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Person
        fields = [
            'id',
            'status',
            'name',
            'first_name',
            'last_name',
            'part',
            'gender',
            'district',
            'email',
            'address',
            'home_phone',
            'work_phone',
            'cell_phone',
            'airports',
            'description',
            'notes',
            'bhs_id',
            'source_id',

            'nomen',
            'image_id',

            'owners',
            'permissions',
        ]
        read_only_fields = [
            'nomen',
            'image_id',
        ]
