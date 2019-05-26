
# Third-Party
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework_json_api import serializers

# Local
from .fields import TimezoneField

from .models import Assignment
from .models import Award
from .models import Convention


class StateLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = StateLog
        fields = (
            'timestamp',
            'object_id',
            'transition',
            'description',
            'by',
        )


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
            'url',
            'status',
            'kind',
            'category',
            'convention',
            'person',
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
        fields = (
            'id',
            'url',
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
            'age',
            'size',
            'size_range',
            'scope',
            'scope_range',
            'tree_sort',
            'group',
            'parent',
            'children',
            'contests',
            'permissions',
        )


class ConventionSerializer(serializers.ModelSerializer):
    timezone = TimezoneField(allow_null=True)
    permissions = DRYPermissionsField()
    included_serializers = {
        # 'sessions': 'api.serializers.SessionSerializer',
        # 'assignments': 'apps.cmanager.serializers.AssignmentSerializer',
        # 'person': 'api.serializers.PersonSerializer',
    }

    class Meta:
        model = Convention
        fields = (
            'id',
            'url',
            'name',
            'district',
            'status',
            'season',
            'panel',
            'year',
            'open_date',
            'close_date',
            'start_date',
            'end_date',
            'location',
            'timezone',
            'image',
            'description',
            'venue',
            'group',
            'assignments',
            'sessions',
            'permissions',
        )

    class JSONAPIMeta:
        included_resources = [
            # 'sessions',
            # 'assignments',
            # 'assignments.person',
        ]


    def validate(self, data):
        return data

