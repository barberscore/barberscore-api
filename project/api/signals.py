import django_rq

# Django
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_fsm.signals import post_transition
# Local
from .models import Appearance
from .models import Panelist
from .models import Person
from .models import User
from .models import Round

from .tasks import save_reports_from_round
from .tasks import save_psa_from_panelist
from .tasks import save_csa_from_appearance


@receiver(post_transition, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        try:
            person = Person.objects.get(
                email=instance.email,
            )
        except Person.DoesNotExist:
            return
        instance.person = person
        instance.save()
    return

@receiver(post_transition, sender=Appearance)
def appearance_post_transition(sender, instance, name, source, target, **kwargs):
    if name == 'complete':
        save_csa_from_appearance.delay(instance)
        return
    return

@receiver(post_transition, sender=Panelist)
def panelist_post_transition(sender, instance, name, source, target, **kwargs):
    if name == 'release':
        save_psa_from_panelist.delay(instance)
        return
    return

@receiver(post_transition, sender=Round)
def round_post_transition(sender, instance, name, source, target, **kwargs):
    if name == 'verify':
        save_reports_from_round.delay(instance)
        return
    return