
# Third-Party
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



class AppearanceSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    included_serializers = {
        'songs': 'apps.rmanager.serializers.SongSerializer',
    }

    class Meta:
        model = Appearance
        fields = [
            'id',
            'url',
            'status',
            'num',
            'draw',
            'is_private',
            'is_single',
            'participants',
            'representing',
            'onstage',
            'actual_start',
            'actual_finish',
            'pos',
            'stats',
            'base',
            'variance_report',
            'csa',

            'owners',
            'round',
            'group_id',

            'round__kind',
            # 'run_total',

            'songs',

            'permissions',
        ]
        read_only_fields = [
            'round__kind',
            'run_total',
        ]


    class JSONAPIMeta:
        included_resources = [
            # 'songs',
        ]


class ContenderSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Contender
        fields = [
            'id',
            'url',
            'status',
            'appearance',
            'outcome',
            'permissions',
        ]


class OutcomeSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    # included_serializers = {
    #     'contenders': 'apps.rmanager.serializers.ContenderSerializer',
    # }

    class Meta:
        model = Outcome
        fields = [
            'id',
            'url',
            'status',
            'num',
            'name',

            'round',
            'award',

            'contenders',
            'permissions',
        ]


class PanelistSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    # included_serializers = {
    #     'scores': 'apps.rmanager.serializers.ScoreSerializer',
    # }

    class Meta:
        model = Panelist
        fields = [
            'id',
            'url',
            'status',
            'num',
            'kind',
            'category',
            'psa',
            'representing',

            'row_class',

            'round',
            'user',

            'person_id',

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
        'appearances': 'apps.rmanager.serializers.AppearanceSerializer',
        'outcomes': 'apps.rmanager.serializers.OutcomeSerializer',
        'panelists': 'apps.rmanager.serializers.PanelistSerializer',
    }

    class Meta:
        model = Round
        fields = [
            'id',
            'url',
            'status',
            'kind',
            'num',
            'spots',
            'date',
            'footnotes',
            'oss',
            'legacy_oss',
            'sa',
            'is_reviewed',

            'owners',
            'session',

            'appearances',
            'panelists',
            'outcomes',
            'permissions',
        ]

    class JSONAPIMeta:
        included_resources = [
            'appearances',
            'panelists',
            'outcomes',
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
        'scores': 'apps.rmanager.serializers.ScoreSerializer',
    }

    class Meta:
        model = Song
        fields = [
            'id',
            'url',
            'status',
            'num',
            'asterisks',
            'dixons',
            'penalties',
            'stats',

            'appearance',
            'chart_id',

            'scores',
            'permissions',
        ]

    class JSONAPIMeta:
        included_resources = [
            'scores',
        ]
