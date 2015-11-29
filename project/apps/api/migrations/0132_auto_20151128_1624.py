# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0131_auto_20151128_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='kind',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Championship'), (2, b'Qualifier')]),
        ),
    ]
