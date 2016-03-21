from django.db.models.signals import (
    post_save,
)

# from django_fsm.signals import (
#     post_transition,
#     pre_transition,
# )

from django.dispatch import receiver

from .models import (
    Performer,
    Performance,
    Certification,
)


@receiver(post_save, sender=Certification)
def certification_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Denormalization to make autocomplete work as expected."""
    if not raw:
        if created:
            instance.person.save()


@receiver(post_save, sender=Performer)
def performer_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Create contestant sentinels on performer creation."""
    if not raw:
        if created:
            instance.build()


@receiver(post_save, sender=Performance)
def performance_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Create scoring sentinels on performance creation."""
    if not raw:
        if created:
            instance.build()


# @receiver(post_transition)
# def dixon_post_transition(sender, instance, target, source, **kwargs):
#     if sender == Performance and target == Performance.STATUS.entered:
#         dixon(instance)
#         instance.calculate()
#         instance.save()


# @receiver(pre_transition)
# def fill_pre_transition(sender, instance, target, source, **kwargs):
#     if sender == Performance and target == Performance.STATUS.entered:
#         fill_missing(instance)
