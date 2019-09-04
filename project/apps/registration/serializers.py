
# Third-Party
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework_json_api import serializers

# Local

from .models import Assignment
from .models import Contest
from .models import Entry
from .models import Repertory
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
            'image_id',
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
        'repertories': 'apps.registration.serializers.RepertorySerializer',
    }

    class Meta:
        model = Entry
        fields = [
            'id',
            'status',
            'is_evaluation',
            'is_private',
            'is_mt',
            'is_senior',
            'is_youth',
            'draw',
            'seed',
            'prelim',
            'base',
            'participants',
            'pos',
            'representing',
            'chapters',
            'description',
            'notes',
            'image_id',

            'group_id',
            'name',
            'kind',
            'gender',
            # 'district',
            'division',
            'bhs_id',
            'code',

            'owners',
            'contests',
            'repertories',
            'session',

            'statelogs',
            'permissions',
        ]
        read_only_fields = [
            'image_id',
        ]



class RepertorySerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Repertory
        fields = [
            'id',
            'chart_id',
            'title',
            'arrangers',

            'entry',
            'permissions',
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
