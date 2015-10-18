# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20151018_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='status_monitor',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, help_text=b'Status last updated', monitor=b'status'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='bracket',
            field=models.IntegerField(default=1, help_text=b'\n            Bracket size', choices=[(1, b'Finals'), (2, b'Semis'), (3, b'Quarters')]),
        ),
        migrations.AlterField(
            model_name='contest',
            name='goal',
            field=models.IntegerField(default=1, help_text=b'\n            The objective of the contest', choices=[(1, b'Champion'), (2, b'Qualifier')]),
        ),
    ]
