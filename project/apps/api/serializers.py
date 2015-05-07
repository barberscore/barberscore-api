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
    Group,
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
        lookup_field = 'slug'
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

    choruses = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
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
            'choruses',
        )


class PerformanceSerializer(serializers.ModelSerializer):
    round = serializers.CharField(
        source='get_round_display',
    )

    class Meta:
        model = Performance
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
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


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group


class ContestantSerializer(serializers.ModelSerializer):
    performances = PerformanceSerializer(
        many=True,
        read_only=True,
    )

    # group = serializers.StringRelatedField(
    #     read_only=True,
    # )

    group = GroupSerializer(
        read_only=True,
    )

    class Meta:
        model = Contestant
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
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
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
            'name',
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
    contestants = ContestantSerializer(
        many=True,
    )

    kind = serializers.CharField(
        source='get_kind_display',
    )

    class Meta:
        model = Contest
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
            'kind',
            'panel',
            'scoresheet_pdf',
            'contestants',
        )


class ConventionSerializer(serializers.ModelSerializer):
    contests = ContestSerializer(
        many=True,
    )

    kind = serializers.CharField(
        source='get_kind_display',
    )

    class Meta:
        model = Convention
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
            'kind',
            'year',
            'dates',
            'location',
            'timezone',
            'contests',
        )


class QuartetSerializer(serializers.ModelSerializer):
    contestants = ContestantSerializer(
        many=True,
        read_only=True,
    )

    lead = SingerSerializer(
        read_only=True,
    )

    tenor = SingerSerializer(
        read_only=True,
    )

    baritone = SingerSerializer(
        read_only=True,
    )

    bass = SingerSerializer(
        read_only=True,
    )

    class Meta:
        model = Quartet
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
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
            'lead',
            'tenor',
            'baritone',
            'bass',
            'contestants',
        )

