# Third-Party
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_json_api import serializers
from rest_framework_json_api.relations import ResourceRelatedField

# Local
from .fields import TimezoneField
from .models import Appearance
from .models import Assignment
from .models import Award
from .models import Chart
from .models import Competitor
from .models import Contest
from .models import Contestant
from .models import Convention
from .models import Entry
from .models import Grantor
from .models import Grid
from .models import Group
from .models import Member
from .models import Office
from .models import Officer
from .models import Panelist
from .models import Person
from .models import Repertory
from .models import Round
from .models import Score
from .models import Session
from .models import Song
from .models import User
from .models import Venue


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
            'variance_report',
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
            'group',
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
            'image',
            'holders',
            'repertories',
            'songs',
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
            'group',
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
            'is_evaluation',
            'is_private',
            'draw',
            'seed',
            'prelim',
            'directors',
            'mos',
            'representing',
            'rank',
            'description',
            'notes',
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
        # if data['is_private'] and data['contestants']:
        #     raise serializers.ValidationError("Can not be private and compete for an award.")
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
            'group',
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


# class GroupMemberField(ResourceRelatedField):
#     def get_queryset(self, request):
#         print('dfd')
#         qs = super().get_queryset(request)
#         qs = qs.filter(
#             status__gt=0,
#         )
#         return qs


class GroupSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    members = ResourceRelatedField(
        queryset=Member.lows,
        many=True
    )

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
            'is_senior',
            'code',
            'start_date',
            'end_date',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'image',
            'description',
            'bhs_id',
            'international',
            'district',
            'division',
            'chapter',
            'parent',
            'children',
            'entries',
            'members',
            'tree_sort',
            'repertories',
            'permissions',
        ]


class MemberSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Member
        fields = [
            'id',
            'url',
            'status',
            'part',
            'group',
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
            'code',
            'is_convention_manager',
            'is_session_manager',
            'is_scoring_manager',
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
            'group',
            'permissions',
        ]

        validators = [
            UniqueTogetherValidator(
                queryset=Officer.objects.all(),
                fields=('person', 'office'),
                message='This person already holds this office.',
            )
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
            'image',
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
            # 'user',
            'permissions',
        )
        read_only_fields = [
            'common_name',
            'full_name',
            'sort_name',
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

    class Meta:
        model = Session
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'kind',
            'gender',
            'is_invitational',
            'description',
            'notes',
            'bbscores_report',
            'drcj_report',
            'admins_report',
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
            'is_staff',
            # 'person',
            'permissions',
            'is_convention_manager',
            'is_session_manager',
            'is_scoring_manager',
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
