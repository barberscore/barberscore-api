# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0050_auto_20151021_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='history',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (10, b'Partial'), (50, b'Complete')]),
        ),
        migrations.AddField(
            model_name='contest',
            name='history_monitor',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, help_text=b'History last updated', monitor=b'history'),
        ),
    ]
