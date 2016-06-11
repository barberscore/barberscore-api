from django.db.models.signals import (
    post_save,
)

from django.dispatch import receiver

from .models import (
    Performance,
)


@receiver(post_save, sender=Performance)
def performance_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Denormalization to create protected class."""
    if not raw:
        if created:
            s = 1
            while s <= instance.round.num_songs:
                song = instance.songs.create(
                    performance=instance,
                    order=s,
                )
                s += 1
                judges = instance.round.session.judges.filter(
                    category__in=[
                        instance.round.session.judges.model.CATEGORY.music,
                        instance.round.session.judges.model.CATEGORY.presentation,
                        instance.round.session.judges.model.CATEGORY.singing,
                    ]
                )
                for judge in judges:
                    judge.scores.create(
                        judge=judge,
                        song=song,
                        category=judge.category,
                        kind=judge.kind,
                    )
