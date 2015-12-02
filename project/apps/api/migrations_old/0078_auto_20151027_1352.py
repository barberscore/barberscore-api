# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0077_auto_20151027_1337'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='catalog',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='catalog',
            name='fuzzy',
        ),
        migrations.RemoveField(
            model_name='catalog',
            name='name',
        ),
        migrations.RemoveField(
            model_name='catalog',
            name='person',
        ),
        migrations.RemoveField(
            model_name='catalog',
            name='person_match',
        ),
        migrations.RemoveField(
            model_name='catalog',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='catalog',
            name='song_match',
        ),
    ]
