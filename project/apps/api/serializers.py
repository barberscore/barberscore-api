from rest_framework import serializers

from .models import (
    Singer,
    Chorus,
    Quartet,
    Contest,
    District,
    Convention,
    Contestant,
    Performance,
)


class SingerSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(
        source='first_name',
    )

    lastName = serializers.CharField(
        source='last_name',
    )

    class Meta:
        model = Singer
        # lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'name',
            'slug',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            'notes',
            'firstName',
            'lastName',
        )


class DistrictSerializer(serializers.ModelSerializer):
    kind = serializers.CharField(
        source='get_kind_display',
    )

    longName = serializers.CharField(
        source='long_name',
    )

    class Meta:
        model = District
        # lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'name',
            'slug',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            'notes',
            'kind',
            'longName',
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
            'mus1_rata',
            'prs1_rata',
            'sng1_rata',
            'song1_raw',
            'song1_rata',
            'mus2_rata',
            'prs2_rata',
            'sng2_rata',
            'song2_raw',
            'song2_rata',
            'total_raw',
            'total_rata',
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

    chapterName = serializers.CharField(
        source='chapter_name',
    )

    chapterCode = serializers.CharField(
        source='chapter_code',
    )

    class Meta:
        model = Chorus
        # lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'name',
            'slug',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            'notes',
            'director',
            'chapterName',
            'chapterCode',
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
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            'notes',
            'contests',
        )


class ConventionSerializer(serializers.ModelSerializer):
    contests = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )

    kind = serializers.CharField(
        source='get_kind_display',
    )

    class Meta:
        model = Convention
        # lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'kind',
            'year',
            'dates',
            'location',
            'timezone',
            'contests',
        )
