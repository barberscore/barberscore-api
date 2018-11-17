

# Standard Library
from collections import defaultdict

# Third-Party
import django_rq

# Django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models.signals import pre_delete
from django.db.models.signals import post_save
from django.dispatch import receiver

# Local
from .models import Person
from .models import User



@receiver(post_save, sender=Person)
def person_post_save(sender, instance, **kwargs):
    if instance.user and instance.tracker.has_changed('email'):
        queue = django_rq.get_queue('low')
        queue.enqueue(
            instance.user.update_or_create_account()
        )
    return


@receiver(pre_delete, sender=User)
def user_pre_delete(sender, instance, **kwargs):
    if not instance.is_staff:
        queue = django_rq.get_queue('low')
        queue.enqueue(
            instance.delete_account
        )
    return
