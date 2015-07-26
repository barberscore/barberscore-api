# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20150725_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personf',
            name='child',
            field=models.ForeignKey(related_name='person_children', blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='songf',
            name='child',
            field=models.ForeignKey(related_name='song_children', blank=True, to='api.Song', null=True),
        ),
    ]
