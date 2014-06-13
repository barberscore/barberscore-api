from django.db.models.signals import pre_save
from django.dispatch import receiver

import logging
log = logging.getLogger('apps.convention')

from django.utils.text import slugify

from .models import (
    Contestant,
    Performance,
)


@receiver(pre_save, sender=Contestant)
def contestant_pre_save(sender, instance, **kwargs):
    instance.slug = slugify(instance.name)


@receiver(pre_save, sender=Performance)
def performance_pre_save(sender, instance, **kwargs):
    if instance.contest_round == Performance.QUARTERS:
        suffix = 'quarters'
    elif instance.contest_round == Performance.SEMIS:
        suffix = 'semis'
    elif instance.contest_round == Performance.FINALS:
        suffix = 'finals'
    else:
        raise RuntimeError("No valid performance round.")
    instance.slug = "{0}-{1}".format(
        slugify(instance.contestant.name), suffix
    )

    song1_score = round(
        sum[instance.sng1, instance.mus1, instance.prs1] / 1500
    )
    instance.song1_score = song1_score

    song2_score = round(
        sum[instance.sng2, instance.mus2, instance.prs2] / 1500
    )
    instance.song2_score = song2_score

    instance.performance_score = (song1_score + song2_score) / 2
