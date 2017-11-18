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
    Entry,
    Grantor,
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
    Slot,
    Song,
    User,
    Venue,
)


class AppearanceSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    # included_serializers = {
    #     'songs': 'api.serializers.SongSerializer',
    #     'slot': 'api.serializers.SlotSerializer',
    # }
    #
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
            'var_pdf',
            'round',
            'entry',
            'slot',
            'songs',
            'permissions',
        )
    # class JSONAPIMeta:
    #     included_resources = [
    #         'songs',
    #         'slot',
    #     ]


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
    # included_serializers = {
    #     'children': 'api.serializers.AwardSerializer',
    #     'contests': 'api.serializers.ContestSerializer',
    # }

    class Meta:
        model = Award
        fields = (
            'id',
            'url',
            'nomen',
            'name',
            'status',
            'kind',
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
    # class JSONAPIMeta:
    #     included_resources = [
    #         'children',
    #         'contests',
    #     ]


class ChartSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    # included_serializers = {
    #     'repertories': 'api.serializers.RepertorySerializer',
    #     'songs': 'api.serializers.SongSerializer',
    # }

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
    # class JSONAPIMeta:
    #     included_resources = [
    #         'repertories',
    #         'songs',
    #     ]


class ContestSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    # included_serializers = {
    #     'contestants': 'api.serializers.ContestantSerializer',
    # }

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
    # class JSONAPIMeta:
    #     included_resources = [
    #         'contestants',
    #     ]


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
    # included_serializers = {
    #     'sessions': 'api.serializers.SessionSerializer',
    #     'assignments': 'api.serializers.AssignmentSerializer',
    # }

    class Meta:
        model = Convention
        fields = (
            'id',
            'url',
            'nomen',
            'name',
            'status',
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
        # if data['open_date'] > data['close_date']:
        #     raise serializers.ValidationError("Session open must be before close")
        return data

    # class JSONAPIMeta:
    #     included_resources = [
    #         'sessions',
    #         'assignments',
    #     ]


class EntrySerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    # included_serializers = {
    #     'appearances': 'api.serializers.AppearanceSerializer',
    #     'contestants': 'api.serializers.ContestantSerializer',
    #     'participants': 'api.serializers.ParticipantSerializer',
    # }
    logs = serializers.SerializerMethodField()
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
            'rank',
            'directors',
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
            'appearances',
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
    # class JSONAPIMeta:
    #     included_resources = [
    #         'appearances',
    #         'contestants',
    #         'participants',
    #     ]


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


class GroupSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    # included_serializers = {
    #     'entries': 'api.serializers.EntrySerializer',
    #     'members': 'api.serializers.MemberSerializer',
    #     'repertories': 'api.serializers.RepertorySerializer',
    # }
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
            'org_sort',
            'organization',
            'entries',
            'members',
            'repertories',
            'permissions',
        ]

        read_only_fields = [
            'img',
        ]
    # class JSONAPIMeta:
    #     included_resources = [
    #         'entries',
    #         'members',
    #         'repertories',
    #     ]


class MemberSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    # included_serializers = {
    #     'participants': 'api.serializers.ParticipantSerializer',
    # }

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
    # class JSONAPIMeta:
    #     included_resources = [
    #         'participants',
    #     ]


class OfficeSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    # included_serializers = {
    #     'officers': 'api.serializers.OfficerSerializer',
    # }

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
    # class JSONAPIMeta:
    #     included_resources = [
    #         'officers',
    #     ]


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
    # included_serializers = {
    #     'awards': 'api.serializers.AwardSerializer',
    #     'conventions': 'api.serializers.ConventionSerializer',
    #     'officers': 'api.serializers.OfficerSerializer',
    #     'children': 'api.serializers.OrganizationSerializer',
    # }

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
    # class JSONAPIMeta:
    #     included_resources = [
    #         'awards',
    #         'conventions',
    #         'officers',
    #         'children',
    #     ]


class PanelistSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    # included_serializers = {
    #     'scores': 'api.serializers.ScoreSerializer',
    # }

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
    # class JSONAPIMeta:
    #     included_resources = [
    #         'scores',
    #     ]


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
    # included_serializers = {
    #     'assignments': 'api.serializers.AssignmentSerializer',
    #     'members': 'api.serializers.MemberSerializer',
    #     'officers': 'api.serializers.OfficerSerializer',
    #     'panelists': 'api.serializers.PanelistSerializer',
    #     'user': 'api.serializers.UserSerializer',
    # }

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
            # 'phone',
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
        # fields = '__all__'
        read_only_fields = [
            'common_name',
            'full_name',
            'sort_name',
            'img',
        ]
    # class JSONAPIMeta:
    #     included_resources = [
    #         'assignments',
    #         'members',
    #         'officers',
    #         'panelists',
    #         'user',
    #     ]


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
    # included_serializers = {
    #     'appearances': 'api.serializers.AppearanceSerializer',
    #     'panelists': 'api.serializers.PanelistSerializer',
    #     'slots': 'api.serializers.SlotSerializer',
    # }

    class Meta:
        model = Round
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'kind',
            'num',
            'ann_pdf',
            'session',
            'appearances',
            'panelists',
            'slots',
            'permissions',
        )
    # class JSONAPIMeta:
    #     included_resources = [
    #         'appearances',
    #         'panelists',
    #         'slots',
    #     ]


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
    # included_serializers = {
    #     'contests': 'api.serializers.ContestSerializer',
    #     'entries': 'api.serializers.EntrySerializer',
    #     'rounds': 'api.serializers.RoundSerializer',
    # }

    class Meta:
        model = Session
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'is_archived',
            'kind',
            'is_invitational',
            'scoresheet',
            'bbscores',
            'drcj_report',
            'admin_emails',
            'num_rounds',
            'convention',
            'contests',
            'entries',
            'rounds',
            'permissions',
        )
    # class JSONAPIMeta:
    #     included_resources = [
    #         'contests',
    #         'entries',
    #         'rounds',
    #     ]


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
            'appearance',
            'permissions',
        )


class SongSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    # included_serializers = {
    #     'scores': 'api.serializers.ScoreSerializer',
    # }

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
    # class JSONAPIMeta:
    #     included_resources = [
    #         'scores',
    #     ]


class VenueSerializer(serializers.ModelSerializer):
    timezone = TimezoneField(allow_null=True)
    permissions = DRYPermissionsField()
    # included_serializers = {
    #     'conventions': 'api.serializers.ConventionSerializer',
    # }

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
    # class JSONAPIMeta:
    #     included_resources = [
    #         'conventions',
    #     ]


class UserSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = User
        fields = [
            'id',
            'url',
            'email',
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
