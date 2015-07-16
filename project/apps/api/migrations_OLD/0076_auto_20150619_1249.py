# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0075_auto_20150619_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='kind',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'International'), (2, b'Midwinter'), (3, b'Fall'), (4, b'Spring'), (5, b'Pacific')]),
        ),
    ]
