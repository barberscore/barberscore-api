# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0144_auto_20151130_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='kind',
            field=models.IntegerField(choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate'), (5, b'Novice')]),
        ),
    ]
