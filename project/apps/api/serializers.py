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
    Event,
    Judge,
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

    events = serializers.SlugRelatedField(
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
            'level',
            'kind',
            'year',
            'district',
            'convention',
            'panel',
            'is_active',
            'status',
            'scoresheet_pdf',
            'contestants',
            'events',
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

    events = serializers.SlugRelatedField(
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
            'contest',
            'group',
            'district',
            'picture',
            'seed',
            'prelim',
            'points',
            'score',
            'place',
            'men',
            'quarters_points',
            'semis_points',
            'finals_points',
            'quarters_score',
            'semis_score',
            'finals_score',
            'quarters_place',
            'semis_place',
            'finals_place',
            'delta_score',
            'delta_place',
            'status',
            'performances',
            'directors',
            'singers',
            'events',
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

    events = serializers.SlugRelatedField(
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
            'kind',
            'dates',
            'location',
            'year',
            'district',
            'timezone',
            'contests',
            'events',
            'is_active',
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
            'is_active',
            'contestants',
        )


class EventSerializer(serializers.ModelSerializer):
    convention = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    contest = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    contestant = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Event
        fields = [
            'id',
            # 'url',
            'slug',
            'name',
            'convention',
            'contest',
            'contestant',
            'draw',
            'location',
            'is_active',
            'kind',
        ]


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
            'is_active',
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


class PerformanceSerializer(serializers.ModelSerializer):
    catalog = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    song = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    person = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    contestant = serializers.SlugRelatedField(
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
            'session',
            'order',
            'status',
            'is_parody',
            'catalog',
            'song',
            'person',
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
            'is_active',
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
