# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0078_auto_20151027_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (10, b'Structured'), (20, b'Current'), (30, b'Complete')]),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (10, b'Qualified'), (20, b'Current'), (30, b'Complete')]),
        ),
        migrations.AlterField(
            model_name='convention',
            name='status',
            field=models.IntegerField(default=0, help_text=b'The current status', choices=[(0, b'New'), (10, b'Structured'), (20, b'Current'), (30, b'Complete')]),
        ),
        migrations.AlterField(
            model_name='performance',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (10, b'Qualified'), (20, b'Current'), (30, b'Complete'), (40, b'Flagged')]),
        ),
        migrations.AlterField(
            model_name='score',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (10, b'Flagged'), (20, b'Confirmed'), (30, b'Final')]),
        ),
        migrations.AlterField(
            model_name='session',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (10, b'Structured'), (20, b'Current'), (30, b'Complete')]),
        ),
        migrations.AlterField(
            model_name='song',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (10, b'Ready'), (20, b'Current'), (30, b'Complete'), (40, b'Flagged')]),
        ),
    ]
