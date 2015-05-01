from rest_framework import serializers

from .models import (
    Singer,
    Chorus,
    Quartet,
    Contest,
    Convention,
    Performance,
    GroupFinish,
)


class SingerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Singer
        lookup_field = 'slug'
        fields = (
            'url',
            'id',
            'name',
            'slug',
        )


class ChorusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chorus
        lookup_field = 'slug'
        fields = (
            'url',
            'id',
            'name',
            'slug',
        )


class QuartetSerializer(serializers.ModelSerializer):
    singers = SingerSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Quartet
        lookup_field = 'slug'
        fields = (
            'url',
            'id',
            'name',
            'slug',
            'singers',
        )


class GroupFinishSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupFinish
        fields = (
            'seed',
            'prelim',
            'place',
            'score',
        )


class PerformanceSerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField(
        read_only=True,
    )

    class Meta:
        model = Performance
        fields = (
            'id',
            'group',
            'round',
            'queue',
            'session',
            'stagetime',
            'song1',
            'song2',
        )


class ContestSerializer(serializers.ModelSerializer):
    performances = PerformanceSerializer(
        many=True,
        read_only=True,
    )
    groupfinishes = GroupFinishSerializer(
        many=True,
        read_only=True,
    )

    kind = serializers.CharField(source='get_kind_display')

    class Meta:
        model = Contest
        lookup_field = 'slug'

        fields = (
            'url',
            'id',
            'slug',
            'panel',
            'kind',
            'year',
            'performances',
            'groupfinishes',
        )


class ConventionSerializer(serializers.ModelSerializer):
    contests = ContestSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Convention
        lookup_field = 'slug'
        fields = (
            'url',
            'id',
            'slug',
            'contests',
        )
