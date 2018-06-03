# Django
# Third-Party
from django.db.models.signals import pre_delete
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# Local
from .models import User
from .tasks import delete_account


@receiver(pre_delete, sender=User)
def user_pre_delete(sender, instance, **kwargs):
    if settings.DJANGO_SETTINGS_MODULE == 'settings.prod':
        if instance.username.startswith('auth0|'):
            delete_account(instance)
    return


@receiver(pre_delete, sender=User)
def user_post_save(sender, instance, created, raw=False, **kwargs):
    if settings.DJANGO_SETTINGS_MODULE == 'settings.prod':
        if instance.username.startswith('auth0|'):
            activate_user(instance)
    return
