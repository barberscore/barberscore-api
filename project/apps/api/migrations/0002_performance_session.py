# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='session',
            field=models.ForeignKey(related_name='performances', blank=True, to='api.Session', null=True),
        ),
    ]
