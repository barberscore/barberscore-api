# Third-Party
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework_json_api import serializers
from rest_framework.validators import UniqueTogetherValidator
from django_fsm_log.models import StateLog

# Local
from .fields import (
    TimezoneField,
)

from .models import (
    Appearance,
    Assignment,
    Award,
    Chart,
    Contest,
    Contestant,
    Convention,
    Entity,
    Entry,
    Member,
    Office,
    Officer,
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

    class Meta:
        model = Appearance
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'num',
            'actual_start',
            'actual_finish',
            'round',
            'entry',
            'slot',
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
            'category',
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
            'age',
            'season',
            'size',
            'size_range',
            'scope',
            'scope_range',
            'is_qualifier',
            'is_primary',
            'is_improved',
            'is_novice',
            'is_manual',
            'is_multi',
            'is_district_representative',
            'rounds',
            'threshold',
            'minimum',
            'advance',
            'entity',
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
            'is_qualifier',
            'kind',
            'award',
            'session',
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
            'kind',
            'panel',
            'risers',
            'year',
            'open_date',
            'close_date',
            'start_date',
            'end_date',
            'location',
            'venue',
            'entity',
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
            'description',
            'parent',
            # 'children',
            'bhs_id',
            'conventions',
            'members',
            'entries',
            'awards',
            'repertories',
            'officers',
            'permissions',
        ]


class EntrySerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    logs = serializers.SerializerMethodField()
    class Meta:
        model = Entry
        fields = (
            'id',
            'url',
            'nomen',
            'status',
            'men',
            'risers',
            'is_evaluation',
            'is_private',
            'is_mt',
            'seed',
            'prelim',
            'session',
            'entity',
            'representing',
            'director',
            'codirector',
            'participants',
            'appearances',
            'contestants',
            'permissions',
            'logs',
        )
    def get_logs(self, obj):
        # TODO HACKY!!!
        qs = StateLog.objects.for_(obj).values(
            'timestamp',
            'transition',
            'by',
        )
        for q in qs:
            if q['by']:
                email = User.objects.get(id=q['by'].hex).person.nomen
                q['by'] = email
        return qs


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
            'entity',
            'person',
            'participants',
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
            'person',
            'entity',
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
            'category',
            'kind',
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
            'entry',
            'member',
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
            'bhs_id',
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
            'description',
            'common_name',
            'full_name',
            'formal_name',
            'first_name',
            'last_name',
            'nick_name',
            'representing',
            'international',
            'district',
            'division',
            'chapter',
            'assignments',
            'members',
            'officers',
            'permissions',
            'panelists',
            'user',
        )
        # fields = '__all__'
        read_only_fields = [
            'common_name',
            'full_name',
            'formal_name',
            'first_name',
            'last_name',
            'nick_name',
            'international',
            'district',
            'division',
            'chapter',
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
            'entity',
            'chart',
            'permissions',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Repertory.objects.all(),
                fields=('entity', 'chart'),
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
            'num_songs',
            'start_date',
            'end_date',
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
            'age',
            'is_invitational',
            'start_date',
            'end_date',
            'num_rounds',
            'panel_size',
            'cursor',
            'current',
            'primary',
            'scoresheet',
            # 'computed_rounds',
            'convention',
            'entries',
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
            'appearance',
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
            'long_name',
        ]
