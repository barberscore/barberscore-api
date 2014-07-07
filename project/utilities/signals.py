from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

import logging
log = logging.getLogger(__name__)

from django.utils.text import slugify
from django.conf import settings

from convention.models import (
    Contestant,
    Contest,
)

from profile.models import (
    Profile,
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
        u"{0} {1} {2}".format(
            instance.year,
            instance.get_contest_level_display(),
            instance.get_contest_type_display(),
        )
    )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()
