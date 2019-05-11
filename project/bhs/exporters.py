from rest_framework import serializers


from .models import Group
from .models import Member
from .models import Office
from .models import Officer
from .models import Person


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
