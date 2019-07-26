# Django
from django.db.models.signals import post_save

# Local
from .tasks import update_or_create_account_from_person
from .tasks import create_user_from_account
from .tasks import add_group_owner_from_officer
from .tasks import update_or_create_roles_from_officer


from .models import Person
from .models import Officer

def person_post_save(sender, instance, created, **kwargs):
    if not instance.email:
        return
    if created:
        account, new = update_or_create_account_from_person(instance)
        if new:
            create_user_from_account(account)
        return
    update_or_create_account_from_person(instance)
    return

def officer_post_save(sender, instance, created, **kwargs):
    add_group_owner_from_officer(instance)
    update_or_create_roles_from_officer.delay(instance)
    return

post_save.connect(person_post_save, sender=Person)
post_save.connect(officer_post_save, sender=Officer)
