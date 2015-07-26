# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20150725_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupf',
            name='child',
            field=models.ForeignKey(related_name='group_children', blank=True, to='api.Group', null=True),
        ),
        migrations.AddField(
            model_name='personf',
            name='child',
            field=models.ForeignKey(related_name='person_children', blank=True, to='api.Group', null=True),
        ),
        migrations.AddField(
            model_name='songf',
            name='child',
            field=models.ForeignKey(related_name='song_children', blank=True, to='api.Group', null=True),
        ),
    ]
