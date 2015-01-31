from rest_framework import serializers

from .models import (
    Performance,
    Contest,
    Contestant,
)


class HyperlinkedFileField(serializers.FileField):
    """
    Overrides the default file field to render the full URL path rather than
    the instance name.  Enables a direct link to the image source.
    """
    def to_native(self, value):
        try:
            request = self.context.get('request', None)
            return request.build_absolute_uri(value.url)
        except:
            return None


class ContestantSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes the Contestant model instance.
    """
    performances = serializers.HyperlinkedRelatedField(
        view_name='performance-detail',
        many=True,
        read_only=True,
    )

    picture = HyperlinkedFileField()

    class Meta:
        model = Contestant


class PerformanceSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes the Performance model instance.
    """
    class Meta:
        model = Performance


class ContestSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes the Contest model instance, and nests performance instances.
    """
    performances = serializers.HyperlinkedRelatedField(
        view_name='performance-detail',
        many=True,
        read_only=True,
    )

    class Meta:
        model = Contest
