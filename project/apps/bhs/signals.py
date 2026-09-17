# Django
from django.conf import settings
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Local
from .owners import add_user_to_owners
from .owners import remove_user_from_owners


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def user_pre_save(sender, instance, raw=False, **kwargs):
    if raw:
        return
    # The rest_framework_jwt pre_save receiver may rewrite instance.id
    # from Auth0 before this one runs, so fall back to the (unique)
    # email when the pk lookup comes up empty.
    previous = None
    if instance.pk:
        previous = sender.objects.filter(
            pk=instance.pk,
        ).values_list(
            'is_staff',
            flat=True,
        ).first()
    if previous is None and instance.email:
        previous = sender.objects.filter(
            email=instance.email,
        ).values_list(
            'is_staff',
            flat=True,
        ).first()
    instance._previous_is_staff = bool(previous)
    return


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_post_save(sender, instance, created, raw=False, **kwargs):
    """Refresh owners on in-progress objects when staff status changes."""
    if raw:
        return
    previous = getattr(instance, '_previous_is_staff', None)
    if previous is None:
        return
    if instance.is_staff and not previous:
        add_user_to_owners(instance)
    elif previous and not instance.is_staff:
        remove_user_from_owners(instance)
    return
