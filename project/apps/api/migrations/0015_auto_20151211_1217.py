# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20151211_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='qual',
            field=models.IntegerField(blank=True, help_text=b'\n            How is qualification determined?  By absolute score or relative rank?', null=True, choices=[(1, b'Score'), (2, b'Rank')]),
        ),
        migrations.AlterField(
            model_name='contest',
            name='qual_score',
            field=models.FloatField(help_text=b"\n            If the qual type is 'score', enter the cutoff  in percentile.", null=True, blank=True),
        ),
    ]
