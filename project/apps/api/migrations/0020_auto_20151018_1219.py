# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20151018_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='bracket',
            field=models.IntegerField(default=1, help_text=b'\n            Bracket size'),
        ),
        migrations.AddField(
            model_name='contest',
            name='drcj',
            field=models.ForeignKey(related_name='contests', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', help_text=b'\n            The director for the contest.', null=True),
        ),
        migrations.AddField(
            model_name='contest',
            name='goal',
            field=models.IntegerField(default=1, help_text=b'\n            The objective of the contest'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='level',
            field=models.IntegerField(default=1, help_text=b'\n            The level of the contest (currently only International is supported.)', choices=[(1, b'International'), (2, b'District'), (4, b'Prelims')]),
        ),
    ]
