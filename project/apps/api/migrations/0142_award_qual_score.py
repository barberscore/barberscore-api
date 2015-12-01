# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0141_award_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='qual_score',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
