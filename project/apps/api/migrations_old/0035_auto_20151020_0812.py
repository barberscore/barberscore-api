# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_auto_20151020_0558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appearance',
            name='draw',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
