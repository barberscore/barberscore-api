# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0157_panelist_panel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='panelist',
            options={},
        ),
        migrations.AlterField(
            model_name='score',
            name='panelist',
            field=models.ForeignKey(related_name='scores', on_delete=django.db.models.deletion.SET_NULL, to='api.Panelist', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='panelist',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='panelist',
            name='contest',
        ),
    ]
