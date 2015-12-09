# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_auto_20151209_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='contest',
            field=mptt.fields.TreeForeignKey(related_name='contestants', to='api.Contest'),
        ),
    ]
