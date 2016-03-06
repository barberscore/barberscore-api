from rest_framework_json_api import serializers

import six
import pytz

from django.core.exceptions import (
    ValidationError,
)

from drf_extra_fields.fields import (
    DateTimeRangeField,
    DateRangeField,
)

from .models import (
    Award,
    Certification,
    Chapter,
    Chart,
    Contest,
    Contestant,
    Convention,
    Group,
    Judge,
    Member,
    Organization,
    Performance,
    Performer,
    Person,
    Role,
    Round,
    Score,
    Session,
    Setlist,
    Song,
    Venue,
)


class TimezoneField(serializers.Field):
    def to_representation(self, obj):
        return six.text_type(obj)

    def to_internal_value(self, data):
        try:
            return pytz.timezone(str(data))
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValidationError('Unknown timezone')


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'status',
            'kind',
            'season',
            'size',
            'scope',
            'num_rounds',
            'is_primary',
            'is_improved',
            'is_novice',
            'idiom',
            'cutoff',
            'level',
            'organization',
        )
        read_only_fields = [
            'level',
        ]


class CertificationSerializer(serializers.ModelSerializer):
    date = DateRangeField()

    class Meta:
        model = Certification
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'category',
            'status',
            'date',
            'person',
        )


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'organization',
        )


class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chart
        fields = (
            'id',
            'url',
            'name',
            'status',
            'title',
            'arranger',
            'composer',
            'lyricist',
        )


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'status',
            'contestants',
            'award',
            'session',
        )


class ContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contestant
        fields = (
            'id',
            'url',
            'name',
            'slug',
            'status',
            'rank',
            'mus_points',
            'prs_points',
            'sng_points',
            'total_points',
            'mus_score',
            'prs_score',
            'sng_score',
            'total_score',
            'performer',
            'contest',
        )


class ConventionSerializer(serializers.ModelSerializer):
    date = DateRangeField()

    class Meta:
        model = Convention
        fields = (
            'id',
            'url',
            'name',
            'slug',
            'status',
            'season',
            'level',
            'division',
            'date',
            'venue',
            'year',
            'organization',
            'drcj',
            'sessions',
            'human_date',
        )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'date',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            'kind',
            'chapter',
            'organization',
            'performers',
        )
        read_only_fields = [
            'picture',
        ]


class JudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Judge
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'person',
            'category',
            'designation',
            'kind',
            'slot',
            'status',
            'session',
            'scores',
        )


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'person',
            'chapter',
        )


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'date',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            'long_name',
            'parent',
            'children',
        )
        read_only_fields = [
            'picture',
        ]


class PerformanceSerializer(serializers.ModelSerializer):
    scheduled = DateTimeRangeField()
    actual = DateTimeRangeField()

    class Meta:
        model = Performance
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'status',
            'slot',
            'start_dt',
            'scheduled',
            'actual',
            'mus_points',
            'prs_points',
            'sng_points',
            'total_points',
            'mus_score',
            'prs_score',
            'sng_score',
            'total_score',
            'round',
            'performer',
            'songs',
        )


class PerformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performer
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'status',
            'organization',
            'picture',
            'seed',
            'prelim',
            'rank',
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
            'session',
            'group',
            'performances',
            'roles',
            'contestants',
        )
        read_only_fields = [
            'picture',
        ]


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'date',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            'roles',
            'panels',
            'conventions',
        )
        read_only_fields = [
            'picture',
        ]


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'performer',
            'person',
            'part',
        )


class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'status',
            'kind',
            'session',
            'performances',
        )


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = [
            'id',
            'url',
            'slug',
            'name',
            'song',
            'judge',
            'points',
            'status',
            'kind',
        ]


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'status',
            'kind',
            'convention',
            'administrator',
            'aca',
            'rounds',
            'performers',
            'contests',
            'judges',
        )


class SetlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setlist
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'status',
            'chart',
            'performer',
        )


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'order',
            'title',
            'status',
            'is_parody',
            'chart',
            'performance',
            'mus_points',
            'prs_points',
            'sng_points',
            'total_points',
            'mus_score',
            'prs_score',
            'sng_score',
            'total_score',
            'scores',
        )


class VenueSerializer(serializers.ModelSerializer):
    timezone = TimezoneField()

    class Meta:
        model = Venue
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'timezone',
            'conventions',
        )
