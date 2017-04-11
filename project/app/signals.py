# Django
from auth0.v2.management import Auth0
from auth0.v2.management.rest import Auth0Error
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Local
from .models import (
    # Award,
    User,
)

from .utils import get_auth0_token


# @receiver(post_save, sender=Appearance)
# def appearance_post_save(sender, instance=None, created=False, raw=False, **kwargs):
#     """Create sentinels."""
#     if not raw:
#         if created:
#             s = 1
#             while s <= instance.round.num_songs:
#                 song = instance.songs.create(
#                     appearance=instance,
#                     num=s,
#                 )
#                 s += 1
#                 assignments = instance.round.session.assignments.filter(
#                     category__in=[
#                         instance.round.session.assignments.model.CATEGORY.music,
#                         instance.round.session.assignments.model.CATEGORY.presentation,
#                         instance.round.session.assignments.model.CATEGORY.singing,
#                     ]
#                 )
#                 for assignment in assignments:
#                     assignment.scores.create(
#                         assignment=assignment,
#                         song=song,
#                         category=assignment.category,
#                         kind=assignment.kind,
#                     )


@receiver(post_save, sender=User)
def user_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Create Auth0 from user and send verification email."""
    if not raw:
        if created:
            if instance.person:
                token = get_auth0_token()
                password = User.objects.make_random_password()
                auth0 = Auth0(
                    settings.AUTH0_DOMAIN,
                    token,
                )
                create_user_payload = {
                    "connection": "Default",
                    "email": instance.email,
                    "verify_email": False,
                    "password": password,
                    "user_metadata": {
                        "name": instance.person.name
                    },
                    "app_metadata": {
                        "bhs_id": instance.person.bhs_id
                    }
                }
                try:
                    response = auth0.users.create(create_user_payload)
                except Auth0Error as e:
                    if 'The user already exists' in e.message:
                        return
                    else:
                        raise(e)
                change_password_payload = {
                    "user_id": response['user_id'],
                    "result_url": settings.PROJECT_WEBSITE,
                }
                ticket = auth0.tickets.create_pswd_change(change_password_payload)
                message = render_to_string(
                    'welcome_email.txt',
                    context={
                        'link': ticket['ticket'],
                    }
                )
                send_mail(
                    "Welcome to Barberscore Alpha Test",
                    message,
                    "Barberscore Admin <admin@barberscore.com>",
                    [instance.email],
                    fail_silently=False
                )
