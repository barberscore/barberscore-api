import pytz
from django.core.exceptions import ValidationError
# Third-Party
from rest_framework import serializers

# Local

from .models import Assignment
from .models import Contest
from .models import Entry
from .models import Session


class TimezoneField(serializers.Field):
    def to_representation(self, obj):
        return str(obj)

    def to_internal_value(self, data):
        try:
            return pytz.timezone(str(data))
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValidationError('Unknown timezone')

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = [
            'id',
            'get_kind_display',
            'get_category_display',
            'person_id',
            'name',
            'first_name',
            'last_name',
            'get_district_display',
            'email',
            'cell_phone',
            'bhs_id',
            'image_id',
        ]


        read_only_fields = [
        ]


class ContestListSerializer(serializers.ListSerializer):

    """Serializer to filter the active system, which is a boolen field in
       System Model. The value argument to to_representation() method is
      the model instance"""

    def to_representation(self, data):
        data = data.filter(
            entries__isnull=False,
        )
        return super().to_representation(data)

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        list_serializer_class = ContestListSerializer
        fields = [
            'id',
            'award_id',
            'name',
            'get_level_display',
            # 'entries',
            'tree_sort',
        ]


class EntryListSerializer(serializers.ListSerializer):

    """Serializer to filter the active system, which is a boolen field in
       System Model. The value argument to to_representation() method is
      the model instance"""

    def to_representation(self, data):
        data = data.filter(
            status=Entry.STATUS.approved,
        )
        return super().to_representation(data)


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        list_serializer_class = EntryListSerializer
        fields = [
            'id',
            'get_status_display',
            'is_evaluation',
            'is_private',
            'notes',

            'is_mt',
            'draw',
            'prelim',
            'base',

            'participants',
            'chapters',
            'pos',
            'area',

            'group_id',
            'name',
            'get_kind_display',
            'get_gender_display',
            'get_district_display',
            'get_division_display',
            'bhs_id',
            'code',
            'is_senior',
            'is_youth',
            'image_id',

            'description',

            'owners',
            'session',
        ]
        read_only_fields = [
            'nomen',
            'image_id',
        ]


class SessionSerializer(serializers.ModelSerializer):
    contests = ContestSerializer(many=True)
    entries = EntrySerializer(many=True)
    assignments = AssignmentSerializer(many=True)
    timezone = TimezoneField()

    class Meta:
        model = Session
        fields = [
            'id',
            'get_status_display',
            'get_kind_display',
            'num_rounds',
            'is_invitational',
            'nomen',

            'convention_id',
            'name',
            'get_district_display',
            'get_season_display',
            'get_panel_display',
            'year',
            'open_date',
            'close_date',
            'start_date',
            'end_date',
            'venue_name',
            'location',
            'timezone',
            'divisions',

            'image_id',

            'owners',
            'contests',
            'entries',
            'assignments',

        ]
        read_only_fields = [
            'image_id',
        ]
