import os
import string
from datetime import date
import phonenumbers
import six
import pytz
from django.db.models import EmailField, CharField, DateField
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from rest_framework_json_api import serializers
from django.contrib.postgres.fields import ArrayField
from django.forms import MultipleChoiceField


@deconstructible
class UploadPath(object):

    def __init__(self, name):
        self.name = name

    def __call__(self, instance, filename):
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


class DistrictField(ArrayField):
    def formfield(self, **kwargs):
        defaults = {
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


class TimezoneField(serializers.Field):
    def to_representation(self, obj):
        return six.text_type(obj)

    def to_internal_value(self, data):
        try:
            return pytz.timezone(str(data))
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValidationError('Unknown timezone')


class ValidatedPhoneField(CharField):
    def from_db_value(self, value, expression, connection):
        try:
            value = phonenumbers.parse(value, 'US')
        except phonenumbers.NumberParseException:
            return ""
        return phonenumbers.format_number(value, phonenumbers.PhoneNumberFormat.E164)


class LowerEmailField(EmailField):
    def from_db_value(self, value, expression, connection):
        try:
            validate_email(value)
        except ValidationError:
            return None
        return value.lower()


class VoicePartField(CharField):
    def from_db_value(self, value, expression, connection):
        part_map = {
            'tenor': 'tenor',
            'lead': 'lead',
            'baritone': 'baritone',
            'bass': 'bass',
        }
        try:
            return part_map[value.lower().strip()]
        except AttributeError:
            return None
        except KeyError:
            return None



class ReasonableBirthDate(DateField):
    def from_db_value(self, value, expression, connection):
        if value == date(1900, 1, 1) or value == date(2018, 11, 13):
            return None
        return value



class GenderField(CharField):
    def from_db_value(self, value, expression, connection):
        gender_map = {
            'men': 'male',
            'women': 'female',
            'mixed': 'mixed',
        }
        try:
            return gender_map[value.lower()]
        except AttributeError:
            return None
        except KeyError:
            return None


@deconstructible
class ImageUploadPath(object):

    def __init__(self, name):
        self.name = name

    def __call__(self, instance, filename):
        return os.path.join(
            instance._meta.app_label,
            instance._meta.model_name,
            self.name,
            str(instance.id),
        )



class NoPunctuationCharField(CharField):
    def from_db_value(self, value, expression, connection):
        if not value:
            return ""
        return value.translate(
            value.maketrans('', '', '!"#$%&()*+,./:;<=>?@[\\]^_`{|}~')
        ).strip()


class TimezoneField(serializers.Field):
    def to_representation(self, obj):
        return six.text_type(obj)

    def to_internal_value(self, data):
        try:
            return pytz.timezone(str(data))
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValidationError('Unknown timezone')
