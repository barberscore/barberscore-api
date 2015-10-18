# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_convention_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='convention',
            name='status_monitor',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor=b'status'),
        ),
    ]
