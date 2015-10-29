# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0086_auto_20151028_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (10, b'Structured'), (15, b'Ready'), (20, b'Current'), (25, b'Review'), (30, b'Complete')]),
        ),
        migrations.AlterField(
            model_name='performance',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (10, b'Structured'), (15, b'Ready'), (20, b'Current'), (25, b'Review'), (30, b'Complete')]),
        ),
        migrations.AlterField(
            model_name='score',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (10, b'Flagged'), (20, b'Passed'), (30, b'Complete')]),
        ),
        migrations.AlterField(
            model_name='session',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (10, b'Structured'), (15, b'Ready'), (20, b'Current'), (25, b'Review'), (30, b'Complete')]),
        ),
        migrations.AlterField(
            model_name='song',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (10, b'Flagged'), (20, b'Passed'), (30, b'Complete')]),
        ),
    ]
