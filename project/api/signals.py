# Django
import django_rq

# Third-Party
from collections import defaultdict
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings

# Local
from .models import Person
from .models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if not instance.is_staff:
        if created:
            account, new = instance.update_or_create_account()
            if new:
                # Set username if new; otherwise it's an overwrite and skip save
                instance.username = account['user_id']
                instance.save()
        else:
            queue = django_rq.get_queue('low')
            queue.enqueue(
                instance.update_or_create_account
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
