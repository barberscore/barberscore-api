# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_auto_20151203_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='panel',
            field=models.ForeignKey(related_name='contests', to='api.Panel'),
        ),
    ]
