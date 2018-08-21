# Django
# Third-Party
from collections import defaultdict
from django.db.models.signals import *
from django.dispatch import receiver
from django.conf import settings

# Local
from .models import Person
from .models import User
from .tasks import delete_account
from .tasks import update_account
from .tasks import link_account


# @receiver(pre_delete, sender=User)
def user_pre_delete(sender, instance, **kwargs):
    if not instance.is_staff:
        delete_account.delay(instance)
    return


# @receiver(pre_save, sender=User)
def user_pre_save(sender, instance, **kwargs):
    """Create User-Person Link"""
    person = getattr(instance, 'person', None)
    if not instance.is_staff and not person:
        # Link person to user, only if empty and not admin
        person = link_account(instance)
        instance.person = person
    return


# @receiver(post_save, sender=Person)
def person_post_save(sender, instance, created, **kwargs):
    user = getattr(instance, 'user', None)
    # changed = instance.tracker.has_changed('email')
    changed = True
    if user and changed:
        # Update if record linked and name/email has changed
        update_account.delay(instance)
    return