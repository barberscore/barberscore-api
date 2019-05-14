from rest_framework import serializers


from .models import Group
from .models import Member
from .models import Officer
from .models import Person

from .models import Chart
from .models import Repertory


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = (
            'id',
            'common_name',
            'bhs_id',
        )
        read_only_fields = [
            'common_name',
        ]

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'bhs_id',
            'get_kind_display',
            'get_gender_display',
            'is_senior',
            'is_youth',
            'code',
            'international',
            'district',
            'get_division_display',
            'chapter',
        ]

class ChartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chart
        fields = (
            'id',
            'title',
            'arrangers',
            'composers',
            'lyricists',
        )

