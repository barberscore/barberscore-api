# Django
from auth0.v2.management import Auth0
from auth0.v2.management.rest import Auth0Error
from django.conf import settings
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

# Local
from .models import (
    # Award,
    Session,
    User,
    Contest,
    ContestPrivate,
    Performer,
    PerformerPrivate,
    Performance,
    PerformancePrivate,
    Song,
    SongPrivate,
    Contestant,
    ContestantPrivate,
)

from .utils import get_auth0_token


@receiver(post_save, sender=Session)
def session_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Create sentinels."""
    if not raw:
        if created:
            with transaction.atomic():

                # Add Rounds
                i = 1
                while i <= instance.num_rounds:
                    instance.rounds.create(
                        num=i,
                        kind=(instance.num_rounds - i) + 1,
                    )
                    i += 1
                # Add Contests
                instance.build_contests()

                # awards = Award.objects.filter(
                #     entity__hosts__convention=instance.convention,
                #     status=Award.STATUS.active,
                #     kind=instance.kind,
                # )
                # # Add all direct championship awards
                # for award in awards:
                #     instance.contests.create(
                #         award=award,
                #         num_rounds=award.championship_rounds
                #     )
                # # Add Prelims (if necessary)
                # # Check if it's a prelim session
                # if instance.is_prelims:
                #     # Get the "highest" host, excluding the Divisions
                #     host = instance.convention.hosts.filter(
                #         entity__kind__lt=20,
                #         entity__status=10,
                #     ).order_by(
                #         'entity__kind',
                #     ).first()
                #     # Find the primary award of that host entity
                #     prelim = host.entity.parent.awards.get(
                #         is_primary=True,
                #         kind=instance.kind,
                #     )
                #     instance.contests.create(
                #         award=prelim,
                #         num_rounds=prelim.qualifier_rounds,
                #         is_qualifier=True,
                #     )


@receiver(post_save, sender=Contest)
def contest_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Create Private Contest."""
    if not raw:
        if created:
            ContestPrivate.objects.create(contest=instance)


@receiver(post_save, sender=Contestant)
def contestant_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Create Private Contest."""
    if not raw:
        if created:
            ContestantPrivate.objects.create(contestant=instance)


@receiver(post_save, sender=Performer)
def performer_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Create Private Contest."""
    if not raw:
        if created:
            PerformerPrivate.objects.create(performer=instance)


@receiver(post_save, sender=Performance)
def performance_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Create Private Contest."""
    if not raw:
        if created:
            PerformancePrivate.objects.create(performance=instance)


@receiver(post_save, sender=Song)
def song_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Create Private Contest."""
    if not raw:
        if created:
            SongPrivate.objects.create(song=instance)


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
                payload = {
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
                    response = auth0.users.create(payload)
                except Auth0Error as e:
                    if 'The user already exists' in e.message:
                        return
                    else:
                        raise(e)
                ticket = auth0.tickets.create_pswd_change({"user_id": response['user_id']})
                send_mail(
                    "Welcome",
                    "Click: {0}".format(ticket['ticket']),
                    "Barberscore Admin <admin@barberscore.com>",
                    [instance.email],
                    fail_silently=False
                )
