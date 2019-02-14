
# Third-Party
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_json_api import serializers

# Local
from .fields import TimezoneField
from .models import Appearance
from .models import Assignment
from .models import Award
from .models import Chart
from .models import Competitor
from .models import Contest
from .models import Contender
from .models import Contestant
from .models import Convention
from .models import Entry
from .models import Grid
from .models import Group
from .models import Member
from .models import Office
from .models import Officer
from .models import Outcome
from .models import Panelist
from .models import Person
from .models import Repertory
from .models import Round
from .models import Score
from .models import Session
from .models import Song
from .models import User
from .models import Venue


class StateLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = StateLog
        fields = (
            'timestamp',
            'object_id',
            'transition',
            'description',
            'by',
        )


class AppearanceSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    included_serializers = {
        'songs': 'api.serializers.SongSerializer',
    }

    class Meta:
        model = Appearance
        fields = (
            'id',
            'url',
            'status',
            'num',
            'draw',
            'actual_start',
            'actual_finish',
            'pos',
            'rank',
            'mus_points',
            'per_points',
            'sng_points',
            'tot_points',
            'mus_score',
            'per_score',
            'sng_score',
            'tot_score',
            'mus_rank',
            'per_rank',
            'sng_rank',
            'tot_rank',
            'variance_report',
            'round',
            'competitor',
            'grid',
            'songs',
            'permissions',
        )

    class JSONAPIMeta:
        included_resources = [
            'songs',
        ]



class AssignmentSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    # included_serializers = {
    #     'person': 'api.serializers.PersonSerializer',
    #     'convention': 'api.serializers.ConventionSerializer',
    # }

    class Meta:
        model = Assignment
        fields = (
            'id',
            'url',
            'status',
            'kind',
            'category',
            'convention',
            'person',
            'permissions',
        )

    # class JSONAPIMeta:
    #     included_resources = [
    #         'convention',
    #         'person',
    #     ]

class AwardSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Award
        fields = (
            'id',
            'url',
            'name',
            'status',
            'kind',
            'gender',
            'level',
            'season',
            'num_rounds',
            'threshold',
            'minimum',
            'advance',
            'spots',
            'description',
            'notes',
            'age',
            'size',
            'size_range',
            'scope',
            'scope_range',
            'tree_sort',
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


class CompetitorSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    included_serializers = {
        'appearances': 'api.serializers.AppearanceSerializer',
    }

    class Meta:
        model = Competitor
        fields = (
            'id',
            'url',
            'status',
            'is_multi',
            'pos',
            'rank',
            'mus_points',
            'per_points',
            'sng_points',
            'tot_points',
            'mus_score',
            'per_score',
            'sng_score',
            'tot_score',
            'mus_rank',
            'per_rank',
            'sng_rank',
            'tot_rank',
            'csa',
            'session',
            'group',
            'entry',
            'appearances',
            'permissions',
        )

    class JSONAPIMeta:
        included_resources = [
            'appearances',
        ]



class ContestSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    included_serializers = {
        'contestants': 'api.serializers.ContestantSerializer',
    }

    class Meta:
        model = Contest
        fields = (
            'id',
            'url',
            'status',
            'num',
            'result',
            'group',
            'session',
            'award',
            'contestants',
            'permissions',
        )

    class JSONAPIMeta:
        included_resources = [
            'contestants',
        ]


class ContenderSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Contender
        fields = (
            'id',
            'url',
            'status',
            'mus_points',
            'per_points',
            'sng_points',
            'tot_points',
            'mus_score',
            'per_score',
            'sng_score',
            'tot_score',
            'mus_rank',
            'per_rank',
            'sng_rank',
            'tot_rank',
            'appearance',
            'outcome',
            'permissions',
        )


class ContestantSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Contestant
        fields = (
            'id',
            'url',
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
            'mus_rank',
            'per_rank',
            'sng_rank',
            'tot_rank',
            'entry',
            'contest',
            'permissions',
        )


class ConventionSerializer(serializers.ModelSerializer):
    timezone = TimezoneField(allow_null=True)
    permissions = DRYPermissionsField()
    included_serializers = {
        'sessions': 'api.serializers.SessionSerializer',
        'assignments': 'api.serializers.AssignmentSerializer',
        'venue': 'api.serializers.VenueSerializer',
        # 'person': 'api.serializers.PersonSerializer',
    }

    class Meta:
        model = Convention
        fields = (
            'id',
            'url',
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
            'timezone',
            'image',
            'description',
            'venue',
            'group',
            'assignments',
            'sessions',
            'permissions',
        )

    class JSONAPIMeta:
        included_resources = [
            'sessions',
            'assignments',
            # 'assignments.person',
        ]


    def validate(self, data):
        return data


class EntrySerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    # competitor = serializers.PrimaryKeyRelatedField(
    #     queryset=Competitor.objects.all(),
    #     required=False,
    #     allow_null=True,
    # )
    # logs = StateLogSerializer(many=True)
    statelogs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    included_serializers = {
        'contestants': 'api.serializers.ContestantSerializer',
        'statelogs': 'api.serializers.StateLogSerializer',
        'group': 'api.serializers.GroupSerializer',
    }

    class Meta:
        model = Entry
        fields = (
            'id',
            'url',
            'status',
            'is_evaluation',
            'is_private',
            'is_mt',
            'draw',
            'seed',
            'prelim',
            'participants',
            'pos',
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
            'mus_rank',
            'per_rank',
            'sng_rank',
            'tot_rank',
            'session',
            'group',
            # 'competitor',
            'contestants',
            'permissions',
            'statelogs',
        )

    class JSONAPIMeta:
        included_resources = [
            'appearances',
            'contestants',
        ]

    def validate(self, data):
        """Check that the start is before the stop."""
        # if data['is_private'] and data['contestants']:
        #     raise serializers.ValidationError("Can not be private and compete for an award.")
        return data


class GridSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Grid
        fields = [
            'id',
            'url',
            'status',
            'period',
            'num',
            'location',
            'photo',
            'arrive',
            'depart',
            'backstage',
            'onstage',
            'start',
            'renditions',
            'venue',
            'round',
            'appearance',
            'permissions',
        ]


class GroupSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    included_serializers = {
        'repertories': 'api.serializers.RepertorySerializer',
        'members': 'api.serializers.MemberSerializer',
        'officers': 'api.serializers.OfficerSerializer',
        'competitors': 'api.serializers.CompetitorSerializer',
        'entries': 'api.serializers.EntrySerializer',
    }

    class Meta:
        model = Group
        fields = [
            'id',
            'url',
            'name',
            'status',
            'kind',
            'gender',
            'is_senior',
            'is_youth',
            'division',
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
            'chapter',
            'tree_sort',
            'parent',
            'children',
            'awards',
            'competitors',
            'conventions',
            'entries',
            'members',
            'officers',
            'repertories',
            'permissions',
        ]

    class JSONAPIMeta:
        included_resources = [
            'repertories',
            'members',
            'officers',
            'competitors',
            'entries',
        ]

    # def to_representation(self, instance):
    #     if instance.kind <= 30:
    #         self.fields.pop('members')
    #     return super().to_representation(instance)


class MemberSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Member
        fields = [
            'id',
            'url',
            'status',
            'part',
            'start_date',
            'end_date',
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
            'name',
            'status',
            'kind',
            'code',
            'is_convention_manager',
            'is_session_manager',
            'is_round_manager',
            'is_scoring_manager',
            'is_group_manager',
            'is_person_manager',
            'is_award_manager',
            'is_officer_manager',
            'is_chart_manager',
            'is_assignment_manager',
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


class OutcomeSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Outcome
        fields = (
            'id',
            'url',
            'status',
            'round',
            'contest',
            'num',
            'name',
            'legacy_num',
            'legacy_name',
            'permissions',
        )


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

class PersonSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    included_serializers = {
        'assignments': 'api.serializers.AssignmentSerializer',
        'members': 'api.serializers.MemberSerializer',
        'officers': 'api.serializers.OfficerSerializer',
        'panelists': 'api.serializers.PanelistSerializer',
    }

    class Meta:
        model = Person
        fields = (
            'id',
            'url',
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
            'current_status',
            'current_district',
            'full_name',
            'common_name',
            'sort_name',
            'assignments',
            'members',
            'officers',
            'panelists',
            'user',
            'permissions',
        )
        read_only_fields = [
            'common_name',
            'full_name',
            'sort_name',
        ]

    class JSONAPIMeta:
        included_resources = [
            'assignments',
            'members',
            'officers',
            'panelists',
        ]


class RepertorySerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Repertory
        fields = (
            'id',
            'url',
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
    included_serializers = {
        'appearances': 'api.serializers.AppearanceSerializer',
        'members': 'api.serializers.MemberSerializer',
        'grids': 'api.serializers.GridSerializer',
        'outcomes': 'api.serializers.OutcomeSerializer',
    }

    class Meta:
        model = Round
        fields = (
            'id',
            'url',
            'status',
            'kind',
            'num',
            'spots',
            'date',
            'footnotes',
            'oss',
            'sa',
            'session',
            'appearances',
            'panelists',
            'grids',
            'outcomes',
            'permissions',
        )

    class JSONAPIMeta:
        included_resources = [
            'appearances',
            'members',
            'grids',
            'outcomes',
        ]


class ScoreSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Score
        fields = [
            'id',
            'url',
            'status',
            'category',
            'kind',
            'num',
            'points',
            'song',
            'panelist',
            'permissions',
        ]


class SessionSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    included_serializers = {
        'contests': 'api.serializers.ContestSerializer',
        'entries': 'api.serializers.EntrySerializer',
        'rounds': 'api.serializers.RoundSerializer',
    }

    class Meta:
        model = Session
        fields = (
            'id',
            'url',
            'status',
            'kind',
            'is_invitational',
            'footnotes',
            'description',
            'notes',
            'oss',
            'sa',
            'num_rounds',
            'competitors',
            'convention',
            'contests',
            'entries',
            'rounds',
            'permissions',
        )

    class JSONAPIMeta:
        included_resources = [
            'contests',
            'entries',
            'rounds',
        ]


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
            'status',
            'legacy_chart',
            'num',
            'penalties',
            'rank',
            'mus_points',
            'per_points',
            'sng_points',
            'tot_points',
            'mus_score',
            'per_score',
            'sng_score',
            'tot_score',
            'mus_rank',
            'per_rank',
            'sng_rank',
            'tot_rank',
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

    class Meta:
        model = Venue
        fields = (
            'id',
            'url',
            'name',
            'status',
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
            'username',
            'is_active',
            'is_staff',
            'person',
            'is_convention_manager',
            'is_session_manager',
            'is_round_manager',
            'is_scoring_manager',
            'is_group_manager',
            'is_person_manager',
            'is_award_manager',
            'is_officer_manager',
            'is_chart_manager',
            'is_assignment_manager',
            'permissions',
        ]
        read_only_fields = [
            'is_convention_manager',
            'is_session_manager',
            'is_round_manager',
            'is_scoring_manager',
            'is_group_manager',
            'is_person_manager',
            'is_award_manager',
            'is_officer_manager',
            'is_chart_manager',
            'is_assignment_manager',
        ]
