from django.db.models.signals import (
    post_save,
)

from django.dispatch import receiver

from .models import (
    Contestant,
    ContestantScore,
    Performance,
    PerformanceScore,
    Performer,
    PerformerScore,
    Song,
    SongScore,
)


@receiver(post_save, sender=Contestant)
def contestant_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Denormalization to create protected class."""
    if not raw:
        if created:
            ContestantScore.objects.create(
                contestant=instance,
            )


@receiver(post_save, sender=Performance)
def performance(sender, instance=None, created=False, raw=False, **kwargs):
    """Denormalization to create protected class."""
    if not raw:
        if created:
            PerformanceScore.objects.create(
                performance=instance,
            )


@receiver(post_save, sender=Performer)
def performer_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Denormalization to create protected class."""
    if not raw:
        if created:
            PerformerScore.objects.create(
                performer=instance,
            )


@receiver(post_save, sender=Song)
def song_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Denormalization to create protected class."""
    if not raw:
        if created:
            SongScore.objects.create(
                song=instance,
            )
