
# Third-Party
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework_json_api import serializers
from rest_framework_json_api.relations import ResourceRelatedField
from django.contrib.auth import get_user_model

# Local
from .fields import TimezoneField

from .models import Organization
from .models import District
from .models import Division

User = get_user_model()

class OrganizationSerializer(serializers.ModelSerializer):
    timezone = TimezoneField(allow_null=True)
    permissions = DRYPermissionsField()

    class Meta:
        model = Organization
        fields = [
            'id',
            'nomen',
            'name',
            'abbr',
            'logo',
            'district_nomen',
            'division_nomen',
            'drcj_nomen',
            'default_owners',
            'timezone',
            'permissions',
        ]
        read_only_fields = [
            'nomen'
            'logo',
        ]

    class JSONAPIMeta:
        included_resources = [
        ]

    def validate(self, data):
        return data


