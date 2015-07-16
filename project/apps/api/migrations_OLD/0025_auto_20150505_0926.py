# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20150504_1405'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contest',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='contest',
            unique_together=set([('kind', 'convention')]),
        ),
        migrations.RemoveField(
            model_name='contest',
            name='district',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='year',
        ),
    ]
