# Django
# Third-Party
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings

# Local
from .models import Person
from .models import User
from .tasks import delete_account


@receiver(pre_delete, sender=User)
def user_pre_delete(sender, instance, **kwargs):
    if settings.ENV == 'prod':
        if instance.username.startswith('auth0'):
            delete_account(instance)
    return
