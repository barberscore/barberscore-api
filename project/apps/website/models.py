from django.db import models

from apps.api.models import (
    Group,
    Contestant,
)


class Collection(models.Model):
    kind = models.CharField(
        max_length=200,
    )

    def get_next(self):
        next = Collection.objects.filter(id__gt=self.id)
        if next:
            return next[0]
        return False

    def get_prev(self):
        prev = Collection.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev[0]
        return False


class Duplicate(models.Model):
    source_id = models.CharField(
        max_length=200,
    )

    collection = models.ForeignKey(
        'Collection',
        related_name='duplicates',
    )
