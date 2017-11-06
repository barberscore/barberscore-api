# Django
# Third-Party
from auth0.v3.management import Auth0
from auth0.v3.management.rest import Auth0Error

from django.conf import settings
from django.db.models.signals import (
    post_save,
    pre_delete,
)
from django.dispatch import receiver

# Local
from .models import (
    Award,
    Entry,
    Session,
    User,
)
from .utils import get_auth0_token


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


@receiver(post_save, sender=Session)
def session_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Create/Update Auth0 from User."""
    if not raw:
        if created:
            # Add contestants
            awards = Award.objects.filter(
                status=Award.STATUS.active,
                organization__grantors__session=instance,
            )
            for award in awards:
                instance.contests.create(
                    award=award,
                    status=instance.contests.model.STATUS.included,
                )


@receiver(post_save, sender=User)
def user_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Create/Update Auth0 from User."""
    if not raw:
        if instance.is_active:
            if created:
                token = get_auth0_token()
                auth0 = Auth0(
                    settings.AUTH0_DOMAIN,
                    token,
                )
                payload = {
                    "connection": "email",
                    "email": instance.email,
                    "email_verified": True,
                    "user_metadata": {
                        "name": instance.name
                    },
                    "app_metadata": {
                        "barberscore_id": str(instance.id),
                    }
                }
                try:
                    response = auth0.users.create(payload)
                except Auth0Error as e:
                    if 'The user already exists' in e.message:
                        return
                    else:
                        raise(e)
                instance.auth0_id = response['user_id']
                instance.save()
            else:
                token = get_auth0_token()
                auth0 = Auth0(
                    settings.AUTH0_DOMAIN,
                    token,
                )
                payload = {
                    "connection": "email",
                    "email": instance.email,
                    "email_verified": True,
                    "user_metadata": {
                        "name": instance.name
                    },
                    "app_metadata": {
                        "barberscore_id": str(instance.id),
                    }
                }
                try:
                    response = auth0.users.update(instance.auth0_id, payload)
                except Auth0Error as e:
                    raise(e)


@receiver(pre_delete, sender=User)
def user_pre_delete(sender, instance, **kwargs):
    if instance.auth0_id:
        token = get_auth0_token()
        auth0 = Auth0(
            settings.AUTH0_DOMAIN,
            token,
        )
        auth0.users.delete(instance.auth0_id)
    return
