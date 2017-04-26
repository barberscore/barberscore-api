# Django
from auth0.v3.management import Auth0
from auth0.v3.management.rest import Auth0Error
from auth0.v3.authentication import Passwordless
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.template.loader import render_to_string

# Local
from .models import (
    User,
)

from .utils import get_auth0_token


@receiver(post_save, sender=User)
def user_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Create Auth0 from user and send verification email."""
    if not raw:
        if created:
            if instance.person:
                token = get_auth0_token()
                auth0 = Auth0(
                    settings.AUTH0_DOMAIN,
                    token,
                )
                create_user_payload = {
                    "connection": "email",
                    "email": instance.email,
                    "email_verified": True,
                    "user_metadata": {
                        "name": instance.person.name
                    },
                    "app_metadata": {
                        "bhs_id": instance.person.bhs_id
                    }
                }
                try:
                    auth0.users.create(create_user_payload)
                except Auth0Error as e:
                    if 'The user already exists' in e.message:
                        return
                    else:
                        raise(e)
                # And send Link
                ps = Passwordless('barberscore-dev.auth0.com')
                ps.email(
                    client_id=settings.AUTH0_CLIENT_ID,
                    email=instance.email,
                )
