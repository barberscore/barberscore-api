# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0093_auto_20151103_1014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='is_judge',
        ),
        migrations.AddField(
            model_name='person',
            name='judge',
            field=models.IntegerField(blank=True, null=True, choices=[(0, b'Admin'), (1, b'Music'), (2, b'Presentation'), (3, b'Singing'), (4, b'Music Candidate'), (5, b'Presentation Candidate'), (6, b'Singing Candidate'), (7, b'Music Composite'), (8, b'Presentation Composite'), (9, b'Singing Composite')]),
        ),
        migrations.AddField(
            model_name='person',
            name='judge_monitor',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, help_text=b'Certification last updated', monitor=b'judge'),
        ),
    ]
