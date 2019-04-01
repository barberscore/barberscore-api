from rest_framework import serializers

from .models import Appearance
from .models import Assignment
from .models import Award
from .models import Chart
from .models import Contest
from .models import Contestant
from .models import Convention
from .models import Entry
from .models import Grid
from .models import Group
from .models import Member
from .models import Office
from .models import Officer
from .models import Outcome
from .models import Panelist
from .models import Person
from .models import Repertory
from .models import Round
from .models import Score
from .models import Session
from .models import Song
from .models import User
from .models import Venue

class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = (
            'id',
            'common_name',
            'bhs_id',
        )
        read_only_fields = [
            'common_name',
        ]

class PanelistSerializer(serializers.ModelSerializer):

    person = PersonSerializer(read_only=True, many=False)
    # person = serializers.StringRelatedField(read_only=True, many=False)
    class Meta:
        model = Panelist
        fields = (
            'id',
            'num',
            'get_kind_display',
            'get_category_display',
            'person',
        )

class ScoreSerializer(serializers.ModelSerializer):

    panelist = PanelistSerializer(read_only=True, many=False)

    class Meta:
        model = Score
        fields = [
            'id',
            'points',
            'panelist',
        ]

class ChartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chart
        fields = (
            'id',
            'title',
            'arrangers',
            'composers',
            'lyricists',
        )

class SongSerializer(serializers.ModelSerializer):

    scores = ScoreSerializer(read_only=True, many=True)
    chart = ChartSerializer(read_only=True, many=False)
    # chart = serializers.StringRelatedField(read_only=True, many=False)

    class Meta:
        model = Song
        fields = (
            'id',
            'num',
            'chart',
            'stats',
            'penalties',
            'scores',
        )


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

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'bhs_id',
            'get_kind_display',
            'get_gender_display',
            'is_senior',
            'is_youth',
            'code',
            'international',
            'district',
            'get_division_display',
            'chapter',
        ]

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
