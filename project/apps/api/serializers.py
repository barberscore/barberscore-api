from rest_framework import serializers

from drf_haystack.serializers import HaystackSerializer

from .models import (
    Convention,
    Contest,
    Award,
    Competitor,
    Contestant,
    Session,
    Group,
    Person,
    Tune,
    Song,
    Singer,
    Director,
    Catalog,
    Score,
    Judge,
    Performance,
    Organization,
)

from .search_indexes import (
    GroupIndex,
    TuneIndex,
    PersonIndex,
)


class AwardSerializer(serializers.ModelSerializer):
    contest = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    organization = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    competitors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Award
        fields = (
            'id',
            # 'url',
            'slug',
            'name',
            'status',
            'organization',
            'level',
            'kind',
            'goal',
            'year',
            'rounds',
            'qual_score',
            'contest',
            'competitors',
        )


class CatalogSerializer(serializers.ModelSerializer):
    tune = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    arrangers = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Catalog
        fields = (
            'id',
            # 'url',
            'tune',
            'song_name',
            'arrangers',
        )


class CompetitorSerializer(serializers.ModelSerializer):
    award = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    contestant = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Competitor
        fields = (
            'id',
            # 'url',
            'slug',
            'name',
            'status',
            'place',
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
            'award',
            'contestant',
        )


class ContestSerializer(serializers.ModelSerializer):
    convention = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    awards = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    sessions = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    judges = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    contestants = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Contest
        fields = (
            'id',
            # 'url',
            'slug',
            'name',
            'status',
            'kind',
            'rounds',
            'size',
            'convention',
            'awards',
            'sessions',
            'contestants',
            'judges',
        )


class ContestantSerializer(serializers.ModelSerializer):
    contest = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    organization = serializers.SlugRelatedField(
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

    competitors = serializers.SlugRelatedField(
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
            'organization',
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
            'contest',
            'performances',
            'directors',
            'singers',
            'competitors',
        )


class ConventionSerializer(serializers.ModelSerializer):
    organization = serializers.SlugRelatedField(
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
            'organization',
            # 'timezone',
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
            'start_date',
            'end_date',
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
            'person',
            'kind',
            'status',
            'contest',
            'scores',
        )


class OrganizationSerializer(serializers.ModelSerializer):
    children = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )
    parent = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Organization
        fields = (
            'id',
            # 'url',
            'slug',
            'name',
            'start_date',
            'end_date',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            # 'kind',
            'long_name',
            'parent',
            'children',
            # 'contestants',
        )


class PerformanceSerializer(serializers.ModelSerializer):
    contestant = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    session = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    songs = serializers.SlugRelatedField(
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
            'status',
            'draw',
            'start_time',
            'mus_points',
            'prs_points',
            'sng_points',
            'total_points',
            'mus_score',
            'prs_score',
            'sng_score',
            'total_score',
            'session',
            'contestant',
            'songs',
        )


class PersonSerializer(serializers.ModelSerializer):
    # catalogs = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

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

    contests = serializers.SlugRelatedField(
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
            'start_date',
            'end_date',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            'kind',
            # 'catalogs',
            'choruses',
            'quartets',
            'contests',
        )


class ScoreSerializer(serializers.ModelSerializer):
    song = serializers.SlugRelatedField(
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
            'song',
            'judge',
            'points',
            'status',
            'kind',
        ]


class SearchSerializer(HaystackSerializer):
    kind = serializers.CharField(
        source='model_name',
    )

    class Meta:
        index_classes = [
            GroupIndex,
            TuneIndex,
            PersonIndex,
        ]
        fields = [
            "text",
            "name",
            "slug",
            "description",
            "kind",
        ]


class SessionSerializer(serializers.ModelSerializer):
    contest = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )
    performances = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Session
        fields = (
            'id',
            # 'url',
            'slug',
            'name',
            'status',
            'kind',
            'slots',
            'contest',
            'performances',
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
            'name',
            'contestant',
            'person',
            'part',
        )


class SongSerializer(serializers.ModelSerializer):
    tune = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    # catalog = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='slug',
    # )

    performance = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    scores = serializers.SlugRelatedField(
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
            'order',
            'status',
            'is_parody',
            'tune',
            # 'catalog',
            'arranger',
            'performance',
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


class TuneSerializer(serializers.ModelSerializer):
    # catalogs = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    songs = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Tune
        fields = (
            'id',
            # 'url',
            'slug',
            'name',
            # 'catalogs',
            'songs',
        )
