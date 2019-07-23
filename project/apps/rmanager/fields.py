

# Standard Library
import os

# Third-Party
import pytz
import six
from rest_framework_json_api import serializers

# Django
from django.core.exceptions import ValidationError
from django.db.models import EmailField
from django.utils.deconstruct import deconstructible


@deconstructible
class UploadPath(object):

    def __init__(self, name):
        self.name = name

    def __call__(self, instance):
        return os.path.join(
            instance._meta.app_label,
            instance._meta.model_name,
            self.name,
            str(instance.id),
        )


class LowerEmailField(EmailField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is not None:
            value = value.lower()
        return value


class TimezoneField(serializers.Field):
    def to_representation(self, obj):
        return six.text_type(obj)

    def to_internal_value(self, data):
        try:
            return pytz.timezone(str(data))
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValidationError('Unknown timezone')
