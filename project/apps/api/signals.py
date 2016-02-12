from django.db.models.signals import (
    post_save,
)

from django_fsm.signals import (
    post_transition,
    pre_transition,
)

from django.dispatch import receiver

from .models import (
    Performance,
    Certification,
)

# from .factories import (
#     add_rounds,
#     add_judges,
# )


from .validators import (
    dixon,
    fill_missing,
)


@receiver(post_save, sender=Certification)
def certification_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """ Denormalization to make autocomplete work as expected """
    if not raw:
        if created:
            instance.person.save()


@receiver(post_transition)
def dixon_post_transition(sender, instance, target, source, **kwargs):
    if sender == Performance and target == Performance.STATUS.entered:
        dixon(instance)
        instance.calculate()
        instance.save()


@receiver(pre_transition)
def fill_pre_transition(sender, instance, target, source, **kwargs):
    if sender == Performance and target == Performance.STATUS.entered:
        fill_missing(instance)
