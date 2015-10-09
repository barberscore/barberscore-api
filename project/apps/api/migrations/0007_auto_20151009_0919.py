# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20151009_0546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='order',
            field=models.IntegerField(choices=[(1, b'First'), (2, b'Second')]),
        ),
    ]
