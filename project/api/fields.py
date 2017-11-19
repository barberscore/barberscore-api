# Third-Party
import pytz
import six
from cloudinary.models import CloudinaryField
from rest_framework_json_api import serializers

# Django
from django.core.exceptions import (
    ValidationError,
)


class CloudinaryRenameField(CloudinaryField):
    def upload_options(self, model_instance):
        folder = model_instance._meta.model_name
        public_id = str(model_instance.id)
        options = {
            'public_id': public_id,
            'overwrite': True,
            'invalidate': True,
            'folder': folder,
            'format': 'png',
        }
        return options


class TimezoneField(serializers.Field):
    def to_representation(self, obj):
        return six.text_type(obj)

    def to_internal_value(self, data):
        try:
            return pytz.timezone(str(data))
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValidationError('Unknown timezone')
