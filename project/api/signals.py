# Django
# Third-Party
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# Local
from .models import User
from .tasks import delete_account


@receiver(pre_delete, sender=User)
def user_pre_delete(sender, instance, **kwargs):
    if instance.account_id:
        delete_account(instance.account_id)
    return
