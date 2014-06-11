from rest_framework import serializers

from .models import (
    Performance,
    Contest,
    Contestant,
)


class HyperlinkedFileField(serializers.FileField):
    def to_native(self, value):
        request = self.context.get('request', None)
        return request.build_absolute_uri(value.url)


class ContestantSerializer(serializers.HyperlinkedModelSerializer):
    performances = serializers.HyperlinkedRelatedField(
        view_name='performance-detail',
        many=True,
        read_only=True,
    )

    picture = HyperlinkedFileField()

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
