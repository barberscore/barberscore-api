
# Third-Party
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_json_api import serializers

# Local
from .fields import TimezoneField

from .models import Appearance
from .models import Assignment
from .models import Award
from .models import Contest
from .models import Contender
from .models import Contestant
from .models import Convention
from .models import Entry
from .models import Outcome
from .models import Panelist
from .models import Round
from .models import Score
from .models import Session
from .models import Song
from .models import User


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


class AppearanceSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    included_serializers = {
        'songs': 'api.serializers.SongSerializer',
        # 'songs__scores': 'api.serializers.ScoreSerializer',
    }

    class Meta:
        model = Appearance
        fields = (
            'id',
            'url',
            'status',
            'num',
            'draw',
            'actual_start',
            'actual_finish',
            'is_single',
            'is_private',
            'participants',
            'representing',
            'pos',
            'stats',
            'run_total',
            'variance_report',
            'round',
            'group',
            'songs',
            # 'songs__scores',
            # 'contenders',
            'permissions',
        )
        read_only_fields = [
            'run_total',
        ]


    class JSONAPIMeta:
        included_resources = [
            'songs',
            # 'songs__scores',
        ]


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


class ContestSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    included_serializers = {
        'contestants': 'api.serializers.ContestantSerializer',
    }

    class Meta:
        model = Contest
        fields = (
            'id',
            'url',
            'status',
            'result',
            'group',
            'session',
            'award',
            'contestants',
            'permissions',
        )

    class JSONAPIMeta:
        included_resources = [
            # 'contestants',
        ]


class ContestantSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Contestant
        fields = (
            'id',
            'url',
            'status',
            'entry',
            'contest',
            'permissions',
        )


class ContenderSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Contender
        fields = (
            'id',
            'url',
            'status',
            'appearance',
            'outcome',
            'permissions',
        )


class ConventionSerializer(serializers.ModelSerializer):
    timezone = TimezoneField(allow_null=True)
    permissions = DRYPermissionsField()
    included_serializers = {
        'sessions': 'api.serializers.SessionSerializer',
        'assignments': 'api.serializers.AssignmentSerializer',
        # 'person': 'api.serializers.PersonSerializer',
    }

    class Meta:
        model = Convention
        fields = (
            'id',
            'url',
            'name',
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
            'sessions',
            'assignments',
            # 'assignments.person',
        ]


    def validate(self, data):
        return data


class EntrySerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    # logs = StateLogSerializer(many=True)
    statelogs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    included_serializers = {
        'contestants': 'api.serializers.ContestantSerializer',
        'statelogs': 'api.serializers.StateLogSerializer',
        'group': 'apps.bhs.serializers.GroupSerializer',
    }

    class Meta:
        model = Entry
        fields = (
            'id',
            'url',
            'status',
            'is_evaluation',
            'is_private',
            'is_mt',
            'draw',
            'seed',
            'prelim',
            'participants',
            'pos',
            'representing',
            'description',
            'notes',
            'session',
            'group',
            'contestants',
            'permissions',
            'statelogs',
        )

    class JSONAPIMeta:
        included_resources = [
            # 'appearances',
            'contestants',
        ]

    def validate(self, data):
        """Check that the start is before the stop."""
        # if data['is_private'] and data['contestants']:
        #     raise serializers.ValidationError("Can not be private and compete for an award.")
        return data


class OutcomeSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    # included_serializers = {
    #     'contenders': 'api.serializers.ContenderSerializer',
    # }

    class Meta:
        model = Outcome
        fields = (
            'id',
            'url',
            'status',
            'round',
            'award',
            'num',
            'name',
            'contenders',
            'legacy_num',
            'legacy_name',
            'permissions',
        )


class PanelistSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    # included_serializers = {
    #     'scores': 'api.serializers.ScoreSerializer',
    # }

    class Meta:
        model = Panelist
        fields = (
            'id',
            'url',
            'status',
            'num',
            'kind',
            'category',
            'round',
            'person',
            'scores',
            'permissions',
        )

    # class JSONAPIMeta:
    #     included_resources = [
    #         'scores',
    #     ]


class RoundSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    included_serializers = {
        'appearances': 'api.serializers.AppearanceSerializer',
        'members': 'apps.bhs.serializers.MemberSerializer',
        'outcomes': 'api.serializers.OutcomeSerializer',
        'panelists': 'api.serializers.PanelistSerializer',
    }

    class Meta:
        model = Round
        fields = (
            'id',
            'url',
            'status',
            'kind',
            'num',
            'spots',
            'date',
            'footnotes',
            'oss',
            'sa',
            'session',
            'appearances',
            'panelists',
            'grids',
            'outcomes',
            'permissions',
        )

    class JSONAPIMeta:
        included_resources = [
            'appearances',
            'panelists',
            # 'members',
            # 'grids',
            # 'outcomes',
        ]


class ScoreSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Score
        fields = [
            'id',
            'url',
            'status',
            'points',
            'song',
            'panelist',
            'permissions',
        ]


class SessionSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    included_serializers = {
        'contests': 'api.serializers.ContestSerializer',
        'entries': 'api.serializers.EntrySerializer',
        'rounds': 'api.serializers.RoundSerializer',
    }

    class Meta:
        model = Session
        fields = (
            'id',
            'url',
            'status',
            'kind',
            'is_invitational',
            'footnotes',
            'description',
            'notes',
            'legacy_report',
            'drcj_report',
            'num_rounds',
            'convention',
            'contests',
            'entries',
            'rounds',
            'permissions',
        )

    class JSONAPIMeta:
        included_resources = [
            # 'contests',
            'entries',
            # 'rounds',
        ]


class SongSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    included_serializers = {
        'scores': 'api.serializers.ScoreSerializer',
    }

    class Meta:
        model = Song
        fields = (
            'id',
            'url',
            'status',
            'legacy_chart',
            'num',
            'penalties',
            'appearance',
            'chart',
            'scores',
            'permissions',
        )

    class JSONAPIMeta:
        included_resources = [
            'scores',
        ]


class UserSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = User
        fields = [
            'id',
            'url',
            'username',
            'is_active',
            'is_staff',
            'person',
            'is_convention_manager',
            'is_session_manager',
            'is_round_manager',
            'is_scoring_manager',
            'is_group_manager',
            'is_person_manager',
            'is_award_manager',
            'is_officer_manager',
            'is_chart_manager',
            'is_assignment_manager',
            'permissions',
        ]
        read_only_fields = [
            'is_convention_manager',
            'is_session_manager',
            'is_round_manager',
            'is_scoring_manager',
            'is_group_manager',
            'is_person_manager',
            'is_award_manager',
            'is_officer_manager',
            'is_chart_manager',
            'is_assignment_manager',
        ]
