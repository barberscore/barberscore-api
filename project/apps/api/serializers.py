from rest_framework import serializers

from drf_haystack.serializers import HaystackSerializer

from .models import (
    Convention,
    Contest,
    Contestant,
    Group,
    District,
    Person,
    Song,
    Performance,
    Singer,
    Director,
    Chart,
    # Arranger,
)

from .search_indexes import (
    GroupIndex,
    SongIndex,
    PersonIndex,
)


class GroupSerializer(serializers.ModelSerializer):

    chapterName = serializers.CharField(
        source='chapter_name',
    )

    contestants = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    # lead = serializers.StringRelatedField()

    # tenor = serializers.StringRelatedField()

    # baritone = serializers.StringRelatedField()

    # bass = serializers.StringRelatedField()

    class Meta:
        model = Group
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'kind',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            'notes',
            'chapterName',
            # 'lead',
            # 'tenor',
            # 'baritone',
            # 'bass',
            'contestants',
        )


class ContestantSerializer(serializers.ModelSerializer):
    contest = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    # district = serializers.StringRelatedField()

    group = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    # lead = serializers.StringRelatedField()

    # tenor = serializers.StringRelatedField()

    # baritone = serializers.StringRelatedField()

    # bass = serializers.StringRelatedField()

    # director = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # finals_song1_arranger = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # finals_song2_arranger = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # semis_song1_arranger = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # semis_song2_arranger = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # quarters_song1_arranger = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # quarters_song2_arranger = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    district = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    # lead = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )
    # tenor = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )
    # baritone = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )
    # bass = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # quarters_song1 = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # quarters_song2 = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # semis_song1 = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # semis_song2 = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # finals_song1 = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # finals_song2 = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    performances = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    directors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    singers = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Contestant
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'contest',
            'group',
            'district',
            'picture',
            'seed',
            'prelim',
            'draw',
            'stagetime',
            'place',
            'points',
            'score',
            'delta_score',
            'delta_place',
            'quarters_place',
            'quarters_score',
            'semis_place',
            'semis_score',
            'finals_place',
            'finals_score',
            'finals_points',
            'semis_points',
            'quarters_points',
            # 'finals_mus1_score',
            # 'finals_mus2_score',
            # 'semis_mus1_score',
            # 'semis_mus2_score',
            # 'quarters_mus1_score',
            # 'quarters_mus2_score',
            # 'finals_prs1_score',
            # 'finals_prs2_score',
            # 'semis_prs1_score',
            # 'semis_prs2_score',
            # 'quarters_prs1_score',
            # 'quarters_prs2_score',
            # 'finals_sng1_score',
            # 'finals_sng2_score',
            # 'semis_sng1_score',
            # 'semis_sng2_score',
            # 'quarters_sng1_score',
            # 'quarters_sng2_score',
            # 'quarters_song1',
            # 'quarters_song2',
            # 'semis_song1',
            # 'semis_song2',
            # 'finals_song1_arranger',
            # 'finals_song2_arranger',
            # 'semis_song1_arranger',
            # 'semis_song2_arranger',
            # 'quarters_song1_arranger',
            # 'quarters_song2_arranger',
            # 'finals_song1',
            # 'finals_song2',
            # 'quarters_song1_score',
            # 'quarters_song2_score',
            # 'semis_song1_score',
            # 'semis_song2_score',
            # 'finals_song1_score',
            # 'finals_song2_score',
            # 'director',

            # 'lead',
            # 'tenor',
            # 'baritone',
            # 'bass',
            'men',
            'district',
            'performances',
            'directors',
            'singers',
        )


class ContestSerializer(serializers.ModelSerializer):
    contestants = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    district = serializers.StringRelatedField()

    class Meta:
        model = Contest
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'year',
            'level',
            'kind',
            'district',
            'panel',
            'is_active',
            'is_complete',
            'is_place',
            'is_score',
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
            'year',
            'timezone',
            'contests',
            'is_active',
        )


class PersonSerializer(serializers.ModelSerializer):
    # contestants_director = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    # contestants_lead = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    # contestants_tenor = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    # contestants_baritone = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    # contestants_bass = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    charts = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    choruses = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )
    quartets = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Person
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
            'name',
            # 'contestants_director',
            # 'contestants_lead',
            # 'contestants_tenor',
            # 'contestants_baritone',
            # 'contestants_bass',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            'notes',
            'charts',
            # 'directors',
            'choruses',
            'quartets',
        )


class SongSerializer(serializers.ModelSerializer):
    # contestants_finals_song1 = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    # contestants_finals_song2 = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    # contestants_semis_song1 = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    # contestants_semis_song2 = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    # contestants_quarters_song1 = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    # contestants_quarters_song2 = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )
    charts = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Song
        fields = (
            'id',
            'url',
            'slug',
            'name',
            # 'contestants_finals_song1',
            # 'contestants_finals_song2',
            # 'contestants_semis_song1',
            # 'contestants_semis_song2',
            # 'contestants_quarters_song1',
            # 'contestants_quarters_song2',
            'charts',
        )
        lookup_field = 'slug'


class DistrictSerializer(serializers.ModelSerializer):
    contestants = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = District
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'kind',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            'notes',
            'long_name',
            # 'chapterName',
            # 'lead',
            # 'tenor',
            # 'baritone',
            # 'bass',
            'contestants',
        )


class SearchSerializer(HaystackSerializer):
    kind = serializers.CharField(
        source='model_name',
    )

    class Meta:
        index_classes = [
            GroupIndex,
            SongIndex,
            PersonIndex,
        ]
        fields = [
            "text",
            "name",
            "slug",
            "description",
            "kind",
        ]


class PerformanceSerializer(serializers.ModelSerializer):
    chart = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    # song = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    # arranger = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    contestant = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Performance
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'round',
            'order',
            # 'song',
            # 'arranger',
            'chart',
            'mus_points',
            'prs_points',
            'sng_points',
            'total_points',
            'mus_score',
            'prs_score',
            'sng_score',
            'total_score',
            'penalty',
            'contestant',
        )
        lookup_field = 'slug'


class SingerSerializer(serializers.ModelSerializer):
    contestant = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )
    person = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Singer
        fields = (
            'id',
            'url',
            'slug',
            'contestant',
            'person',
            'name',
            'part',
        )
        lookup_field = 'slug'


class DirectorSerializer(serializers.ModelSerializer):
    contestant = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )
    person = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Director
        fields = (
            'id',
            'url',
            'slug',
            'contestant',
            'person',
            'name',
            'part',
        )
        lookup_field = 'slug'


class ChartSerializer(serializers.ModelSerializer):
    song = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    arranger = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    # contestants_finals_song2 = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    # contestants_semis_song1 = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    # contestants_semis_song2 = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    # contestants_quarters_song1 = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    # contestants_quarters_song2 = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )
    performances = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Chart
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'song',
            'arranger',
            # 'contestants_finals_song1',
            # 'contestants_finals_song2',
            # 'contestants_semis_song1',
            # 'contestants_semis_song2',
            # 'contestants_quarters_song1',
            # 'contestants_quarters_song2',
            'performances',
        )
        lookup_field = 'slug'
