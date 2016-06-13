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


class RankField(serializers.Field):
    def get_attribute(self, obj):
        # We pass the object instance onto `to_representation`,
        # not just the field attribute.
        return obj

    def to_representation(self, obj):
        # for read functionality
        if self.context['request'].user.is_staff:
            return obj.rank
        if obj.status == obj.STATUS.published:
            return obj.rank
        else:
            return None

    def to_internal_value(self, data):
        # for write functionality
        # check if data is valid and if not raise ValidationError
        return data


class SlotField(serializers.Field):
    def get_attribute(self, obj):
        # We pass the object instance onto `to_representation`,
        # not just the field attribute.
        return obj

    def to_representation(self, obj):
        # for read functionality
        if self.context['request'].user.is_staff:
            return obj.slot
        if obj.status >= obj.STATUS.published:
            return obj.slot
        else:
            return None

    def to_internal_value(self, data):
        # for write functionality
        # check if data is valid and if not raise ValidationError
        return data


class AdvancingField(serializers.Field):
    def get_attribute(self, obj):
        # We pass the object instance onto `to_representation`,
        # not just the field attribute.
        return obj

    def to_representation(self, obj):
        # for read functionality
        if self.context['request'].user.is_staff:
            return obj.is_advancing
        if obj.status == obj.STATUS.published:
            return obj.is_advancing
        else:
            return None

    def to_internal_value(self, data):
        # for write functionality
        # check if data is valid and if not raise ValidationError
        return data


class ChampionField(serializers.Field):
    def get_attribute(self, obj):
        # We pass the object instance onto `to_representation`,
        # not just the field attribute.
        return obj

    def to_representation(self, obj):
        # for read functionality
        if self.context['request'].user.is_staff:
            return obj.champion
        if obj.status == obj.STATUS.published:
            return obj.champion
        else:
            return None

    def to_internal_value(self, data):
        # for write functionality
        # check if data is valid and if not raise ValidationError
        return data


class MusPointsField(serializers.Field):
    def get_attribute(self, obj):
        # We pass the object instance onto `to_representation`,
        # not just the field attribute.
        return obj

    def to_representation(self, obj):
        # for read functionality
        if self.context['request'].user.is_staff:
            return obj.mus_points
        if obj.status == obj.STATUS.published:
            return obj.mus_points
        else:
            return None

    def to_internal_value(self, data):
        # for write functionality
        # check if data is valid and if not raise ValidationError
        return data


class PrsPointsField(serializers.Field):
    def get_attribute(self, obj):
        # We pass the object instance onto `to_representation`,
        # not just the field attribute.
        return obj

    def to_representation(self, obj):
        # for read functionality
        if self.context['request'].user.is_staff:
            return obj.prs_points
        if obj.status == obj.STATUS.published:
            return obj.prs_points
        else:
            return None

    def to_internal_value(self, data):
        # for write functionality
        # check if data is valid and if not raise ValidationError
        return data


class SngPointsField(serializers.Field):
    def get_attribute(self, obj):
        # We pass the object instance onto `to_representation`,
        # not just the field attribute.
        return obj

    def to_representation(self, obj):
        # for read functionality
        if self.context['request'].user.is_staff:
            return obj.sng_points
        if obj.status == obj.STATUS.published:
            return obj.sng_points
        else:
            return None

    def to_internal_value(self, data):
        # for write functionality
        # check if data is valid and if not raise ValidationError
        return data


class TotalPointsField(serializers.Field):
    def get_attribute(self, obj):
        # We pass the object instance onto `to_representation`,
        # not just the field attribute.
        return obj

    def to_representation(self, obj):
        # for read functionality
        if self.context['request'].user.is_staff:
            return obj.total_points
        if obj.status == obj.STATUS.published:
            return obj.total_points
        else:
            return None

    def to_internal_value(self, data):
        # for write functionality
        # check if data is valid and if not raise ValidationError
        return data


class MusScoreField(serializers.Field):
    def get_attribute(self, obj):
        # We pass the object instance onto `to_representation`,
        # not just the field attribute.
        return obj

    def to_representation(self, obj):
        # for read functionality
        if self.context['request'].user.is_staff:
            return obj.mus_score
        if obj.status == obj.STATUS.published:
            return obj.mus_score
        else:
            return None

    def to_internal_value(self, data):
        # for write functionality
        # check if data is valid and if not raise ValidationError
        return data


class PrsScoreField(serializers.Field):
    def get_attribute(self, obj):
        # We pass the object instance onto `to_representation`,
        # not just the field attribute.
        return obj

    def to_representation(self, obj):
        # for read functionality
        if self.context['request'].user.is_staff:
            return obj.prs_score
        if obj.status == obj.STATUS.published:
            return obj.prs_score
        else:
            return None

    def to_internal_value(self, data):
        # for write functionality
        # check if data is valid and if not raise ValidationError
        return data


class SngScoreField(serializers.Field):
    def get_attribute(self, obj):
        # We pass the object instance onto `to_representation`,
        # not just the field attribute.
        return obj

    def to_representation(self, obj):
        # for read functionality
        if self.context['request'].user.is_staff:
            return obj.sng_score
        if obj.status == obj.STATUS.published:
            return obj.sng_score
        else:
            return None

    def to_internal_value(self, data):
        # for write functionality
        # check if data is valid and if not raise ValidationError
        return data


class TotalScoreField(serializers.Field):
    def get_attribute(self, obj):
        # We pass the object instance onto `to_representation`,
        # not just the field attribute.
        return obj

    def to_representation(self, obj):
        # for read functionality
        if self.context['request'].user.is_staff:
            return obj.total_score
        if obj.status == obj.STATUS.published:
            return obj.total_score
        else:
            return None

    def to_internal_value(self, data):
        # for write functionality
        # check if data is valid and if not raise ValidationError
        return data


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
    champion = ChampionField()

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
    rank = RankField()
    mus_points = MusPointsField()
    prs_points = PrsPointsField()
    sng_points = SngPointsField()
    total_points = TotalPointsField()
    mus_score = MusScoreField()
    prs_score = PrsScoreField()
    sng_score = SngScoreField()
    total_score = TotalScoreField()

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
    slot = SlotField()
    rank = RankField()
    mus_points = MusPointsField()
    prs_points = PrsPointsField()
    sng_points = SngPointsField()
    total_points = TotalPointsField()
    mus_score = MusScoreField()
    prs_score = PrsScoreField()
    sng_score = SngScoreField()
    total_score = TotalScoreField()

    class Meta:
        model = Performance
        fields = (
            'id',
            'url',
            'name',
            'status',
            'slot',
            'is_advancing',
            'rank',
            'scheduled',
            'actual',
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
            'songs',
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


class PerformerSerializer(serializers.ModelSerializer):
    rank = RankField()
    mus_points = MusPointsField()
    prs_points = PrsPointsField()
    sng_points = SngPointsField()
    total_points = TotalPointsField()
    mus_score = MusScoreField()
    prs_score = PrsScoreField()
    sng_score = SngScoreField()
    total_score = TotalScoreField()

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
            'primary',
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
    mus_points = MusPointsField()
    prs_points = PrsPointsField()
    sng_points = SngPointsField()
    total_points = TotalPointsField()
    mus_score = MusScoreField()
    prs_score = PrsScoreField()
    sng_score = SngScoreField()
    total_score = TotalScoreField()

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
