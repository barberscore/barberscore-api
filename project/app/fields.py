import os
import pytz
import six


# Django
from django.core.exceptions import ValidationError


from django.db import models
from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import OneToOneField
from django.db.transaction import atomic
from django.utils.deconstruct import deconstructible

from rest_framework_json_api import serializers


class ReverseOneToOneDescriptorReturnsNone(ReverseOneToOneDescriptor):
    def __get__(self, instance, cls=None):
        try:
            return super().__get__(instance=instance)
        except ObjectDoesNotExist:
            return None


class OneToOneOrNoneField(models.OneToOneField):
    related_accessor_class = ReverseOneToOneDescriptorReturnsNone


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path=''):
        self.path = sub_path

    def __call__(self, instance, filename):
        f, ext = os.path.splitext(filename)
        filename = '{0}{1}'.format(instance.id, ext.lower())
        return os.path.join(self.path, filename)


class TimezoneField(serializers.Field):
    def to_representation(self, obj):
        return six.text_type(obj)

    def to_internal_value(self, data):
        try:
            return pytz.timezone(str(data))
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValidationError('Unknown timezone')
