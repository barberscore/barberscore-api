# Django
from django.db.models.signals import post_save

# Local
from .models import Convention


def convention_post_save(sender, instance, created, **kwargs):
    if created:
        instance.district = instance.group.code
        instance.save()
    return

post_save.connect(convention_post_save, sender=Convention)
