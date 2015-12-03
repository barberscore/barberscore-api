# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20151202_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='panel',
            field=models.ForeignKey(related_name='contestants', blank=True, to='api.Panel', null=True),
        ),
    ]
