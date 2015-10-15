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
    Arrangement,
    Score,
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

    class Meta:
        model = Group
        fields = (
            'id',
            # 'url',
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
            'is_active',
            'contestants',
        )


class ContestantSerializer(serializers.ModelSerializer):
    contest = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    group = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    district = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

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
        fields = (
            'id',
            # 'url',
            'slug',
            'name',
            'contest',
            'group',
            'district',
            'picture',
            'seed',
            'prelim',
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
            'men',
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
        fields = (
            'id',
            # 'url',
            'slug',
            'name',
            'year',
            'level',
            'kind',
            'district',
            'panel',
            'is_active',
            'status',
            # 'is_complete',
            # 'is_place',
            # 'is_score',
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
        fields = (
            'id',
            # 'url',
            'slug',
            'name',
            'dates',
            'year',
            'timezone',
            'contests',
            'is_active',
        )
        # extra_kwargs = {
        #     # 'url': {'view_name': 'convention-detail', 'lookup_field': 'slug'},
        #     'contests': {'view_name': 'contest-detail', 'lookup_field': 'slug'},
        # }


class PersonSerializer(serializers.ModelSerializer):
    arrangements = serializers.SlugRelatedField(
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
        fields = (
            'id',
            # 'url',
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
            'is_active',
            'arrangements',
            'choruses',
            'quartets',
        )


class SongSerializer(serializers.ModelSerializer):
    arrangements = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Song
        fields = (
            'id',
            # 'url',
            'slug',
            'name',
            'arrangements',
        )


class DistrictSerializer(serializers.ModelSerializer):
    contestants = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = District
        fields = (
            'id',
            # 'url',
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
            'is_active',
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
    arrangement = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    contestant = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Performance
        fields = (
            'id',
            # 'url',
            'slug',
            'name',
            'session',
            'order',
            'arrangement',
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
            # 'url',
            'slug',
            'contestant',
            'person',
            'name',
            'part',
        )


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
            # 'url',
            'slug',
            'contestant',
            'person',
            'name',
            'part',
        )


class ArrangementSerializer(serializers.ModelSerializer):
    song = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    arranger = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Arrangement
        fields = (
            'id',
            # 'url',
            'slug',
            'name',
            'song',
            'arranger',
        )


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
