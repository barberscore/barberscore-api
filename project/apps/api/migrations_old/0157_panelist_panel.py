# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0156_auto_20151201_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='panelist',
            name='panel',
            field=models.ForeignKey(related_name='panelists', blank=True, to='api.Panel', null=True),
        ),
    ]
