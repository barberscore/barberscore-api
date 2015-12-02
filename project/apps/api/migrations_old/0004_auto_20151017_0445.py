# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20151016_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='appearance',
            name='draw',
            field=models.IntegerField(help_text=b'\n            The OA (Order of Appearance) in the contest schedule.  Specific to each session.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='appearance',
            name='start',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (1, b'Structured'), (2, b'Current'), (3, b'Complete')]),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (1, b'Qualified'), (2, b'Current'), (3, b'Complete')]),
        ),
        migrations.AlterField(
            model_name='score',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (1, b'Flagged'), (2, b'Confirmed'), (3, b'Final')]),
        ),
    ]
