# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0141_auto_20151201_0827'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='convention',
            field=models.ForeignKey(related_name='contestants', blank=True, to='api.Convention', null=True),
        ),
    ]
