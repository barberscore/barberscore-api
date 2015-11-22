# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0130_performance_entrant'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrant',
            name='convention',
            field=models.ForeignKey(related_name='entrants', blank=True, to='api.Convention', null=True),
        ),
    ]
