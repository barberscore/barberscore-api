# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_auto_20151216_0112'),
    ]

    operations = [
        migrations.AddField(
            model_name='judge',
            name='round',
            field=models.ForeignKey(related_name='judges', blank=True, to='api.Round', null=True),
        ),
    ]
