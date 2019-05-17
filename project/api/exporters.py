from rest_framework import serializers

from .models import Appearance
from .models import Contest
from .models import Contestant
from .models import Entry
from .models import Outcome
from .models import Panelist
from .models import Round
from .models import Score
from .models import Session
from .models import Song
from .models import User


class AwardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Award
        fields = (
            'id',
            'name',
        )


class OutcomeSerializer(serializers.ModelSerializer):
    # award = serializers.StringRelatedField(read_only=True, many=False)
    award = AwardSerializer(read_only=True, many=False)

    class Meta:
        model = Outcome
        fields = (
            'id',
            'num',
            'name',
            'award',
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


class SessionSerializer(serializers.ModelSerializer):

    rounds = RoundSerializer(read_only=True, many=True)

    class Meta:
        model = Session
        fields = (
            'id',
            'get_kind_display',
            'rounds',
        )


class ConventionSerializer(serializers.ModelSerializer):

    sessions = SessionSerializer(read_only=True, many=True)

    class Meta:
        model = Convention
        fields = (
            'id',
            'name',
            'get_season_display',
            'year',
            'open_date',
            'close_date',
            'start_date',
            'end_date',
            'location',
            'sessions',
        )
