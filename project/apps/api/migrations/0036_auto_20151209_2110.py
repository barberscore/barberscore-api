# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.api.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_auto_20151209_2035'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapter',
            name='status',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='status_monitor',
        ),
        migrations.AlterField(
            model_name='chapter',
            name='code',
            field=models.CharField(blank=True, help_text=b'\n            The chapter code.', max_length=200, validators=[apps.api.validators.validate_trimmed]),
        ),
    ]
