# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0120_auto_20160212_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='is_senior',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='group',
            name='is_youth',
            field=models.BooleanField(default=False),
        ),
    ]
