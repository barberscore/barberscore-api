# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0061_auto_20151024_0522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appearance',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (1, b'Qualified'), (2, b'Current'), (3, b'Complete'), (4, b'Flagged')]),
        ),
        migrations.AlterField(
            model_name='performance',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (1, b'Ready'), (2, b'Current'), (3, b'Complete'), (4, b'Flagged')]),
        ),
    ]
