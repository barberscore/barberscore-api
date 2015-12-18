# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_auto_20151217_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='kind',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Seniors'), (4, b'Collegiate'), (5, b'Novice')]),
        ),
    ]
