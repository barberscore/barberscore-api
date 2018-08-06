# Django
# Third-Party
from collections import defaultdict
from django.db.models.signals import *
from django.dispatch import receiver
from django.conf import settings

# Local
from .models import User
from .tasks import activate_user
from .tasks import delete_account


@receiver(pre_delete, sender=User)
def user_pre_delete(sender, instance, **kwargs):
    allowed = any([
        settings.DJANGO_SETTINGS_MODULE == 'settings.prod',
        settings.DJANGO_SETTINGS_MODULE == 'settings.dev',
    ])
    if allowed:
        if not instance.is_staff:
            delete_account(instance)
    return


@receiver(pre_save, sender=User)
def user_pre_save(sender, instance, **kwargs):
    allowed = any([
        settings.DJANGO_SETTINGS_MODULE == 'settings.prod',
        settings.DJANGO_SETTINGS_MODULE == 'settings.dev',
    ])
    if allowed:
        if not instance.is_staff and not instance.person:
            activate_user(instance)
    return


class DisableSignals(object):
    def __init__(self, disabled_signals=None):
        self.stashed_signals = defaultdict(list)
        self.disabled_signals = disabled_signals or [
            pre_init, post_init,
            pre_save, post_save,
            pre_delete, post_delete,
            pre_migrate, post_migrate,
        ]

    def __enter__(self):
        for signal in self.disabled_signals:
            self.disconnect(signal)

    def __exit__(self, exc_type, exc_val, exc_tb):
        for signal in self.stashed_signals.keys():
            self.reconnect(signal)

    def disconnect(self, signal):
        self.stashed_signals[signal] = signal.receivers
        signal.receivers = []

    def reconnect(self, signal):
        signal.receivers = self.stashed_signals.get(signal, [])
        del self.stashed_signals[signal]
