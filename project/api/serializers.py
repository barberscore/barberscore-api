# Third-Party
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_json_api import serializers

# Local
from .fields import TimezoneField
from .models import (
    Appearance,
    Assignment,
    Award,
    Chart,
    Contest,
    Contestant,
    Convention,
    Competitor,
    Entry,
    Grantor,
    Grid,
    Group,
    Member,
    Office,
    Officer,
    Organization,
    Panelist,
    Participant,
    Person,
    Repertory,
    Round,
    Score,
    Session,
    Song,
    User,
    Venue,
)


class AppearanceSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Appearance
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'num',
            'draw',
            'actual_start',
            'actual_finish',
            'rank',
            'mus_points',
            'per_points',
            'sng_points',
            'tot_points',
            'mus_score',
            'per_score',
            'sng_score',
            'tot_score',
            'round',
            'competitor',
            'grid',
            'songs',
            'permissions',
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
            'category',
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
            'gender',
            'level',
            'season',
            'is_primary',
            'is_invitational',
            'is_manual',
            'rounds',
            'threshold',
            'minimum',
            'advance',
            'footnote',
            'description',
            'notes',
            'is_improved',
            'is_multi',
            'is_rep_qualifies',
            'age',
            'size',
            'size_range',
            'scope',
            'scope_range',
            'organization',
            'parent',
            'children',
            'contests',
            'permissions',
        )


class ChartSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Chart
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'title',
            'arrangers',
            'composers',
            'lyricists',
            'description',
            'notes',
            'img',
            'holders',
            'repertories',
            'songs',
            'permissions',
        )
        read_only_fields = [
            'img',
        ]


class ContestSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Contest
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'champion',
            'session',
            'award',
            'contestants',
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
            'rank',
            'mus_points',
            'per_points',
            'sng_points',
            'tot_points',
            'mus_score',
            'per_score',
            'sng_score',
            'tot_score',
            'entry',
            'contest',
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
            'is_archived',
            'season',
            'panel',
            'year',
            'open_date',
            'close_date',
            'start_date',
            'end_date',
            'location',
            'description',
            'venue',
            'organization',
            'assignments',
            'sessions',
            'grantors',
            'permissions',
        )

    def validate(self, data):
        return data


class CompetitorSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Competitor
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'is_archived',
            'rank',
            'mus_points',
            'per_points',
            'sng_points',
            'tot_points',
            'mus_score',
            'per_score',
            'sng_score',
            'tot_score',
            'session',
            'group',
            'entry',
            'appearances',
            'permissions',
        )


class EntrySerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    logs = serializers.SerializerMethodField()
    competitor = serializers.PrimaryKeyRelatedField(
        queryset=Competitor.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Entry
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'is_archived',
            'is_evaluation',
            'is_private',
            'draw',
            'seed',
            'prelim',
            'directors',
            'representing',
            'rank',
            'mus_points',
            'per_points',
            'sng_points',
            'tot_points',
            'mus_score',
            'per_score',
            'sng_score',
            'tot_score',
            'session',
            'group',
            'competitor',
            'contestants',
            'participants',
            'permissions',
            'logs',
        )

    def get_logs(self, obj):
        output = []
        logs = StateLog.objects.for_(obj)
        for log in logs:
            transition = log.transition.title()
            if log.by:
                by = log.by.name
            else:
                by = '(Unknown)'
            timestamp = log.timestamp
            d = {
                'transition': transition,
                'by': by,
                'timestamp': timestamp,
            }
            output.append(d)
        return output

    def validate(self, data):
        """Check that the start is before the stop."""
        if data['is_private'] and data['contestants']:
            raise serializers.ValidationError("Can not be private and compete for an award.")
        return data


class GrantorSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Grantor
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'organization',
            'convention',
            'permissions',
        )


class GridSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Grid
        fields = [
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
            'start',
            'renditions',
            'round',
            'appearance',
            'competitor',
            'permissions',
        ]


class GroupSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    img = serializers.ImageField(use_url=True)

    class Meta:
        model = Group
        fields = [
            'id',
            'url',
            'nomen',
            'name',
            'status',
            'kind',
            'gender',
            'short_name',
            'code',
            'start_date',
            'end_date',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'img',
            'description',
            'bhs_id',
            'international',
            'district',
            'division',
            'chapter',
            'organization',
            'entries',
            'members',
            'repertories',
            'permissions',
        ]

        read_only_fields = [
            'img',
        ]


class MemberSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Member
        fields = [
            'id',
            'url',
            'nomen',
            'status',
            'part',
            'start_date',
            'end_date',
            'group',
            'person',
            'is_admin',
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
            'is_convention_manager',
            'is_session_manager',
            'is_scoring_manager',
            'is_organization_manager',
            'is_group_manager',
            'is_person_manager',
            'is_award_manager',
            'is_judge_manager',
            'is_chart_manager',
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
            'person',
            'organization',
            'permissions',
        ]

        validators = [
            UniqueTogetherValidator(
                queryset=Officer.objects.all(),
                fields=('person', 'office'),
                message='This person already holds this office.',
            )
        ]


class OrganizationSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Organization
        fields = [
            'id',
            'url',
            'nomen',
            'name',
            'status',
            'kind',
            'code',
            'start_date',
            'end_date',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'img',
            'description',
            'bhs_id',
            'org_sort',
            'parent',
            'children',
            'awards',
            'conventions',
            'groups',
            'officers',
            'permissions',
        ]

        read_only_fields = [
            'img',
        ]


class PanelistSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Panelist
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'num',
            'kind',
            'category',
            'round',
            'person',
            'scores',
            'permissions',
        )


class ParticipantSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Participant
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'part',
            'entry',
            'person',
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
            'first_name',
            'middle_name',
            'last_name',
            'nick_name',
            'status',
            'birth_date',
            'spouse',
            'location',
            'part',
            'website',
            'facebook',
            'twitter',
            'email',
            'address',
            'home_phone',
            'work_phone',
            'cell_phone',
            'airports',
            'img',
            'description',
            'bhs_id',
            'current_through',
            'full_name',
            'common_name',
            'sort_name',
            'assignments',
            'members',
            'officers',
            'panelists',
            'participants',
            'user',
            'permissions',
        )
        read_only_fields = [
            'common_name',
            'full_name',
            'sort_name',
            'img',
        ]


class RepertorySerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Repertory
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'group',
            'chart',
            'permissions',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Repertory.objects.all(),
                fields=('group', 'chart'),
                message='This chart already exists in your repertory.',
            )
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
            'session',
            'appearances',
            'panelists',
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
            'num',
            'points',
            'original',
            'violation',
            'penalty',
            'is_flagged',
            'song',
            'panelist',
            'permissions',
        ]


class SessionSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    bbscores_report = serializers.FileField(use_url=True)
    drcj_report = serializers.FileField(use_url=True)
    admins_report = serializers.FileField(use_url=True)
    actives_report = serializers.FileField(use_url=True)

    class Meta:
        model = Session
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'is_archived',
            'kind',
            'gender',
            'is_invitational',
            'description',
            'notes',
            'bbscores_report',
            'drcj_report',
            'admins_report',
            'actives_report',
            'num_rounds',
            'convention',
            'contests',
            'entries',
            'competitors',
            'rounds',
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
            'rank',
            'mus_points',
            'per_points',
            'sng_points',
            'tot_points',
            'mus_score',
            'per_score',
            'sng_score',
            'tot_score',
            'appearance',
            'chart',
            'scores',
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
    permissions = DRYPermissionsField()

    class Meta:
        model = User
        fields = [
            'id',
            'url',
            'email',
            'name',
            'is_active',
            'is_staff',
            'person',
            'permissions',
            'is_convention_manager',
            'is_session_manager',
            'is_scoring_manager',
            'is_organization_manager',
            'is_group_manager',
            'is_person_manager',
            'is_award_manager',
            'is_judge_manager',
            'is_chart_manager',
        ]
        read_only_fields = [
            'is_convention_manager',
            'is_session_manager',
            'is_scoring_manager',
            'is_organization_manager',
            'is_group_manager',
            'is_person_manager',
            'is_award_manager',
            'is_judge_manager',
            'is_chart_manager',
        ]


class StateLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = StateLog
        fields = '__all__'


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
        ]
