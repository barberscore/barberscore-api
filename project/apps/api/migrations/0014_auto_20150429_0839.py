# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20150426_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='kind',
            field=models.IntegerField(default=1, choices=[(1, b'Summer'), (2, b'Midwinter'), (3, b'Fall'), (4, b'Spring'), (5, b'Pan-Pacific')]),
        ),
    ]
