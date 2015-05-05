from rest_framework import serializers

from .models import (
    Singer,
    Chorus,
    Quartet,
    Contest,
    Convention,
    Contestant,
    Performance,
)


class SingerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Singer
        # lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'name',
            'slug',
        )


class PerformanceSerializer(serializers.ModelSerializer):
    round = serializers.CharField(
        source='get_round_display',
    )

    class Meta:
        model = Performance
        fields = (
            'id',
            'url',
            'round',
            'queue',
            'session',
            'stagetime',
            'place',
            'song1',
            'mus1',
            'prs1',
            'sng1',
            'song2',
            'mus2',
            'prs2',
            'sng2',
            'men',
        )


class ContestantSerializer(serializers.ModelSerializer):
    performances = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )

    group = serializers.StringRelatedField(
        read_only=True,
    )

    class Meta:
        model = Contestant
        fields = (
            'id',
            'url',
            'group',
            'seed',
            'prelim',
            'place',
            'score',
            'performances',
        )


class ChorusSerializer(serializers.ModelSerializer):
    contestants = ContestantSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Chorus
        # lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'name',
            'slug',
            'contestants',
        )


class ContestSerializer(serializers.ModelSerializer):
    contestants = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )

    kind = serializers.CharField(
        source='get_kind_display',
    )

    class Meta:
        model = Contest
        fields = (
            'id',
            'url',
            'kind',
            'panel',
            'scoresheet_pdf',
            'contestants',
        )


class QuartetSerializer(serializers.ModelSerializer):
    contests = ContestSerializer(
        many=True,
        read_only=True,
        source='contestant.contests'
    )

    class Meta:
        model = Quartet
        # lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'name',
            'slug',
            'contests',
        )


class ConventionSerializer(serializers.ModelSerializer):
    contests = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Convention
        # lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'contests',
        )
