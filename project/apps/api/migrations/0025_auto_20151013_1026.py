# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def denullify(apps, schema_editor):
    Arrangement = apps.get_model('api', 'Arrangement')
    Convention = apps.get_model('api', 'Convention')
    District = apps.get_model('api', 'District')
    Group = apps.get_model('api', 'Group')
    Performance = apps.get_model('api', 'Performance')
    Person = apps.get_model('api', 'Person')
    Song = apps.get_model('api', 'Song')

    for obj in Arrangement.objects.all():
        if obj.bhs_arranger is None: obj.bhs_arranger = ""
        if obj.bhs_songname is None: obj.bhs_songname = ""
        if obj.fuzzy is None: obj.fuzzy = ""
        if obj.person_match is None: obj.person_match = ""
        if obj.song_match is None: obj.song_match = ""
        obj.save()

    for obj in Convention.objects.all():
        if obj.dates is None: obj.dates = ""
        if obj.location is None: obj.location = ""
        obj.save()

    for obj in District.objects.all():
        if obj.email is None: obj.email = ""
        if obj.long_name is None: obj.long_name = ""
        if obj.notes is None: obj.notes = ""
        obj.save()

    for obj in Group.objects.all():
        if obj.chapter_name is None: obj.chapter_name = ""
        if obj.email is None: obj.email = ""
        if obj.fuzzy is None: obj.fuzzy = ""
        if obj.notes is None: obj.notes = ""
        obj.save()

    for obj in Performance.objects.all():
        if obj.penalty is None: obj.penalty = ""
        obj.save()

    for obj in Person.objects.all():
        if obj.email is None: obj.email = ""
        if obj.fuzzy is None: obj.fuzzy = ""
        if obj.notes is None: obj.notes = ""
        obj.save()

    for obj in Song.objects.all():
        if obj.fuzzy is None: obj.fuzzy = ""
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20151013_1010'),
    ]

    operations = [
        migrations.RunPython(denullify),
    ]
