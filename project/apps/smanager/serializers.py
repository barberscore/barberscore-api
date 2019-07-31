
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
    # included_serializers = {
    #     'person': 'api.serializers.PersonSerializer',
    #     'convention': 'api.serializers.ConventionSerializer',
    # }

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
    # class JSONAPIMeta:
    #     included_resources = [
    #         'convention',
    #         'person',
    #     ]


class ContestSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    included_serializers = {
    }

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

    class JSONAPIMeta:
        included_resources = [
        ]


class EntrySerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    statelogs = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )
    included_serializers = {
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

    class JSONAPIMeta:
        included_resources = [
            # 'appearances',
        ]

    def validate(self, data):
        """Check that the start is before the stop."""
        # if data['is_private']:
        #     raise serializers.ValidationError("Can not be private and compete for an award.")
        return data


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
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Repertory.objects.all(),
        #         fields=('group', 'chart'),
        #         message='This chart already exists in your repertory.',
        #     )
        # ]


class SessionSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    included_serializers = {
        # 'contests': 'apps.smanager.serializers.ContestSerializer',
        # 'entries': 'apps.smanager.serializers.EntrySerializer',
    }

    class Meta:
        model = Session
        fields = [
            'id',
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

            'permissions',
        ]
        read_only_fields = [
            'image_id',
        ]

    class JSONAPIMeta:
        included_resources = [
            # 'contests',
            # 'entries',
        ]
