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
    class Meta:
        model = Performance
        lookup_field = 'slug'
        fields = (
            'id',
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
            'mus1_score',
            'prs1_score',
            'sng1_score',
            'song1_points',
            'song1_score',
            'mus2_score',
            'prs2_score',
            'sng2_score',
            'song2_points',
            'song2_score',
            'points',
            'score',
        )


class GroupSerializer(serializers.ModelSerializer):

    chapterName = serializers.CharField(
        source='chapter_name',
    )

    contestants = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Contestant.objects.filter(
            contest__level=Contest.INTERNATIONAL,
        ).order_by('-contest__year'),
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
            'bsmdb',
            'contestants',
        )


class ContestantSerializer(serializers.ModelSerializer):
    contest = serializers.SlugRelatedField(
        queryset=Contest.objects.filter(
            level=Contest.INTERNATIONAL,
        ).order_by('-contest__year'),
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
            'url',
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
            'men',
            'performances',
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
            'year',
            'level',
            'kind',
            'district',
            'panel',
            'is_active',
            'is_complete',
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


class NoteSerializer(serializers.ModelSerializer):
    performance = serializers.SlugRelatedField(
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
