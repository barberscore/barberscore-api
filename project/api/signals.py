# Django
# Third-Party
from collections import defaultdict
from django.db.models.signals import *
from django.dispatch import receiver
from django.conf import settings
from django.apps import apps

# Local
from .models import Person
from .models import User
from .tasks import delete_account
from .tasks import update_account
from .tasks import get_auth0

# User signals only link/unlink person?
@receiver(pre_delete, sender=User)
def user_pre_delete(sender, instance, **kwargs):
    allowed = any([
        settings.DJANGO_SETTINGS_MODULE == 'settings.prod',
        # settings.DJANGO_SETTINGS_MODULE == 'settings.dev',
    ])
    if allowed:
        if not instance.is_staff:
            delete_account.delay(instance)
    return


@receiver(pre_save, sender=User)
def user_pre_save(sender, instance, **kwargs):
    allowed = any([
        settings.DJANGO_SETTINGS_MODULE == 'settings.prod',
        # settings.DJANGO_SETTINGS_MODULE == 'settings.dev',
    ])
    if allowed:
        person = getattr(instance, 'person', None)
        if not instance.is_staff and not person:
            # Link person to user, only if empty
            Person = apps.get_model('api.person')
            auth0 = get_auth0()
            account = auth0.users.get(instance.username)
            email = account['email'].lower()
            person, created = Person.objects.get_or_create(email=email)
            instance.person = person
    return

@receiver(post_save, sender=Person)
def person_post_save(sender, instance, created, **kwargs):
    allowed = any([
        settings.DJANGO_SETTINGS_MODULE == 'settings.prod',
        # settings.DJANGO_SETTINGS_MODULE == 'settings.dev',
    ])
    if allowed:
        user = getattr(instance, 'user', None)
        if user:
            # Update if record linked.
            update_account.delay(instance)
    return