# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0140_award_rounds'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='level',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'International'), (2, b'District'), (3, b'Division')]),
        ),
    ]
