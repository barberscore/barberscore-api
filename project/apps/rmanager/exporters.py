from rest_framework import serializers

from .models import Appearance
from .models import Outcome
from .models import Panelist
from .models import Round
from .models import Score
from .models import Song


class OutcomeSerializer(serializers.ModelSerializer):
    # award = serializers.StringRelatedField(read_only=True, many=False)
    # award = AwardSerializer(read_only=True, many=False)

    class Meta:
        model = Outcome
        fields = (
            'id',
            'num',
            'name',
            # 'award',
        )


class AppearanceSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True, many=False)
    songs = SongSerializer(read_only=True, many=True)

    class Meta:
        model = Appearance
        fields = (
            'id',
            'num',
            'group',
            'actual_start',
            'actual_finish',
            'pos',
            'stats',
            'songs',
        )


class RoundSerializer(serializers.ModelSerializer):

    appearances = AppearanceSerializer(read_only=True, many=True)
    panelists = PanelistSerializer(read_only=True, many=True)
    outcomes = OutcomeSerializer(read_only=True, many=True)

    class Meta:
        model = Round
        fields = (
            'id',
            'get_kind_display',
            'num',
            'date',
            'footnotes',
            'appearances',
            'panelists',
            'outcomes',
        )
