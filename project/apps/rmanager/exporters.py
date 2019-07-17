from rest_framework import serializers
from rest_framework.fields import UUIDField
from .models import Round
from .models import Contender
from .models import Outcome

from .models import Panelist
from .models import Appearance
from .models import Score
from .models import Song

class PanelistCategoryField(serializers.Field):
    def to_representation(self, value):
        return value.get_category_display()

class ScoreSerializer(serializers.ModelSerializer):
    panelist = PanelistCategoryField()

    class Meta:
        model = Score
        fields = (
            'id',
            'points',
            'panelist',
        )


class ContenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contender
        fields = (
            'id',
        )

class SongSerializer(serializers.ModelSerializer):
    scores = ScoreSerializer(read_only=True, many=True)
    # chart = serializers.PrimaryKeyRelatedField(
    #     read_only=True,
    #     pk_field=UUIDField(format='hex_verbose'),
    #     allow_null=True,
    # )

    class Meta:
        model = Song
        fields = (
            'id',
            'num',
            'legacy_chart',
            'asterisks',
            'dixons',
            'penalties',
            'stats',
            # 'chart',
            'scores',
        )



class PanelistSerializer(serializers.ModelSerializer):
    scores = ScoreSerializer(read_only=True, many=True)
    person = serializers.PrimaryKeyRelatedField(
        read_only=True,
        pk_field=UUIDField(format='hex_verbose'),
        allow_null=True,
    )

    class Meta:
        model = Panelist
        fields = (
            'id',
            'num',
            'get_kind_display',
            'get_category_display',
            'psa_report',
            'legacy_person',
            'representing',
            'person_id',
            'scores',
        )


class OutcomeSerializer(serializers.ModelSerializer):
    contenders = ContenderSerializer(read_only=True, many=True)
    award = serializers.PrimaryKeyRelatedField(
        read_only=True,
        pk_field=UUIDField(format='hex_verbose'),
        allow_null=True,
    )

    class Meta:
        model = Outcome
        fields = (
            'id',
            'num',
            'name',
            'award',
            'contenders',
        )


class AppearanceSerializer(serializers.ModelSerializer):
    contenders = ContenderSerializer(read_only=True, many=True)
    songs = SongSerializer(read_only=True, many=True)
    group = serializers.PrimaryKeyRelatedField(
        read_only=True,
        pk_field=UUIDField(format='hex_verbose'),
        allow_null=True,
    )

    entry = serializers.PrimaryKeyRelatedField(
        read_only=True,
        pk_field=UUIDField(format='hex_verbose'),
        allow_null=True,
    )


    class Meta:
        model = Appearance
        fields = (
            'id',
            'num',
            'draw',
            'is_private',
            'is_single',
            'participants',
            'representing',
            'onstage',
            'actual_start',
            'actual_finish',
            'legacy_group',
            'pos',
            'stats',
            'base',
            'variance_report',
            'group',
            'entry',
            'contenders',
            'songs',
        )


class RoundSerializer(serializers.ModelSerializer):

    appearances = AppearanceSerializer(read_only=True, many=True)
    panelists = PanelistSerializer(read_only=True, many=True)
    outcomes = OutcomeSerializer(read_only=True, many=True)
    session = serializers.PrimaryKeyRelatedField(
        read_only=True,
        pk_field=UUIDField(format='hex_verbose'),
        allow_null=True,
    )

    class Meta:
        model = Round
        fields = (
            'id',
            'get_kind_display',
            'num',
            'date',
            'spots',
            'footnotes',
            'appearances',
            'panelists',
            'outcomes',
            'session',
        )
