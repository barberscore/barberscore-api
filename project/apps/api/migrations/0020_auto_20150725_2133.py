# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20150725_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupf',
            name='score',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='personf',
            name='score',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='songf',
            name='score',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='groupf',
            name='parent',
            field=models.ForeignKey(related_name='group_duplicates', to='api.Group'),
        ),
        migrations.AlterField(
            model_name='personf',
            name='parent',
            field=models.ForeignKey(related_name='person_duplicates', to='api.Person'),
        ),
        migrations.AlterField(
            model_name='songf',
            name='parent',
            field=models.ForeignKey(related_name='song_duplicates', to='api.Song'),
        ),
    ]
