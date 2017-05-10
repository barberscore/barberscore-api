import pytz
import six


# Django
from django.core.exceptions import ValidationError


from django.db import models
from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor
from django.core.exceptions import ObjectDoesNotExist

from rest_framework_json_api import serializers

from cloudinary.models import CloudinaryField


class ReverseOneToOneDescriptorReturnsNone(ReverseOneToOneDescriptor):
    def __get__(self, instance, cls=None):
        try:
            return super().__get__(instance=instance)
        except ObjectDoesNotExist:
            return None


class OneToOneOrNoneField(models.OneToOneField):
    related_accessor_class = ReverseOneToOneDescriptorReturnsNone


class CloudinaryRenameField(CloudinaryField):

    def upload_options(self, model_instance):
        return {'public_id': str(model_instance.id)}


class TimezoneField(serializers.Field):
    def to_representation(self, obj):
        return six.text_type(obj)

    def to_internal_value(self, data):
        try:
            return pytz.timezone(str(data))
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValidationError('Unknown timezone')
