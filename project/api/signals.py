# Django
# Third-Party
from django.db.models.signals import (
    pre_delete,
)
from django.dispatch import receiver

# Local
from .models import (
    User,
)

from .tasks import (
    delete_auth0_account_from_user,
)


@receiver(pre_delete, sender=User)
def user_pre_delete(sender, instance, **kwargs):
    delete_auth0_account_from_user(instance)
    return
