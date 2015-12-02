# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20151201_2255'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='score',
            options={},
        ),
        migrations.AlterField(
            model_name='score',
            name='kind',
            field=models.IntegerField(choices=[(0, b'Admin'), (1, b'Music'), (2, b'Presentation'), (3, b'Singing'), (4, b'Music Candidate'), (5, b'Presentation Candidate'), (6, b'Singing Candidate'), (7, b'Music Composite'), (8, b'Presentation Composite'), (9, b'Singing Composite')]),
        ),
        migrations.AlterField(
            model_name='score',
            name='panelist',
            field=models.ForeignKey(related_name='scores', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Panelist', null=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='performance',
            field=models.ForeignKey(related_name='scores', to='api.Performance'),
        ),
    ]
