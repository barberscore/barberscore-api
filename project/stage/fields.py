
# Third-Party
import pytz
import six
from rest_framework_json_api import serializers

# Django
from django.core.exceptions import ValidationError


class TimezoneField(serializers.Field):
    def to_representation(self, obj):
        return six.text_type(obj)

    def to_internal_value(self, data):
        try:
            return pytz.timezone(str(data))
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValidationError('Unknown timezone')
