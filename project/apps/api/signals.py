from django.db.models.signals import (
    post_save,
)

from django.dispatch import receiver

from .models import (
    Performance,
    Session,
)


@receiver(post_save, sender=Session)
def session_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Create sentinels."""
    if not raw:
        if created:
            i = 1
            while i <= instance.num_rounds:
                instance.rounds.create(
                    num=i,
                    kind=(instance.num_rounds - i) + 1,
                )
                i += 1


@receiver(post_save, sender=Performance)
def performance_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Create sentinels."""
    if not raw:
        if created:
            s = 1
            while s <= instance.round.num_songs:
                song = instance.songs.create(
                    performance=instance,
                    num=s,
                )
                s += 1
                assignments = instance.round.session.assignments.filter(
                    category__in=[
                        instance.round.session.assignments.model.CATEGORY.music,
                        instance.round.session.assignments.model.CATEGORY.presentation,
                        instance.round.session.assignments.model.CATEGORY.singing,
                    ]
                )
                for assignment in assignments:
                    assignment.scores.create(
                        assignment=assignment,
                        song=song,
                        category=assignment.category,
                        kind=assignment.kind,
                    )
