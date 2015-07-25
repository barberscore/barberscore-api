import dedupe

from django.db import models
from django.core.files import File

from jsonfield import JSONField

from apps.api.models import (
    Group,
    Song,
    Person,
)


class PersonF(models.Model):
    parent = models.ForeignKey(
        Person,
        related_name='parent_duplicates',
    )
    child = models.CharField(
        max_length=200,
    )


class SongF(models.Model):
    parent = models.ForeignKey(
        Song,
        related_name='parent_duplicates',
    )
    child = models.CharField(
        max_length=200,
    )


class GroupF(models.Model):
    parent = models.ForeignKey(
        Group,
        related_name='parent_duplicates',
    )
    child = models.CharField(
        max_length=200,
    )


class Collection(models.Model):
    kind = models.CharField(
        max_length=200,
    )

    primitive = models.ForeignKey(
        'Primitive',
        related_name='collections',
    )

    is_flag = models.BooleanField(
        default=False,
    )

    def get_next(self):
        next = Collection.objects.filter(id__gt=self.id)
        if next:
            return next[0]
        return None

    def get_prev(self):
        prev = Collection.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev[0]
        return None


class Duplicate(models.Model):
    source_id = models.CharField(
        max_length=200,
    )

    collection = models.ForeignKey(
        'Collection',
        related_name='duplicates',
    )


class Primitive(models.Model):
    name = models.CharField(
        max_length=200,
    )

    trainer = JSONField(
        null=True,
        blank=True,
    )

    training_file = models.FileField(
        null=True,
        blank=True,
    )

    @property
    def fields(self):
        if self.name == 'Group':
            fields = [
                {
                    'field': 'name',
                    'type': 'String',
                    'has missing': False,
                },
                {
                    'field': 'kind',
                    'type': 'String',
                    'has missing': False,
                },
            ]
        elif self.name == 'Song':
            fields = [
                {
                    'field': 'name',
                    'type': 'String',
                    'has missing': False,
                },
            ]
        elif self.name == 'Person':
            fields = [
                {
                    'field': 'name',
                    'type': 'String',
                    'has missing': False,
                },
            ]
        else:
            return None
        return fields

    @property
    def data(self):
        data = {}
        if self.name == 'Group':
            qs = Group.objects.all()
            for q in qs:
                data[q.id.hex] = {
                    'name': q.name,
                    'kind': q.get_kind_display(),
                }
        elif self.name == 'Song':
            qs = Song.objects.all()
            for q in qs:
                data[q.id.hex] = {
                    'name': q.name,
                }
        elif self.name == 'Person':
            qs = Person.objects.all()
            for q in qs:
                data[q.id.hex] = {
                    'name': q.name,
                }
        else:
            return None
        return data

    def build(self, threshold=.3):
        print 'build sample...'
        deduper = dedupe.Dedupe(self.fields)
        deduper.sample(self.data)
        print 'train sample...'
        dedupe.consoleLabel(deduper)
        print 'build training...'
        deduper.train()
        print 'save training...'
        with open('/tmp/training_file.json', 'wb') as f:
            deduper.writeTraining(f)
        reopen = open('/tmp/training_file.json', 'rb')
        django_file = File(reopen)
        self.training_file.save(
            "{0}_training_file.json".format(self.name),
            django_file,
        )
        print 'training saved'
        print 'matching...'
        matches = deduper.match(self.data, threshold)
        for match in matches:
            collection = Collection.objects.create(
                primitive=self,
            )
            i = 0
            l = len(match[0])
            while i < l:
                Duplicate.objects.create(
                    collection=collection,
                    source_id=match[0][i],
                )
                i += 1
        return 'complete'

    def __unicode__(self):
        return self.name
