

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
from django.contrib.postgres.fields import ArrayField
from django.forms import MultipleChoiceField


@deconstructible
class UploadPath(object):
    # Maintained to keep migrations
    def __call__(self, instance, filename):
        return os.path.join(
            instance._meta.model_name,
            str(instance.id),
        )


@deconstructible
class ImageUploadPath(object):

    def __call__(self, instance, filename):
        return os.path.join(
            instance._meta.model_name,
            'image',
            str(instance.id),
        )


@deconstructible
class FileUploadPath(object):

    def __call__(self, instance, filename):
        return os.path.join(
            instance._meta.model_name,
            filename,
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


class DivisionsField(ArrayField):
    def formfield(self, **kwargs):
        defaults = {
            'form_class': MultipleChoiceField,
            'choices': self.base_field.choices,
        }
        defaults.update(kwargs)
        # Skip our parent's formfield implementation completely as we don't
        # care for it.
        # pylint:disable=bad-super-call
        return super(ArrayField, self).formfield(**defaults)

    def to_python(self, value):
        res = super().to_python(value)
        if isinstance(res, list):
            value = [self.base_field.to_python(val) for val in res]
        return value
