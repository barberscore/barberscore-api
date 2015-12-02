# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0089_auto_20151029_0559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (10, b'Ready'), (20, b'Current'), (30, b'Complete')]),
        ),
    ]
