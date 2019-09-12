
# Third-Party
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework_json_api import serializers

# Local

from .models import Assignment
from .models import Contest
from .models import Entry
from .models import Session


class AssignmentSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Assignment
        fields = (
            'id',
            'kind',
            'category',

            'person_id',
            'name',
            'first_name',
            'last_name',
            'district',
            'email',
            'cell_phone',
            'airports',
            'bhs_id',

            'image_id',
            'session',
            'permissions',
        )


        read_only_fields = [
        ]


class ContestSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Contest
        fields = [
            'id',

            'award_id',
            'name',
            'kind',
            'gender',
            'level',
            'season',
            'description',
            'district',
            'division',
            'age',
            'is_novice',
            'is_single',
            'size',
            'size_range',
            'scope',
            'scope_range',
            'tree_sort',

            'session',
            'entries',
            'permissions',
        ]


class EntrySerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    statelogs = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )

    included_serializers = {
        'contests': 'apps.registration.serializers.ContestSerializer',
    }

    class Meta:
        model = Entry
        fields = [
            'id',
            'status',
            'is_evaluation',
            'is_private',
            'notes',

            'is_mt',
            'draw',
            'prelim',
            'base',

            'participants',
            'chapters',
            'pos',
            'area',

            'group_id',
            'name',
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

            'owners',
            'contests',
            'session',

            'statelogs',
            'permissions',

        ]
        read_only_fields = [
            'nomen',
            'image_id',
        ]


class SessionSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    statelogs = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )
    included_serializers = {
        'contests': 'apps.registration.serializers.ContestSerializer',
        'entries': 'apps.registration.serializers.EntrySerializer',
        'assignments': 'apps.registration.serializers.AssignmentSerializer',
    }

    class Meta:
        model = Session
        fields = [
            'id',
            'url',
            'status',
            'kind',
            'num_rounds',
            'is_invitational',
            'description',
            'notes',
            'footnotes',
            'legacy_report',
            'drcj_report',

            'convention_id',
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
            # 'timezone',
            'divisions',

            'image_id',

            'owners',
            'contests',
            'entries',
            'assignments',

            'statelogs',
            'permissions',
        ]
        read_only_fields = [
            'image_id',
        ]
