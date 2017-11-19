# Third-Party
import pytz
import six
from cloudinary.models import CloudinaryField
from rest_framework_json_api import serializers

# Django
from django.core.exceptions import (
    ValidationError,
)


from django.utils.deconstruct import deconstructible
from django.utils.text import slugify
import os


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path='', prefix=''):
        self.path = sub_path
        self.prefix = prefix

    def __call__(self, instance, filename):
        f, ext = os.path.splitext(filename)
        if self.prefix:
            deslashed = instance.nomen.replace("/", "-")
            name = "-".join([
                self.prefix,
                slugify(deslashed),
            ])
        else:
            name = instance.id
        filename = '{0}{1}'.format(name, ext.lower())
        return os.path.join(self.path, filename)


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

class CloudinaryXLSXField(CloudinaryField):
    pass


class TimezoneField(serializers.Field):
    def to_representation(self, obj):
        return six.text_type(obj)

    def to_internal_value(self, data):
        try:
            return pytz.timezone(str(data))
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValidationError('Unknown timezone')
