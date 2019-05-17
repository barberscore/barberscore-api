from rest_framework import serializers

# from .models import Assignment
from .models import Award
from .models import Convention


class AwardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Award
        fields = (
            'id',
            'name',
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
