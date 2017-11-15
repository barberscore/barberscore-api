# Third-Party
# from rest_framework.validators import UniqueTogetherValidator
from rest_framework_json_api import serializers

# Local
from .models import (
    Human,
    Structure,
)


class HumanSerializer(serializers.ModelSerializer):
    def validate_first_name(self, value):
        return value.strip()

    class Meta:
        model = Human
        fields = (
            'id',
            # 'url',
            'first_name',
            'middle_name',
            'last_name',
            'nick_name',
            'email',
            'birth_date',
            'is_deceased',
            'phone',
            'cell_phone',
            'work_phone',
            'bhs_id',
            'sex',
            'primary_voice_part',
            'full_name',
            'created_ts',
            'updated_ts',
        )


class StructureSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=255,
        allow_blank=True,
        trim_whitespace=True,
    )

    class Meta:
        model = Structure
        fields = (
            'id',
            # 'url',
            'status',
            'name',
            'kind',
            'bhs_id',
            'chapter_code',
            'chorus_name',
            'preferred_name',
            'phone',
            'email',
            'established_date',
            'created_ts',
            'updated_ts',
            'parent',
        )
