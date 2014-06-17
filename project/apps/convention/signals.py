from django.db.models.signals import pre_save
from django.dispatch import receiver

import logging
log = logging.getLogger('apps.convention')

from django.utils.text import slugify

from .models import (
    Contestant,
    Contest,
)


@receiver(pre_save, sender=Contestant)
def contestant_pre_save(sender, instance, **kwargs):
    """
    Builds the slug; required before the contestant model can be saved.
    """
    instance.slug = slugify(unicode(instance.name))


@receiver(pre_save, sender=Contest)
def contest_pre_save(sender, instance, **kwargs):
    """
    Builds the slug; required before the contestant model can be saved.
    """
    instance.slug = slugify(
        unicode(instance.year),
        unicode(instance.get_contest_level_display()),
        unicode(instance.get_contest_type_display()),
    )
