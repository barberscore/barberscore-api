# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0114_auto_20160211_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='award',
            field=models.ForeignKey(related_name='contestants', blank=True, to='api.Award', null=True),
        ),
    ]
