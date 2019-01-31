import django_rq

# Django
from django.db.models.signals import pre_delete
from django.db.models.signals import post_save
from django.dispatch import receiver

# Local
from .models import Person
from .models import User

from .tasks import person_post_save_handler


@receiver(post_save, sender=Person)
def person_post_save(sender, instance, created, **kwargs):
    queue = django_rq.get_queue('low')
    queue.enqueue(
        person_post_save_handler(instance)
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
