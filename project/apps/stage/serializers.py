from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework_json_api import serializers

from .fields import TimezoneField

from .models import Grid
from .models import Venue


class GridSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Grid
        fields = [
            'id',
            'url',
            'status',
            'period',
            'num',
            'location',
            'photo',
            'arrive',
            'depart',
            'backstage',
            'onstage',
            'start',
            'renditions',
            'venue',
            'round',
            # 'appearance',
            'permissions',
        ]


class VenueSerializer(serializers.ModelSerializer):
    timezone = TimezoneField(allow_null=True)
    permissions = DRYPermissionsField()

    class Meta:
        model = Venue
        fields = (
            'id',
            'url',
            'name',
            'status',
            'city',
            'state',
            'airport',
            'timezone',
            'conventions',
            'permissions',
        )
