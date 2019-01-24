# Django
from django.db.models.signals import pre_delete
from django.db.models.signals import post_save
from django.dispatch import receiver

# Local
from .models import Person
from .models import User



@receiver(post_save, sender=Person)
def person_post_save(sender, instance, created, **kwargs):
    if created and instance.email:
        User.objects.create_user(person=instance)
    user = getattr(instance, 'user', None)
    # if user and instance.tracker.has_changed('email'):
    #     if instance.email:
    #         instance.user.update_account()
    #     else:
    #         instance.user.delete_account()
    return


@receiver(pre_delete, sender=User)
def user_pre_delete(sender, instance, **kwargs):
    if not instance.is_staff:
        instance.delete_account
    return
