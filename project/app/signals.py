# Django
from django.db.models.signals import post_save
from django.dispatch import receiver
from auth0.v2.management import Auth0
from django.conf import settings

# Local
# from .models import (
#     Performance,
#     Session,
#     User,
# )


# @receiver(post_save, sender=Session)
# def session_post_save(sender, instance=None, created=False, raw=False, **kwargs):
#     """Create sentinels."""
#     if not raw:
#         if created:
#             i = 1
#             while i <= instance.num_rounds:
#                 instance.rounds.create(
#                     num=i,
#                     kind=(instance.num_rounds - i) + 1,
#                 )
#                 i += 1


# @receiver(post_save, sender=Performance)
# def performance_post_save(sender, instance=None, created=False, raw=False, **kwargs):
#     """Create sentinels."""
#     if not raw:
#         if created:
#             s = 1
#             while s <= instance.round.num_songs:
#                 song = instance.songs.create(
#                     performance=instance,
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


# @receiver(post_save, sender=User)
# def user_post_save(sender, instance=None, created=False, raw=False, **kwargs):
#     """Create Auth0 from user."""
#     if not raw:
#         if created:
#             auth0 = Auth0(
#                 settings.AUTH0_DOMAIN,
#                 settings.AUTH0_TOKEN,
#             )
#             payload = {
#                 "connection": "Default",
#                 "email": instance.email,
#                 "password": 'changeme',
#                 "user_metadata": {
#                     "name": instance.name
#                 },
#                 "app_metadata": {
#                     "bhs_id": instance.bhs_id
#                 }
#             }
#             response = auth0.users.create(payload)
#             instance.sub = response['user_id']
#             instance.save()
