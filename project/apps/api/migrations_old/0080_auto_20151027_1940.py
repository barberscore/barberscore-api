# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0079_auto_20151027_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (10, b'Active'), (20, b'Inactive')]),
        ),
        migrations.AddField(
            model_name='person',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (10, b'Active'), (20, b'Inactive'), (30, b'Retired'), (40, b'Deceased')]),
        ),
    ]
