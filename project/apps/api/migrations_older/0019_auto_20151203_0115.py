# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20151203_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='panel',
            field=models.ForeignKey(related_name='contestants', to='api.Panel'),
        ),
    ]
