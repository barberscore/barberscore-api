
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
            'award',
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
    # statelogs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
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

            'contestants',
            'permissions',
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
