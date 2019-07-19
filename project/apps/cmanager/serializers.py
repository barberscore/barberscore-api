
# Third-Party
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework_json_api import serializers
from rest_framework.serializers import SerializerMethodField
# Local
from .fields import TimezoneField

from .models import Assignment
from .models import Award
from .models import Convention



class AssignmentSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    # included_serializers = {
    #     'person': 'api.serializers.PersonSerializer',
    #     'convention': 'api.serializers.ConventionSerializer',
    # }

    class Meta:
        model = Assignment
        fields = (
            'id',
            'status',
            'kind',
            'category',
            'convention',
            'person_id',
            'user',
            'permissions',
        )

    # class JSONAPIMeta:
    #     included_resources = [
    #         'convention',
    #         'person',
    #     ]


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


class ConventionSerializer(serializers.ModelSerializer):
    timezone = TimezoneField(allow_null=True)
    permissions = DRYPermissionsField()
    included_serializers = {
        'assignments': 'apps.cmanager.serializers.AssignmentSerializer',
    }

    class Meta:
        model = Convention
        fields = [
            'id',
            '__str__',
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
            'image',
            'description',
            'divisions',
            'kinds',

            'group_id',

            'image_id',

            'assignments',
            'sessions',
            'permissions',
        ]
        read_only_fields = [
            '__str__'
            'image_id',
        ]

    class JSONAPIMeta:
        included_resources = [
            'assignments',
        ]


    def validate(self, data):
        return data

