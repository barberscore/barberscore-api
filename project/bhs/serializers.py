
# Third-Party
# from rest_framework.validators import UniqueTogetherValidator
from rest_framework_json_api import serializers

# Local
from .models import Human
from .models import Structure


class HumanSerializer(serializers.ModelSerializer):
    common_name = serializers.SerializerMethodField()

    def get_common_name(self, obj):
        last = obj.last_name.strip()
        if obj.nick_name:
            first = obj.nick_name.strip()
        else:
            first = obj.first_name.strip()
        return " ".join([
            first,
            last,
        ])


    class Meta:
        model = Human
        fields = (
            'id',
            # 'url',
            'first_name',
            'middle_name',
            'last_name',
            'nick_name',
            'common_name',
            'email',
            'birth_date',
            'is_deceased',
            'home_phone',
            'cell_phone',
            'work_phone',
            'bhs_id',
            'gender',
            'part',
            # 'full_name',
            'created',
            'modified',
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
            'created',
            'modified',
            'parent',
        )
