from rest_framework import serializers

from .models import (
    Performance,
    Contest,
    Contestant,
)


class ContestantSerializer(serializers.HyperlinkedModelSerializer):
    performances = serializers.HyperlinkedRelatedField(
        view_name='performance-detail',
        many=True,
        read_only=True,
    )

    class Meta:
        model = Contestant


class PerformanceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Performance


class ContestSerializer(serializers.HyperlinkedModelSerializer):
    performances = serializers.HyperlinkedRelatedField(
        view_name='performance-detail',
        many=True,
        read_only=True,
    )

    class Meta:
        model = Contest
