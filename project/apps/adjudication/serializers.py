
# Third-Party
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_json_api import serializers

# Local
from .fields import TimezoneField

from .models import Appearance
from .models import Outcome
from .models import Panelist
from .models import Round
from .models import Score
from .models import Song


class AppearanceSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    included_serializers = {
        # 'songs': 'apps.adjudication.serializers.SongSerializer',
    }

    class Meta:
        model = Appearance
        fields = [
            'id',
            'status',
            'num',
            'draw',
            'is_private',
            'is_single',
            'participants',
            'area',
            'onstage',
            'actual_start',
            'actual_finish',
            'pos',
            'stats',
            'base',
            'variance_report',
            'csa_report',

            'group_id',
            'name',
            'kind',
            'gender',
            'district',
            'division',
            'bhs_id',
            'code',
            'charts',

            'owners',
            'round',
            'outcomes',

            'songs',
            'permissions',
        ]


    class JSONAPIMeta:
        included_resources = [
            # 'songs',
        ]


class OutcomeSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Outcome
        fields = [
            'id',
            'status',
            'num',
            'winner',

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
            'size',
            'size_range',
            'scope',
            'scope_range',
            'tree_sort',

            'round',
            'appearances',

            'permissions',
        ]


class PanelistSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    # included_serializers = {
    #     'scores': 'apps.adjudication.serializers.ScoreSerializer',
    # }

    class Meta:
        model = Panelist
        fields = [
            'id',
            'status',
            'num',
            'kind',
            'category',
            'psa_report',

            'round',
            'owners',

            'person_id',
            'name',
            'first_name',
            'last_name',
            'district',
            'email',
            'cell_phone',
            'airports',

            'scores',
            'permissions',
        ]

    # class JSONAPIMeta:
    #     included_resources = [
    #         'scores',
    #     ]


class RoundSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    included_serializers = {
        # 'appearances': 'apps.adjudication.serializers.AppearanceSerializer',
        # 'outcomes': 'apps.adjudication.serializers.OutcomeSerializer',
        # 'panelists': 'apps.adjudication.serializers.PanelistSerializer',
    }

    class Meta:
        model = Round
        fields = [
            'id',
            'status',
            'kind',
            'num',
            'spots',
            'date',
            'footnotes',
            'oss_report',
            'sa_report',
            'legacy_oss',

            'convention_id',
            'nomen',
            # 'timezone',
            'image_id',

            'session_id',
            'session_kind',

            'owners',
            'appearances',
            'panelists',
            'outcomes',
            'permissions',
        ]

        read_only_fields = [
            'nomen',
        ]
    class JSONAPIMeta:
        included_resources = [
            # 'appearances',
            # 'panelists',
            # 'outcomes',
        ]


class ScoreSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Score
        fields = [
            'id',
            'status',
            'points',

            'song',
            'panelist',

            'permissions',
        ]


class SongSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    included_serializers = {
        'scores': 'apps.adjudication.serializers.ScoreSerializer',
    }

    class Meta:
        model = Song
        fields = [
            'id',
            'status',
            'num',
            'asterisks',
            'dixons',
            'penalties',
            'stats',

            'chart_id',
            'title',
            'arrangers',

            'appearance',
            'scores',
            'permissions',
        ]

    class JSONAPIMeta:
        included_resources = [
            'scores',
        ]
