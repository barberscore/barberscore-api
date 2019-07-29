
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
            'status',
            'kind',
            'category',

            'person_id',
            'name',
            'first_name',
            'last_name',
            'representing',
            'email',
            'cell_phone',
            'airports',

            'bhs_id',
            'image_id',
            # 'user',
            'sessions',
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
            'status',

            'award_id',
            'award_age',
            'award_description',
            'award_district',
            'award_division',
            'award_gender',
            'award_is_novice',
            'award_kind',
            'award_level',
            'award_name',
            'award_scope',
            'award_scope_range',
            'award_season',
            'award_size',
            'award_size_range',
            'award_tree_sort',

            'session',
            'entry',
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
            'group_status',
            'group_name',
            'group_nomen',
            'group_kind',
            'group_gender',
            'group_division',
            'group_bhs_id',
            'group_code',
            # 'group_image_id',
            'group_description',
            'group_participants',
            'group_tree_sort',
            'group_international',
            'group_district',
            'group_chapter',
            'group_is_senior',
            'group_is_youth',
            'group_is_divided',
            # 'group_charts',

            'owners',
            'contests',
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
            'status',
            'title',
            'arrangers',

            'chart_id',
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
            'representing',
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
            'imageId',
            'divisions',

            'owners',

            'contests',
            'entries',

            'permissions',
        ]

    class JSONAPIMeta:
        included_resources = [
            # 'contests',
            # 'entries',
        ]
