# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_auto_20151216_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'New'), (10, b'Active'), (20, b'Inactive'), (30, b'Retired'), (40, b'Deceased'), (50, b'Possible Stix Duplicate')]),
        ),
    ]
