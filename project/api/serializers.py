
# Third-Party
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_json_api import serializers

# Local
from .fields import TimezoneField


from .models import User


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
            # 'is_convention_manager',
            # 'is_session_manager',
            # 'is_round_manager',
            # 'is_scoring_manager',
            # 'is_group_manager',
            # 'is_person_manager',
            # 'is_award_manager',
            # 'is_officer_manager',
            # 'is_chart_manager',
            # 'is_assignment_manager',
            'permissions',
        ]
        # read_only_fields = [
        #     'is_convention_manager',
        #     'is_session_manager',
        #     'is_round_manager',
        #     'is_scoring_manager',
        #     'is_group_manager',
        #     'is_person_manager',
        #     'is_award_manager',
        #     'is_officer_manager',
        #     'is_chart_manager',
        #     'is_assignment_manager',
        # ]
