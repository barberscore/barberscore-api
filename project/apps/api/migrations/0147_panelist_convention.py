# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0146_auto_20151130_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='panelist',
            name='convention',
            field=models.ForeignKey(related_name='panelists', blank=True, to='api.Convention', null=True),
        ),
    ]
