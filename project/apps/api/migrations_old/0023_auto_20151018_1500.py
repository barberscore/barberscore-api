# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20151018_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='appearance',
            name='status_monitor',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, help_text=b'Status last updated', monitor=b'status'),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (1, b'Qualified'), (2, b'Current'), (3, b'Complete')]),
        ),
    ]
