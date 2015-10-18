# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_convention_status_monitor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='status',
            field=models.IntegerField(default=0, help_text=b'The current status', choices=[(0, b'New'), (1, b'Structured'), (2, b'Current'), (3, b'Complete')]),
        ),
        migrations.AlterField(
            model_name='convention',
            name='status_monitor',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, help_text=b'Status last updated', editable=False, monitor=b'status'),
        ),
    ]
