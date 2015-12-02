# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_auto_20151020_0812'),
    ]

    operations = [
        migrations.AddField(
            model_name='appearance',
            name='position',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
    ]
