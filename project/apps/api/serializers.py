# Third-Party
import pytz
import six
from drf_extra_fields.fields import (
    DateRangeField,
    DateTimeRangeField,
)
from rest_framework_json_api import serializers

# Django
from django.core.exceptions import ValidationError

# Local
from .models import (
    Award,
    Certification,
    Chapter,
    Chart,
    Contest,
    Contestant,
    ContestantScore,
    Convention,
    Group,
    Judge,
    Member,
    Organization,
    Performance,
    PerformanceScore,
    Performer,
    PerformerScore,
    Person,
    Role,
    Round,
    Score,
    Session,
    Song,
    SongScore,
    Submission,
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
            'name',
            'status',
            'kind',
            'championship_season',
            'qualifier_season',
            'size',
            'scope',
            'championship_rounds',
            'is_primary',
            'is_improved',
            'is_novice',
            'idiom',
            'threshold',
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
            'name',
            'category',
            'status',
            'date',
            'person',
            'judges',
        )


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = (
            'id',
            'url',
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
            'contestantscore',
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


class ContestantScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestantScore
        fields = (
            'contestant',
            'url',
            'mus_points',
            'prs_points',
            'sng_points',
            'total_points',
            'mus_score',
            'prs_score',
            'sng_score',
            'total_score',
            'contestant',
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


class ConventionSerializer(serializers.ModelSerializer):
    date = DateTimeRangeField()

    class Meta:
        model = Convention
        fields = (
            'id',
            'url',
            'name',
            'status',
            'kind',
            'season',
            'risers',
            'level',
            'is_prelims',
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
            'name',
            'chap_name',
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
            'roles',
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
            'name',
            'status',
            'category',
            'designation',
            'kind',
            'slot',
            'certification',
            'session',
            'scores',
        )


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = (
            'id',
            'url',
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
            'name',
            'status',
            'level',
            'kind',
            'date',
            'spots',
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
            'awards',
            'lft',
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
            'name',
            'status',
            'slot',
            'rank',
            'scheduled',
            'actual',
            'actual_start',
            'actual_finish',
            'is_advancing',
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
            'performancescore',
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


class PerformanceScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceScore
        fields = (
            'performance',
            'url',
            'is_advancing',
            'rank',
            'mus_points',
            'prs_points',
            'sng_points',
            'total_points',
            'mus_score',
            'prs_score',
            'sng_score',
            'total_score',
            'performance',
        )

        readonly_fields = [
            'is_advancing',
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


class PerformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performer
        fields = (
            'id',
            'url',
            'name',
            'status',
            'representing',
            'tenor',
            'lead',
            'baritone',
            'bass',
            'soa',
            'men',
            'risers',
            'is_evaluation',
            'is_private',
            'director',
            'codirector',
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
            'session',
            'group',
            'performances',
            'contestants',
            'submissions',
            'performerscore',
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
        ]


class PerformerScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformerScore
        fields = (
            'performer',
            'url',
            'mus_points',
            'prs_points',
            'sng_points',
            'total_points',
            'mus_score',
            'prs_score',
            'sng_score',
            'total_score',
            'performer',
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


class PersonSerializer(serializers.ModelSerializer):
    date = DateRangeField()

    class Meta:
        model = Person
        fields = (
            'id',
            'url',
            'name',
            'id_name',
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
    date = DateRangeField()

    class Meta:
        model = Role
        fields = (
            'id',
            'url',
            'name',
            'status',
            'group',
            'person',
            'part',
            'date',
        )


class RoundSerializer(serializers.ModelSerializer):
    date = DateTimeRangeField()

    class Meta:
        model = Round
        fields = (
            'id',
            'url',
            'name',
            'status',
            'kind',
            'date',
            'num',
            'mt',
            'session',
            'performances',
        )


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = [
            'id',
            'url',
            'name',
            'status',
            'song',
            'judge',
            'points',
            'category',
            'kind',
        ]


class SessionSerializer(serializers.ModelSerializer):
    date = DateTimeRangeField()

    class Meta:
        model = Session
        fields = (
            'id',
            'url',
            'name',
            'status',
            'kind',
            'convention',
            'date',
            'num_rounds',
            'cursor',
            'current',
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
            'name',
            'status',
            'order',
            'submission',
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
            'songscore',
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


class SongScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongScore
        fields = (
            'song',
            'url',
            'mus_points',
            'prs_points',
            'sng_points',
            'total_points',
            'mus_score',
            'prs_score',
            'sng_score',
            'total_score',
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
    timezone = TimezoneField(allow_null=True)

    class Meta:
        model = Venue
        fields = (
            'id',
            'url',
            'name',
            'location',
            'city',
            'state',
            'airport',
            'timezone',
            'conventions',
        )
