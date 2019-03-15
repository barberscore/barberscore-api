from rest_framework_json_api import serializers

from .models import Person


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = (
            'id',
            'status',
            'prefix',
            'first_name',
            'middle_name',
            'last_name',
            'nick_name',
            'suffix',
            'email',
            'birth_date',
            'is_deceased',
            'home_phone',
            'cell_phone',
            'work_phone',
            'bhs_id',
            'gender',
            'part',
            'mon',
        )
        read_only_fields = [
            'id',
            'status',
            'bhs_id',
        ]
