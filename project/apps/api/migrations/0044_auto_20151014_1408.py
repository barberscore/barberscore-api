# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0043_auto_20151014_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='contest',
            field=models.ForeignKey(related_name='performances', blank=True, to='api.Contest', null=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='contestant',
            field=models.ForeignKey(related_name='performances', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Contestant', null=True),
        ),
    ]
