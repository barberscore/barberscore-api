# Django
# Third-Party
from collections import defaultdict
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings

# Local
from .models import Person
from .models import User
from .tasks import create_account
from .tasks import update_account
from .tasks import delete_account
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# @receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if not instance.is_staff:
        if created:
            create_account.delay(instance)
        else:
            update_account.delay(instance)
    return

# @receiver(pre_delete, sender=User)
def user_pre_delete(sender, instance, **kwargs):
    if not instance.is_staff:
        delete_account.delay(instance)
    return

# @receiver(post_save, sender=Person)
def person_post_save(sender, instance, created, **kwargs):
    user = getattr(instance, 'user', None)
    if user:
        try:
            validate_email(instance.email)
        except ValidationError:
            user.delete()
            return
        if any([
            user.email != instance.email,
            user.name != instance.nomen,
        ]):
            user.email = instance.email
            user.name = instance.nomen
            user.save()
    return
