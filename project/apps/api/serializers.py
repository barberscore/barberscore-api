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
            'slug',
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

    # contestants = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

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
            # 'contestants',
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
            'performances',
        )


class ContestSerializer(serializers.ModelSerializer):
    contestants = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    # contestants = ContestantSerializer(
    #     many=True,
    #     read_only=True,
    # )

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

    # contests = ContestSerializer(
    #     read_only=True,
    #     many=True,
    # )

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
