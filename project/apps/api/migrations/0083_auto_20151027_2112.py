# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0082_auto_20151027_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winner',
            name='award',
            field=models.ForeignKey(related_name='winners', to='api.Award'),
        ),
    ]
