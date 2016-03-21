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
    Submission,
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
            'contests',
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
            'status',
            'code',
            'organization',
            'groups',
            'members',
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
            'is_generic',
            'is_parody',
            'is_medley',
            'songs',
            'submissions',
        )


class ContestSerializer(serializers.ModelSerializer):
    # champion = serializers.StringRelatedField(
    #     read_only=True,
    # )

    class Meta:
        model = Contest
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'status',
            'cycle',
            'is_qualifier',
            'champion',
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

        readonly_fields = [
            'rank',
            'mus_points',
            'prs_points',
            'sng_points',
            'total_points',
            'mus_score',
            'prs_score',
            'sng_score',
            'total_score',
        ]


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
            'year',
            'date',
            'venue',
            'organization',
            'drcj',
            'sessions',
        )


class GroupSerializer(serializers.ModelSerializer):
    date = DateRangeField()

    class Meta:
        model = Group
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'status',
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
            'age',
            'is_novice',
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
            'status',
            'category',
            'designation',
            'kind',
            'slot',
            'person',
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
            'status',
            'person',
            'chapter',
        )


class OrganizationSerializer(serializers.ModelSerializer):
    date = DateRangeField()

    class Meta:
        model = Organization
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'status',
            'level',
            'kind',
            'date',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            'short_name',
            'code',
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
    # get_preceding = serializers.PrimaryKeyRelatedField(read_only=True)
    # get_next = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Performance
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'status',
            'slot',
            'scheduled',
            'actual',
            'get_preceding',
            'get_next',
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

        readonly_fields = [
            'get_preceding',
            'get_next',
            'mus_points',
            'prs_points',
            'sng_points',
            'total_points',
            'mus_score',
            'prs_score',
            'sng_score',
            'total_score',
        ]


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
            'men',
            'picture',
            'seed',
            'prelim',
            'rank',
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
            'contestants',
            'submissions',
            'roles',
        )
        read_only_fields = [
            'picture',
            'seed',
            'prelim',
            'rank',
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
        ]


class PersonSerializer(serializers.ModelSerializer):
    date = DateRangeField()

    class Meta:
        model = Person
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'status',
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
            'certifications',
            'common_name',
            'full_name',
            'formal_name',
            'first_name',
            'last_name',
            'nick_name',
            'organization',
            'chapter',
        )
        read_only_fields = [
            'picture',
            'common_name',
            'full_name',
            'formal_name',
            'first_name',
            'last_name',
            'nick_name',
        ]


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'status',
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
            'num',
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
            'status',
            'song',
            'judge',
            'points',
            'category',
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
            'performers',
            'contests',
            'judges',
            'rounds',
        )


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
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
            'status',
            'order',
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

        readonly_fields = [
            'mus_points',
            'prs_points',
            'sng_points',
            'total_points',
            'mus_score',
            'prs_score',
            'sng_score',
            'total_score',
        ]


class VenueSerializer(serializers.ModelSerializer):
    timezone = TimezoneField()

    class Meta:
        model = Venue
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'location',
            'city',
            'state',
            'timezone',
            'conventions',
        )
