# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20151018_0930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='convention',
            name='is_active',
        ),
        migrations.AddField(
            model_name='contest',
            name='status_monitor',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, help_text=b'Status last updated', monitor=b'status'),
        ),
    ]
