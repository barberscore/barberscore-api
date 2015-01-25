from rest_framework import serializers

from .models import (
    Singer,
    Chorus,
)


class SingerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Singer
        fields = (
            'id',
            'name',
        )


class ChorusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chorus
        fields = (
            'id',
            'name',
        )
