# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0047_remove_score_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='slots',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
