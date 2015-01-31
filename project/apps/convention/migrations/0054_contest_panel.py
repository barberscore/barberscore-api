# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0053_contestant_running_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='panel',
            field=models.IntegerField(default=5, help_text=b'\n            Size of the judging panel (typically\n            three or five.)'),
            preserve_default=True,
        ),
    ]
