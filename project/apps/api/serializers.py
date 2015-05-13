from rest_framework import serializers

from .models import (
    Convention,
    Contest,
    Contestant,
    Group,
    Performance,
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

    contestants = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    district = serializers.CharField(
        source='get_district_display',
    )

    kind = serializers.CharField(
        source='get_kind_display',
    )

    chapterName = serializers.CharField(
        source='chapter_name',
    )

    lead = serializers.StringRelatedField()

    tenor = serializers.StringRelatedField()

    baritone = serializers.StringRelatedField()

    bass = serializers.StringRelatedField()

    class Meta:
        model = Group
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'kind',
            'district',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            'director',
            'chapterName',
            'lead',
            'tenor',
            'baritone',
            'bass',
            'contestants',
        )


class ContestantSerializer(serializers.ModelSerializer):
    contest = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    performances = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    group = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Contestant
        lookup_field = 'slug'
        fields = (
            'id',
            'slug',
            'contest',
            'group',
            'seed',
            'prelim',
            'place',
            'score',
            'performances',
        )


class ContestSerializer(serializers.ModelSerializer):
    contestants = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    level = serializers.CharField(
        source='get_level_display',
    )

    kind = serializers.CharField(
        source='get_kind_display',
    )

    year = serializers.CharField(
        source='get_year_display',
    )

    district = serializers.CharField(
        source='get_district_display',
    )

    class Meta:
        model = Contest
        lookup_field = 'slug'
        fields = (
            'id',
            'slug',
            'level',
            'kind',
            'year',
            'district',
            'panel',
            'scoresheet_pdf',
            'contestants',
        )


class ConventionSerializer(serializers.ModelSerializer):
    contests = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Convention
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'dates',
            'timezone',
            'contests',
        )


class ScheduleSerializer(serializers.ModelSerializer):
    round = serializers.CharField(
        source='get_round_display',
    )

    kind = serializers.CharField(
        source='contestant.contest.get_kind_display',
    )

    prelim = serializers.FloatField(
        source='contestant.prelim',
    )

    group = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
        source='contestant.group',
    )

    class Meta:
        model = Performance
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
            'round',
            # 'day',
            'kind',
            'group',
            'prelim',
            'session',
            'queue',
            'stagetime',
            'song1',
            'song2',
        )
