# Third-Party
import pytz
import six
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework_json_api import serializers

# Django
from django.core.exceptions import ValidationError

# Local
from .models import (
    Assignment,
    Award,
    Catalog,
    Contest,
    ContestScore,
    Contestant,
    ContestantScore,
    Convention,
    Entity,
    Host,
    Membership,
    Office,
    Officer,
    Performance,
    PerformanceScore,
    Performer,
    PerformerScore,
    Person,
    Round,
    Score,
    Session,
    Slot,
    Song,
    SongScore,
    Submission,
    Venue,
    User,
)


class EntitySerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Entity
        fields = [
            'id',
            'url',
            'nomen',
            'name',
            'status',
            'level',
            'kind',
            'age',
            'is_novice',
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
            'short_name',
            'code',
            'long_name',
            'parent',
            'children',
            'awards',
            'lft',
            'permissions',
        ]
        read_only_fields = [
            'picture',
        ]


class MembershipSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Membership
        fields = [
            'id',
            'url',
            'nomen',
            'status',
            'part',
            'start_date',
            'end_date',
            'entity',
            'person',
            'permissions',
        ]


class OfficeSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Office
        fields = [
            'id',
            'url',
            'nomen',
            'name',
            'status',
            'kind',
            'short_name',
            'long_name',
            'permissions',
        ]


class OfficerSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Officer
        fields = [
            'id',
            'url',
            'nomen',
            'status',
            'start_date',
            'end_date',
            'office',
            'membership',
            'permissions',
        ]


class TimezoneField(serializers.Field):
    def to_representation(self, obj):
        return six.text_type(obj)

    def to_internal_value(self, data):
        try:
            return pytz.timezone(str(data))
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValidationError('Unknown timezone')


class AssignmentSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Assignment
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'category',
            'designation',
            'kind',
            'slot',
            'person',
            'session',
            'permissions',
        )


class AwardSerializer(serializers.ModelSerializer):

    permissions = DRYPermissionsField()

    class Meta:
        model = Award
        fields = (
            'id',
            'url',
            'nomen',
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
            'contests',
            'permissions',
        )


class CatalogSerializer(serializers.ModelSerializer):

    permissions = DRYPermissionsField()

    class Meta:
        model = Catalog
        fields = (
            'id',
            'url',
            'nomen',
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
            'permissions',
        )


class ContestSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Contest
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'is_qualifier',
            'contestants',
            'award',
            'session',
            'permissions',
        )


class ContestScoreSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = ContestScore
        fields = (
            'id',
            'url',
            'champion',
            'permissions',
        )


class ContestantSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Contestant
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'performer',
            'contest',
            'permissions',
        )


class ContestantScoreSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = ContestantScore
        fields = (
            'id',
            'url',
            'rank',
            'mus_points',
            'prs_points',
            'sng_points',
            'total_points',
            'mus_score',
            'prs_score',
            'sng_score',
            'total_score',
            'permissions',
        )


class ConventionSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Convention
        fields = (
            'id',
            'url',
            'nomen',
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
            'hosts'
            # 'drcj',
            'sessions',
            'permissions',
        )


class HostSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Host
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'convention',
            'entity',
            'permissions',
        )


class PerformanceSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Performance
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'num',
            'actual_start',
            'actual_finish',
            'round',
            'performer',
            'slot',
            'songs',
            'permissions',
        )


class PerformanceScoreSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = PerformanceScore
        fields = (
            'id',
            'url',
            'rank',
            'mus_points',
            'prs_points',
            'sng_points',
            'total_points',
            'mus_score',
            'prs_score',
            'sng_score',
            'total_score',
            'permissions',
        )


class PerformerSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Performer
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            # 'representing',
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
            'session',
            'entity',
            'performances',
            'contestants',
            'submissions',
            'permissions',
        )
        read_only_fields = [
            'picture',
        ]


class PerformerScoreSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = PerformerScore
        fields = (
            'id',
            'url',
            'rank',
            'mus_points',
            'prs_points',
            'sng_points',
            'total_points',
            'mus_score',
            'prs_score',
            'sng_score',
            'total_score',
            'permissions',
        )


class PersonSerializer(serializers.ModelSerializer):

    permissions = DRYPermissionsField()

    class Meta:
        model = Person
        fields = (
            'id',
            'url',
            'nomen',
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
            'entities',
            'common_name',
            'full_name',
            'formal_name',
            'first_name',
            'last_name',
            'nick_name',
            'permissions',
            'user',
        )
        # fields = '__all__'
        read_only_fields = [
            'picture',
            'common_name',
            'full_name',
            'formal_name',
            'first_name',
            'last_name',
            'nick_name',
        ]


class RoundSerializer(serializers.ModelSerializer):

    permissions = DRYPermissionsField()

    class Meta:
        model = Round
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'kind',
            'start_date',
            'end_date',
            'num',
            # 'mt',
            'session',
            'performances',
            'slots',
            'permissions',
        )


class ScoreSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Score
        fields = [
            'id',
            'url',
            'nomen',
            'status',
            'category',
            'kind',
            'points',
            'original',
            'violation',
            'penalty',
            'is_flagged',
            'song',
            'person',
            'permissions',
        ]


class SessionSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Session
        fields = (
            'id',
            'url',
            'nomen',
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
            'assignments',
            'rounds',
            'permissions',
        )


class SubmissionSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Submission
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'title',
            'arranger',
            'source',
            'is_medley',
            'is_parody',
            'performer',
            'permissions',
        )


class SlotSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Slot
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'num',
            'round',
            'performance',
            'photo',
            'arrive',
            'depart',
            'backstage',
            'onstage',
            'permissions',
        )


class SongSerializer(serializers.ModelSerializer):

    permissions = DRYPermissionsField()

    class Meta:
        model = Song
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'num',
            'submission',
            'performance',
            'scores',
            'songscore',
            'permissions',
        )


class SongScoreSerializer(serializers.ModelSerializer):

    permissions = DRYPermissionsField()

    class Meta:
        model = SongScore
        fields = (
            'id',
            'url',
            'mus_points',
            'prs_points',
            'sng_points',
            'total_points',
            'mus_score',
            'prs_score',
            'sng_score',
            'total_score',
            'permissions',
        )


class VenueSerializer(serializers.ModelSerializer):
    timezone = TimezoneField(allow_null=True)

    permissions = DRYPermissionsField()

    class Meta:
        model = Venue
        fields = (
            'id',
            'url',
            'nomen',
            'name',
            'location',
            'city',
            'state',
            'airport',
            'timezone',
            'conventions',
            'permissions',
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'url',
            'username',
            'is_active',
            'is_staff',
            'person',
        ]
