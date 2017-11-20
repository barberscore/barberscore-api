# Django
# Third-Party
from django.db.models.signals import (
    post_save,
    pre_delete,
)
from django.dispatch import receiver

# Local
from .models import (
    Entry,
    # Person,
    User,
)

from .tasks import (
    create_auth0_account_from_user,
    update_auth0_account_from_user,
    delete_auth0_account_from_user,
)


@receiver(post_save, sender=Entry)
def entry_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Create/Update Auth0 from User."""
    if not raw:
        if created:
            # Add contestants
            contests = instance.session.contests.filter(
                status=instance.session.contests.model.STATUS.included,
            )
            for contest in contests:
                instance.contestants.create(
                    contest=contest,
                    status=instance.contestants.model.STATUS.included,
                )
            # Add participants
            members = instance.group.members.filter(
                status=instance.group.members.model.STATUS.active,
            )
            for member in members:
                instance.participants.create(
                    person=member.person,
                    status=instance.participants.model.STATUS.included,
                )


# @receiver(post_save, sender=Person)
# def person_post_save(sender, instance=None, created=False, raw=False, **kwargs):
#     if not raw:
#         is_active = bool(instance.status > 0)
#         user = getattr(instance, 'user', None)
#         if user:
#             is_delta = any([
#                 instance.full_name != user.name,
#                 instance.email != user.email,
#                 is_active == user.is_active,
#             ])
#         if created:
#             if instance.email:
#                 User.objects.create_user(
#                     person=instance,
#                     is_active=is_active,
#                 )
#         else:
#             if instance.email:
#                 if not user:
#                     User.objects.create_user(
#                         person=instance,
#                         is_active=is_active,
#                     )
#                 else:
#                     if is_delta:
#                         instance.user.name = instance.full_name
#                         instance.user.email = instance.email
#                         instance.user.is_active = is_active
#                         instance.user.save()
#             else:
#                 if user:
#                     user.delete()


@receiver(post_save, sender=User)
def user_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Create/Update Auth0 from User."""
    if not raw:
        if instance.is_active:
            # Can bypass if not active.
            if created:
                response = create_auth0_account_from_user(instance)
                instance.auth0_id = response['user_id']
                instance.save()
            else:
                update_auth0_account_from_user(instance)
    return


@receiver(pre_delete, sender=User)
def user_pre_delete(sender, instance, **kwargs):
    delete_auth0_account_from_user(instance)
    return
