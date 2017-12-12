# Django
# Third-Party
from django.db.models.signals import (
    pre_delete,
    post_save,
)
from django.dispatch import receiver

# Local
from .models import (
    Session,
    Entry,
    User,
)

from .tasks import (
    delete_auth0_account_from_user,
)


@receiver(post_save, sender=Entry)
def entry_post_save(sender, instance, created, raw=False, **kwargs):
    entry = instance
    if created and not raw:
        contests = entry.session.contests.filter(
            status=entry.session.contests.model.STATUS.included,
        )
        for contest in contests:
            # Could also do some logic here.
            entry.contestants.create(
                status=entry.contestants.model.STATUS.included,
                contest=contest,
            )
        round = entry.session.rounds.get(num=1)
        entry.grids.create(
            round=round,
        )
        members = entry.group.members.filter(
            status__gt=0,
        )
        for member in members:
            # Again, we might want to add currying logic.
            entry.participants.create(
                person=member.person,
                status=entry.participants.model.STATUS.included,
                part=member.part,
            )
        has_divisions = bool(
            entry.session.convention.organization.children.filter(
                kind=entry.session.convention.organization.KIND.division,
                status=entry.session.convention.organization.STATUS.active,
            )
        )
        if has_divisions:
            entry.representing = entry.group.division
        else:
            entry.representing = entry.group.district
        entry.save()
    return


@receiver(post_save, sender=Session)
def session_post_save(sender, instance, created, raw=False, **kwargs):
    session = instance
    if created and not raw:
        grantors = session.convention.grantors.all()
        for grantor in grantors:
            awards = grantor.organization.awards.filter(
                status=grantor.organization.awards.model.STATUS.active,
                kind=session.kind,
            )
            for award in awards:
                # Could also do some logic here for more precision
                session.contests.create(
                    status=session.contests.model.STATUS.included,
                    award=award,
                )
        for i in range(session.num_rounds):
            num = i + 1
            kind = session.num_rounds - i
            session.rounds.create(
                num=num,
                kind=kind,
            )
    return


@receiver(pre_delete, sender=User)
def user_pre_delete(sender, instance, **kwargs):
    delete_auth0_account_from_user(instance)
    return
