# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0043_auto_20151217_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='contest',
            field=models.ForeignKey(related_name='contestants', to='api.Contest'),
        ),
    ]
