
# Third-Party
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_json_api import serializers

# Local
from .fields import TimezoneField

from .models import Appearance
from .models import Contender
from .models import Outcome
from .models import Panelist
from .models import Round
from .models import Score
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
            'onstage',
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
            'entry',
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
