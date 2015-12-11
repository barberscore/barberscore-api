# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_convention_level'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='session',
            options={},
        ),
        migrations.AddField(
            model_name='session',
            name='level',
            field=models.IntegerField(blank=True, help_text=b'\n            The contest round.', null=True, choices=[(1, b'Finals'), (2, b'Semis'), (3, b'Quarters')]),
        ),
        migrations.AddField(
            model_name='session',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='children', blank=True, to='api.Session', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='session',
            unique_together=set([]),
        ),
    ]
