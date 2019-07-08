
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

    image_id = serializers.SerializerMethodField()

    def get_image_id(self, obj):
        if obj.image:
            return obj.image.name
        else:
            return 'missing_image'

    class Meta:
        model = Convention
        fields = (
            'id',
            'url',
            'name',
            '__str__',
            'district',
            'status',
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
            'image_id',
            'description',
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

