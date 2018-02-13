# Django
# Third-Party
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# Local
from .models import Entry
from .models import Session
from .models import User
from .tasks import delete_account


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
                status=entry.contestants.model.STATUS.excluded,
                contest=contest,
            )
        has_divisions = bool(
            entry.session.convention.group.children.filter(
                kind=entry.session.convention.group.KIND.division,
                status=entry.session.convention.group.STATUS.active,
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
            awards = grantor.group.awards.filter(
                status=grantor.group.awards.model.STATUS.active,
                kind=session.kind,
                season=session.convention.season,
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
    delete_account(instance.account_id)
    return
