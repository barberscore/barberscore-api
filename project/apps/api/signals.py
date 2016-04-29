from django.db.models.signals import (
    post_save,
)

from django.dispatch import receiver

from .models import (
    Award,
    Group,
    Performer,
    Role,
    Session,
)


@receiver(post_save, sender=Performer)
def performer_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Create contestant sentinels on performer creation."""
    if not raw:
        if created:
            if instance.group.kind == Group.KIND.chorus:
                instance.representing = instance.group.chapter.organization
                directors = instance.group.roles.filter(
                    part=Role.PART.director,
                    status=Role.STATUS.active,
                )
                if directors.count() == 1:
                    instance.director = directors.first()
                elif directors.count() == 2:
                    instance.director = directors.first()
                    instance.codirector = directors.last()
                else:
                    pass
                instance.save()
            else:
                instance.representing = instance.group.organization
                try:
                    instance.tenor = instance.group.roles.get(
                        part=Role.PART.tenor,
                        status=Role.STATUS.active,
                    )
                except Role.DoesNotExist:
                    pass
                except Role.MultipleObjectsReturned:
                    pass
                try:
                    instance.lead = instance.group.roles.get(
                        part=Role.PART.lead,
                        status=Role.STATUS.active,
                    )
                except Role.DoesNotExist:
                    pass
                except Role.MultipleObjectsReturned:
                    pass
                try:
                    instance.baritone = instance.group.roles.get(
                        part=Role.PART.baritone,
                        status=Role.STATUS.active,
                    )
                except Role.DoesNotExist:
                    pass
                except Role.MultipleObjectsReturned:
                    pass
                try:
                    instance.bass = instance.group.roles.get(
                        part=Role.PART.bass,
                        status=Role.STATUS.active,
                    )
                except Role.DoesNotExist:
                    pass
                except Role.MultipleObjectsReturned:
                    pass
                instance.save()


@receiver(post_save, sender=Session)
def session_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Create contest sentinels on performer creation."""
    if not raw:
        if created:
            for participant in instance.convention.participants.all():
                awards = Award.objects.filter(
                    kind=instance.kind,
                    season=instance.convention.season,
                    organization=participant.organization,
                )
                for award in awards:
                    a, c = instance.contests.get_or_create(
                        award=award,
                    )
                    print "contest: {0}".format(a)
            instance.save()
