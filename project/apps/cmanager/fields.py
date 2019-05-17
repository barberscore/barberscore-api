# Standard Library
import os

# Django
from django.utils.deconstruct import deconstructible


@deconstructible
class ImageUploadPath(object):

    def __call__(self, instance, filename):
        return os.path.join(
            instance._meta.model_name,
            'image',
            str(instance.id),
        )
