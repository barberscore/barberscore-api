# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0076_auto_20150619_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='level',
            field=models.IntegerField(default=1, choices=[(1, b'International'), (2, b'District'), (3, b'Regional'), (4, b'Prelims')]),
        ),
    ]
