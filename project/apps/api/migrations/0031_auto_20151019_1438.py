# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_auto_20151019_0920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='drcj',
        ),
        migrations.AddField(
            model_name='contest',
            name='admin',
            field=models.ForeignKey(related_name='admin_contests', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', help_text=b'\n            The DRCJ for the contest.', null=True),
        ),
        migrations.AddField(
            model_name='contest',
            name='rep',
            field=models.ForeignKey(related_name='rep_contests', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', help_text=b'\n            The CA for the contest.', null=True),
        ),
    ]
