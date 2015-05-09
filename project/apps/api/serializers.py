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

    class Meta:
        model = District
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
            'kind',
            'longName',
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


class ContestantGroupSerializer(serializers.ModelSerializer):
    performances = PerformanceSerializer(
        many=True,
        read_only=True,
    )

    group = GroupSerializer(
        read_only=True,
    )

    class Meta:
        model = Contestant
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            # 'slug',
            'group',
            # 'district',
            'seed',
            'prelim',
            'place',
            'score',
            'performances',
        )


class ContestSerializer(serializers.ModelSerializer):
    contestants = ContestantGroupSerializer(
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
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
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
    contests = ContestSerializer(
        many=True,
    )

    # kind = serializers.CharField(
    #     source='get_kind_display',
    # )

    class Meta:
        model = Convention
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
            # 'kind',
            # 'year',
            'name',
            # 'location',
            'dates',
            'timezone',
            'contests',
        )


class QuartetContestSerializer(serializers.ModelSerializer):
    # performances = PerformanceSerializer(
    #     many=True,
    #     read_only=True,
    # )

    contest = serializers.StringRelatedField(
        read_only=True,
    )

    # contest = ContestSerializer(
    #     read_only=True,
    # )

    class Meta:
        model = Contestant
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
            'contest',
            'place',
            'score',
            'seed',
            'prelim',
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
        # lookup_field = 'slug'
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
    contestants = QuartetContestSerializer(
        many=True,
        read_only=True,
        # source='contestants.contest'
    )

    district = serializers.CharField(
        read_only=True,
        source='district.name',
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
            'district',
            'contestants',
        )
