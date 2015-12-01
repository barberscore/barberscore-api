# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0143_auto_20151201_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='qual_score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='kind',
            field=models.IntegerField(choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate'), (5, b'Novice')]),
        ),
    ]
