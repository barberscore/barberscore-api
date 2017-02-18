import os

from django.db import models
from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import OneToOneField
from django.db.transaction import atomic
from django.utils.deconstruct import deconstructible


class ReverseOneToOneDescriptorReturnsNone(ReverseOneToOneDescriptor):
    def __get__(self, instance, cls=None):
        try:
            return super().__get__(instance=instance)
        except ObjectDoesNotExist:
            return None


class OneToOneOrNoneField(models.OneToOneField):
    related_accessor_class = ReverseOneToOneDescriptorReturnsNone


class AutoReverseOneToOneDescriptor(ReverseOneToOneDescriptor):
    """The descriptor that handles the object creation for an AutoOneToOneField."""

    @atomic
    def __get__(self, instance, cls=None):
        model = getattr(self.related, 'related_model', self.related.model)

        try:
            return super().__get__(instance)
        except model.DoesNotExist:
            model.objects.get_or_create(**{self.related.field.name: instance})

            # Don't return obj directly, otherwise it won't be added
            # to Django's cache, and the first 2 calls to obj.relobj
            # will return 2 different in-memory objects
            return super().__get__(instance)


class AutoOneToOneField(OneToOneField):
    """
    OneToOneField creates related object on first call if it doesnt exist yet.

    Use it instead of original OneToOne field.

    example:

        class MyProfile(models.Model):
            user = AutoOneToOneField(User, primary_key=True)
            home_page = models.URLField(max_length=255, blank=True)
            icq = models.IntegerField(max_length=255, null=True)
    """

    def contribute_to_related_class(self, cls, related):
        setattr(cls, related.get_accessor_name(), AutoReverseOneToOneDescriptor(related))


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path=''):
        self.path = sub_path

    def __call__(self, instance, filename):
        f, ext = os.path.splitext(filename)
        filename = '{0}{1}'.format(instance.id, ext.lower())
        return os.path.join(self.path, filename)

generate_image_filename = PathAndRename()
