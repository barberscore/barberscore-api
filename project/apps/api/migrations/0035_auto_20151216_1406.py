# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_judge_round'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='common_name',
            field=models.CharField(default=b'', max_length=255, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='is_judge',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
