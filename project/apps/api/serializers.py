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
    Catalog,
    Score,
    Award,
    Judge,
    Appearance,
)

from .search_indexes import (
    GroupIndex,
    SongIndex,
    PersonIndex,
)


class CatalogSerializer(serializers.ModelSerializer):
    song = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    person = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Catalog
        fields = (
            'id',
            # 'url',
            'slug',
            'name',
            'song',
            'person',
        )


class AwardSerializer(serializers.ModelSerializer):
    contestant = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Award
        fields = [
            'id',
            # 'url',
            'slug',
            'name',
            'contestant',
            'kind',
        ]


class ContestSerializer(serializers.ModelSerializer):
    convention = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

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
            'status',
            'level',
            'kind',
            'goal',
            'rounds',
            'year',
            'district',
            'convention',
            'rep',
            'admin',
            'panel',
            'scoresheet_pdf',
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

    appearances = serializers.SlugRelatedField(
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

    awards = serializers.SlugRelatedField(
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
            'status',
            'contest',
            'group',
            'district',
            'picture',
            'seed',
            'prelim',
            'place',
            'men',
            'mus_points',
            'prs_points',
            'sng_points',
            'total_points',
            'mus_score',
            'prs_score',
            'sng_score',
            'total_score',
            'delta_score',
            'delta_place',
            'appearances',
            'directors',
            'singers',
            'awards',
        )


class ConventionSerializer(serializers.ModelSerializer):
    district = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

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
            'status',
            'kind',
            'dates',
            'location',
            'year',
            'district',
            'timezone',
            'contests',
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
            'name',
            'contestant',
            'person',
            'part',
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
            'start',
            'end',
            'kind',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            'kind',
            'long_name',
            'contestants',
        )


class GroupSerializer(serializers.ModelSerializer):

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
            'start',
            'end',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            'kind',
            'chapter_name',
            'chapter_code',
            'contestants',
        )


class JudgeSerializer(serializers.ModelSerializer):
    scores = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )
    contest = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )
    person = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Judge
        fields = (
            'id',
            # 'url',
            'slug',
            'name',
            'contest',
            'person',
            'part',
            'status',
            'scores',
            'num',
        )


class AppearanceSerializer(serializers.ModelSerializer):
    contestant = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    performances = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Appearance
        fields = (
            'id',
            # 'url',
            'slug',
            'name',
            'status',
            'session',
            'draw',
            'start',
            'mus_points',
            'prs_points',
            'sng_points',
            'total_points',
            'mus_score',
            'prs_score',
            'sng_score',
            'total_score',
            'contestant',
            'performances',
        )


class PerformanceSerializer(serializers.ModelSerializer):
    song = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    # person = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    appearance = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    scores = serializers.SlugRelatedField(
        many=True,
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
            'order',
            'status',
            'is_parody',
            # 'catalog',
            'song',
            # 'person',
            'appearance',
            'mus_points',
            'prs_points',
            'sng_points',
            'total_points',
            'mus_score',
            'prs_score',
            'sng_score',
            'total_score',
            'penalty',
            'scores',
        )


class PersonSerializer(serializers.ModelSerializer):
    catalogs = serializers.SlugRelatedField(
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

    panels = serializers.SlugRelatedField(
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
            'start',
            'end',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            'kind',
            'catalogs',
            'choruses',
            'quartets',
            'panels',
        )


class ScoreSerializer(serializers.ModelSerializer):
    performance = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    judge = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Score
        fields = [
            'id',
            # 'url',
            'slug',
            'name',
            'performance',
            'judge',
            'points',
            'status',
            'category',
            'is_practice',
        ]


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
            'name',
            'contestant',
            'person',
            'part',
        )


class SongSerializer(serializers.ModelSerializer):
    catalogs = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    performances = serializers.SlugRelatedField(
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
            'catalogs',
            'performances',
        )
