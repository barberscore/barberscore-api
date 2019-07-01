from rest_framework import serializers

from .models import Session

class SessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Session
        fields = (
            'id',
            'get_kind_display',
            'rounds',
        )
