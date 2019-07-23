
# Third-Party
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_json_api import serializers

# Local
from .fields import TimezoneField

from .models import Contest
from .models import Contestant
from .models import Entry
from .models import Session



from .models import Assignment
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


class ConventionSerializer(serializers.ModelSerializer):
    timezone = TimezoneField(allow_null=True)
    permissions = DRYPermissionsField()
    included_serializers = {
        'assignments': 'apps.smanager.serializers.AssignmentSerializer',
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

class ContestSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    included_serializers = {
        'contestants': 'apps.smanager.serializers.ContestantSerializer',
    }

    class Meta:
        model = Contest
        fields = [
            'id',
            'status',
            'session',

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

            'contestants',
            'permissions',
        ]

    class JSONAPIMeta:
        included_resources = [
            # 'contestants',
        ]


class ContestantSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Contestant
        fields = [
            'id',
            'status',
            'entry',
            'contest',
            'permissions',
        ]


class EntrySerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    statelogs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    included_serializers = {
        'contestants': 'apps.smanager.serializers.ContestantSerializer',
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
            'description',
            'notes',

            'owners',
            'session',

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
            'group_charts',

            'contestants',
            'permissions',
            'statelogs',
        ]
        read_only_fields = [
            # 'group_image_id',
        ]

    class JSONAPIMeta:
        included_resources = [
            # 'appearances',
            # 'contestants',
        ]

    def validate(self, data):
        """Check that the start is before the stop."""
        # if data['is_private'] and data['contestants']:
        #     raise serializers.ValidationError("Can not be private and compete for an award.")
        return data


class SessionSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    included_serializers = {
        'contests': 'apps.smanager.serializers.ContestSerializer',
        'entries': 'apps.smanager.serializers.EntrySerializer',
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

            'owners',
            'convention',
            'target',

            'contests',
            'entries',
            'rounds',

            'permissions',
        ]

    class JSONAPIMeta:
        included_resources = [
            # 'contests',
            # 'entries',
        ]
