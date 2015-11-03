# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0092_auto_20151102_0446'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='is_judge',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='contest',
            name='panel',
            field=models.IntegerField(blank=True, help_text=b'\n            Size of the judging panel (typically three or five.)', null=True, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]),
        ),
        migrations.AlterField(
            model_name='contest',
            name='rounds',
            field=models.IntegerField(blank=True, help_text=b'\n            Number of rounds', null=True, choices=[(3, 3), (2, 2), (1, 1)]),
        ),
        migrations.AlterField(
            model_name='judge',
            name='name',
            field=models.CharField(unique=True, max_length=255, editable=False),
        ),
    ]
