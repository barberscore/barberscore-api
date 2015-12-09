# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.api.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_judge_panel_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='contest_id',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='code',
            field=models.CharField(blank=True, help_text=b'\n            The chapter code (only for choruses).', max_length=200, validators=[apps.api.validators.validate_trimmed]),
        ),
    ]
