# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0137_auto_20151125_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrant',
            name='convention',
            field=models.ForeignKey(related_name='entrants', blank=True, to='api.Convention', null=True),
        ),
        migrations.AddField(
            model_name='entrant',
            name='place',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='contestant',
            field=models.ForeignKey(related_name='performances', blank=True, to='api.Contestant', null=True),
        ),
    ]
