# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_auto_20151216_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='long_name',
            field=models.CharField(default=b'', max_length=200, blank=True),
        ),
    ]
