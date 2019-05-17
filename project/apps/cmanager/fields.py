# Standard Library
import os
import pytz
import six

# Django
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
from rest_framework_json_api import serializers


@deconstructible
class ImageUploadPath(object):

    def __call__(self, instance, filename):
        return os.path.join(
            instance._meta.model_name,
            'image',
            str(instance.id),
        )

class TimezoneField(serializers.Field):
    def to_representation(self, obj):
        return six.text_type(obj)

    def to_internal_value(self, data):
        try:
            return pytz.timezone(str(data))
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValidationError('Unknown timezone')
