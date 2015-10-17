# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_judge_district'),
    ]

    operations = [
        migrations.AddField(
            model_name='judge',
            name='is_practice',
            field=models.BooleanField(default=False),
        ),
    ]
