from rest_framework import serializers

from .models import Session

class SessionSerializer(serializers.ModelSerializer):

    rounds = RoundSerializer(read_only=True, many=True)

    class Meta:
        model = Session
        fields = (
            'id',
            'get_kind_display',
            'rounds',
        )
