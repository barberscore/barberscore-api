# Third-Party
import pytz
import six
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework_json_api import serializers

# Django
from django.core.exceptions import ValidationError

# Local
from .models import (
    Award,
    Catalog,
    Certification,
    Chapter,
    Contest,
    Contestant,
    Convention,
    Group,
    Host,
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
    Slot,
    Song,
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
            'organization',
            'contests',
        )


class CatalogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catalog
        fields = (
            'id',
            'url',
            'name',
            'status',
            'bhs_id',
            'title',
            'published',
            'arranger',
            'arranger_fee',
            'difficulty',
            'gender',
            'tempo',
            'is_medley',
            'is_learning',
            'voicing',
        )


class CertificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Certification
        fields = (
            'id',
            'url',
            'name',
            'category',
            'kind',
            'status',
            'start_date',
            'end_date',
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


class ContestSerializer(serializers.ModelSerializer):
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
            'performer',
            'contest',
        )


class ConventionSerializer(serializers.ModelSerializer):
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
            'start_date',
            'end_date',
            'venue',
            'organization',
            'drcj',
            'sessions',
        )


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = (
            'id',
            'url',
            'name',
            'name',
            'status',
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


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = (
            'id',
            'url',
            'name',
            'status',
            'convention',
            'organization',
        )


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

    class Meta:
        model = Organization
        fields = (
            'id',
            'url',
            'name',
            'status',
            'level',
            'kind',
            'start_date',
            'end_date',
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
    # rank = RankField(read_only=True)
    # mus_points = MusPointsField(read_only=True)
    # prs_points = PrsPointsField(read_only=True)
    # sng_points = SngPointsField(read_only=True)
    # total_points = TotalPointsField(read_only=True)
    # mus_score = MusScoreField(read_only=True)
    # prs_score = PrsScoreField(read_only=True)
    # sng_score = SngScoreField(read_only=True)
    # total_score = TotalScoreField(read_only=True)

    class Meta:
        model = Performance
        fields = (
            'id',
            'url',
            'name',
            'status',
            'num',
            'rank',
            'actual_start',
            'actual_finish',
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
            'slot',
            'songs',
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


class PerformerSerializer(serializers.ModelSerializer):
    # rank = RankField(read_only=True)
    # mus_points = MusPointsField(read_only=True)
    # prs_points = PrsPointsField(read_only=True)
    # sng_points = SngPointsField(read_only=True)
    # total_points = TotalPointsField(read_only=True)
    # mus_score = MusScoreField(read_only=True)
    # prs_score = PrsScoreField(read_only=True)
    # sng_score = SngScoreField(read_only=True)
    # total_score = TotalScoreField(read_only=True)

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


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = (
            'id',
            'url',
            'name',
            'nomen',
            'status',
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
            'start_date',
            'end_date',
        )


class RoundSerializer(serializers.ModelSerializer):

    class Meta:
        model = Round
        fields = (
            'id',
            'url',
            'name',
            'status',
            'kind',
            'start_date',
            'end_date',
            'num',
            'mt',
            'session',
            'performances',
            'slots',
        )


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = [
            'id',
            'url',
            'name',
            'status',
            'category',
            'kind',
            'points',
            'original',
            'violation',
            'penalty',
            'song',
            'judge',
        ]


class SessionSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Session
        fields = (
            'id',
            'url',
            'name',
            'status',
            'kind',
            'convention',
            'start_date',
            'end_date',
            'num_rounds',
            'cursor',
            'current',
            'primary',
            'performers',
            'contests',
            'judges',
            'rounds',
            'permissions',
        )


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = (
            'id',
            'url',
            'name',
            'status',
            'title',
            'arranger',
            'source',
            'is_medley',
            'is_parody',
            'performer',
        )


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = (
            'id',
            'url',
            'name',
            'status',
            'num',
            'round',
            'performance',
            'photo',
            'arrive',
            'depart',
            'backstage',
            'onstage',
        )


class SongSerializer(serializers.ModelSerializer):
    # mus_points = MusPointsField(read_only=True)
    # prs_points = PrsPointsField(read_only=True)
    # sng_points = SngPointsField(read_only=True)
    # total_points = TotalPointsField(read_only=True)
    # mus_score = MusScoreField(read_only=True)
    # prs_score = PrsScoreField(read_only=True)
    # sng_score = SngScoreField(read_only=True)
    # total_score = TotalScoreField(read_only=True)

    class Meta:
        model = Song
        fields = (
            'id',
            'url',
            'name',
            'status',
            'num',
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
