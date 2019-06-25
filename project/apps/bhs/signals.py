# Django
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
# Local
from .tasks import link_person_from_user
User = get_user_model()

def user_post_save(sender, instance, created, **kwargs):
    if created:
        link_person_from_user.delay(instance)
    return

post_save.connect(user_post_save, sender=User)
