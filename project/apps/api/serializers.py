from rest_framework import serializers

from .models import (
    Chorus,
    Quartet,
    Contest,
    Convention,
    Contestant,
    Performance,
    Group,
)


class PerformanceSerializer(serializers.ModelSerializer):
    round = serializers.CharField(
        source='get_round_display',
    )

    class Meta:
        model = Performance
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

    district = serializers.CharField(
        source='get_district_tag_display',
    )

    class Meta:
        model = Group
        fields = (
            'id',
            'slug',
            'name',
            'district',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
        )


class ContestantContestSerializer(serializers.ModelSerializer):
    performances = PerformanceSerializer(
        many=True,
        read_only=True,
    )

    group = GroupSerializer(
        read_only=True,
    )

    class Meta:
        model = Contestant
        fields = (
            'id',
            'slug',
            'group',
            'seed',
            'prelim',
            'place',
            'score',
            'performances',
        )


class ContestSerializer(serializers.ModelSerializer):
    contestants = ContestantContestSerializer(
        many=True,
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


class ContestantGroupSerializer(serializers.ModelSerializer):
    performances = PerformanceSerializer(
        many=True,
        read_only=True,
    )

    contest = serializers.StringRelatedField(
        read_only=True,
    )

    class Meta:
        model = Contestant
        fields = (
            'id',
            'slug',
            'contest',
            'seed',
            'prelim',
            'place',
            'score',
            'performances',
        )


class ConventionSerializer(serializers.ModelSerializer):
    contests = ContestSerializer(
        many=True,
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


class ChorusSerializer(serializers.ModelSerializer):
    contestants = ContestantGroupSerializer(
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


class QuartetSerializer(serializers.ModelSerializer):
    contestants = ContestantGroupSerializer(
        many=True,
        read_only=True,
    )

    lead = serializers.StringRelatedField(
        read_only=True,
    )

    tenor = serializers.StringRelatedField(
        read_only=True,
    )

    baritone = serializers.StringRelatedField(
        read_only=True,
    )

    bass = serializers.StringRelatedField(
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
            # 'district',
            'contestants',
        )
