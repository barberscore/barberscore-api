# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0140_auto_20151125_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='director',
            name='entrant',
            field=models.ForeignKey(related_name='directors', blank=True, to='api.Entrant', null=True),
        ),
        migrations.AddField(
            model_name='singer',
            name='entrant',
            field=models.ForeignKey(related_name='singers', blank=True, to='api.Entrant', null=True),
        ),
    ]
