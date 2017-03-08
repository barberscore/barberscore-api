# Third-Party
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework_json_api import serializers

# Local
from .fields import (
    TimezoneField,
)

from .models import (
    Assignment,
    Award,
    Catalog,
    Contest,
    Contestant,
    ContestantPrivate,
    ContestPrivate,
    Convention,
    Entity,
    Host,
    Membership,
    Office,
    Officer,
    Performance,
    PerformancePrivate,
    Performer,
    PerformerPrivate,
    Person,
    Round,
    Score,
    Session,
    Slot,
    Song,
    SongPrivate,
    Submission,
    User,
    Venue,
)


class AssignmentSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Assignment
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'kind',
            'convention',
            'person',
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
            'size_range',
            'scope',
            'scope_range',
            'is_primary',
            'is_improved',
            'is_novice',
            'is_manual',
            'is_multi',
            'is_district_representative',
            'championship_rounds',
            'qualifier_rounds',
            'threshold',
            'minimum',
            'advance',
            'entity',
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
            'submissions',
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
            'award',
            'session',
            'contestants',
            'permissions',
        )


class ContestPrivateSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = ContestPrivate
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


class ContestantPrivateSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = ContestantPrivate
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
            'season',
            'kind',
            'panel',
            'risers',
            'year',
            'start_date',
            'end_date',
            'location',
            'venue',
            'entity',
            'hosts',
            'assignments',
            'sessions',
            'permissions',
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
            'kind',
            'age',
            'is_novice',
            'short_name',
            'long_name',
            'code',
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
            'parent',
            'children',
            'hosts',
            'conventions',
            'memberships',
            'performers',
            'awards',
            'permissions',
        ]
        read_only_fields = [
            'picture',
        ]


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
            'officers',
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
            'officers',
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


class PerformancePrivateSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = PerformancePrivate
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
            'picture',
            'men',
            'risers',
            'is_evaluation',
            'is_private',
            'seed',
            'prelim',
            'session',
            'entity',
            'tenor',
            'lead',
            'baritone',
            'bass',
            'director',
            'codirector',
            'performances',
            'contestants',
            'submissions',
            'permissions',
        )
        read_only_fields = [
            'picture',
        ]


class PerformerPrivateSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = PerformerPrivate
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
            'kind',
            'bhs_status',
            'birth_date',
            'start_date',
            'end_date',
            'dues_thru',
            'mon',
            'spouse',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            'common_name',
            'full_name',
            'formal_name',
            'first_name',
            'last_name',
            'nick_name',
            'assignments',
            'memberships',
            'permissions',
            'scores',
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
            'num',
            'num_songs',
            'start_date',
            'end_date',
            'ann_pdf',
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
            'start_date',
            'end_date',
            'num_rounds',
            'panel_size',
            'is_prelims',
            'cursor',
            'current',
            'primary',
            'scoresheet_pdf',
            # 'computed_rounds',
            'convention',
            'performers',
            'contests',
            'rounds',
            'permissions',
        )

        # read_only_fields = [
        #     'computed_rounds',
        # ]


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
            'location',
            'photo',
            'arrive',
            'depart',
            'backstage',
            'onstage',
            'round',
            'performance',
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
            'performance',
            'scores',
            'songprivate',
            'permissions',
        )


class SongPrivateSerializer(serializers.ModelSerializer):

    permissions = DRYPermissionsField()

    class Meta:
        model = SongPrivate
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


class SubmissionSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Submission
        fields = [
            'id',
            'url',
            'nomen',
            'status',
            'title',
            'bhs_catalog',
            'is_medley',
            'is_parody',
            'arrangers',
            'composers',
            'holders',
            'performer',
            'catalog',
            'permissions',
        ]


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
            'status',
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
            'email',
            'is_active',
            'is_staff',
            'person',
        ]


class OfficeCSVSerializer(serializers.ModelSerializer):

    status = serializers.CharField(source='get_status_display')
    kind = serializers.CharField(source='get_kind_display')

    class Meta:
        model = Office
        fields = [
            'id',
            'nomen',
            'name',
            'status',
            'kind',
            'short_name',
            'long_name',
        ]
