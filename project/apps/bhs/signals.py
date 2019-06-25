# Django
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

# Local
User = get_user_model()
from .models import Person

def user_post_save(sender, instance, created, **kwargs):
    # print(instance.email, created)
    if created:
        if instance.email:
            try:
                person = Person.objects.get(email=instance.email)
            except Person.DoesNotExist:
                return
            person.user = instance
            person.save()
    return

post_save.connect(user_post_save, sender=User)
