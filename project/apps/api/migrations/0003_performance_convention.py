# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_performance_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='convention',
            field=models.ForeignKey(related_name='performances', blank=True, to='api.Convention', null=True),
        ),
    ]
