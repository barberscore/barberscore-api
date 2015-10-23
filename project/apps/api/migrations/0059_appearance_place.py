# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0058_auto_20151022_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='appearance',
            name='place',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
