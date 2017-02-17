from django.db import models
from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import OneToOneField
from django.db.transaction import atomic


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
    def __get__(self, instance, instance_type=None):
        model = getattr(self.related, 'related_model', self.related.model)

        try:
            return (super(AutoReverseOneToOneDescriptor, self)
                    .__get__(instance, instance_type))
        except model.DoesNotExist:
            # Using get_or_create instead() of save() or create() as it better handles race conditions
            model.objects.get_or_create(**{self.related.field.name: instance})

            # Don't return obj directly, otherwise it won't be added
            # to Django's cache, and the first 2 calls to obj.relobj
            # will return 2 different in-memory objects
            return (super(AutoReverseOneToOneDescriptor, self)
                    .__get__(instance, instance_type))


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
