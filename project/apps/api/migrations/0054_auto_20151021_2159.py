# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0053_auto_20151021_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judge',
            name='category',
            field=models.IntegerField(blank=True, null=True, choices=[(0, b'Admin'), (1, b'Music'), (2, b'Presentation'), (3, b'Singing'), (4, b'Music Candidate'), (5, b'Presentation Candidate'), (6, b'Singing Candidate'), (7, b'Music Composite'), (8, b'Presentation Composite'), (9, b'Singing Composite')]),
        ),
    ]
