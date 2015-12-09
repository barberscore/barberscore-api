# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_auto_20151209_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='parent',
            field=models.ForeignKey(blank=True, to='api.Contest', null=True),
        ),
    ]
