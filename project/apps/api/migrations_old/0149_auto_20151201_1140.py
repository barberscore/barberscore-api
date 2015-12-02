# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0148_remove_performance_day'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='day',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='day',
            name='contest',
        ),
        migrations.RemoveField(
            model_name='day',
            name='convention',
        ),
        migrations.DeleteModel(
            name='Day',
        ),
    ]
