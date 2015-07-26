# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_groupf_songf'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='primitive',
        ),
        migrations.RemoveField(
            model_name='duplicate',
            name='collection',
        ),
        migrations.RemoveField(
            model_name='groupf',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='personf',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='songf',
            name='parent',
        ),
        migrations.DeleteModel(
            name='Collection',
        ),
        migrations.DeleteModel(
            name='Duplicate',
        ),
        migrations.DeleteModel(
            name='GroupF',
        ),
        migrations.DeleteModel(
            name='PersonF',
        ),
        migrations.DeleteModel(
            name='Primitive',
        ),
        migrations.DeleteModel(
            name='SongF',
        ),
    ]
