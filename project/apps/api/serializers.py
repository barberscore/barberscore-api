from rest_framework import serializers

from .models import (
    Convention,
    Contest,
    Contestant,
    Group,
    Performance,
    Note,
)

from django.contrib.auth import get_user_model
User = get_user_model()


class PerformanceSerializer(serializers.ModelSerializer):
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
            'round',
            'kind',
            'prelim',
            'group',
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
            'score',
        )


class GroupSerializer(serializers.ModelSerializer):

    kind = serializers.CharField(
        source='get_kind_display',
    )

    chapterName = serializers.CharField(
        source='chapter_name',
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
            'chapterName',
            # 'lead',
            # 'tenor',
            # 'baritone',
            # 'bass',
            'bsmdb',
            # 'contestants',
        )


class ContestantSerializer(serializers.ModelSerializer):
    contest = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    performances = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )

    district = serializers.StringRelatedField()

    group = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    lead = serializers.StringRelatedField()

    tenor = serializers.StringRelatedField()

    baritone = serializers.StringRelatedField()

    bass = serializers.StringRelatedField()

    director = serializers.StringRelatedField()

    # group = GroupSerializer(
    #     read_only=True,
    # )

    # performances = PerformanceSerializer(
    #     read_only=True,
    #     many=True,
    # )

    class Meta:
        model = Contestant
        lookup_field = 'slug'
        fields = (
            'id',
            'slug',
            'contest',
            'group',
            'district',
            'seed',
            'prelim',
            'place',
            'score',
            'queue',
            'stagetime',
            'quarters_place',
            'quarters_score',
            'semis_place',
            'semis_score',
            'finals_place',
            'finals_score',
            'director',
            'lead',
            'tenor',
            'baritone',
            'bass',
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

    district = serializers.StringRelatedField()

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
            'is_active',
            'is_complete',
        )


class ConventionSerializer(serializers.ModelSerializer):
    contests = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    # contests = ContestSerializer(
    #     read_only=True,
    #     many=True,
    # )

    year = serializers.CharField(
        source='get_year_display',
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


class NoteSerializer(serializers.ModelSerializer):
    performance = serializers.SlugRelatedField(
        # read_only=True,
        queryset=Performance.objects.all(),
        slug_field='slug',
    )

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        # read_only=True,
    )

    class Meta:
        model = Note
        fields = (
            'id',
            'text',
            'performance',
            'user',
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
        )
