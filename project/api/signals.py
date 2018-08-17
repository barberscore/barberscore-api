# Django
# Third-Party
from collections import defaultdict
from django.db.models.signals import *
from django.dispatch import receiver
from django.conf import settings

# Local
from .models import User
from .tasks import activate_user
from .tasks import delete_account


@receiver(pre_delete, sender=User)
def user_pre_delete(sender, instance, **kwargs):
    allowed = any([
        settings.DJANGO_SETTINGS_MODULE == 'settings.prod',
        settings.DJANGO_SETTINGS_MODULE == 'settings.dev',
    ])
    if allowed:
        if not instance.is_staff:
            delete_account(instance)
    return


@receiver(pre_save, sender=User)
def user_pre_save(sender, instance, **kwargs):
    allowed = any([
        settings.DJANGO_SETTINGS_MODULE == 'settings.prod',
        settings.DJANGO_SETTINGS_MODULE == 'settings.dev',
    ])
    if allowed:
        if not instance.is_staff and not instance.person:
            activate_user(instance)
    return
