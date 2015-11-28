# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0149_remove_performance_contestant'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='kind',
            field=models.IntegerField(blank=True, null=True, choices=[(10, b'Championship'), (20, b'Qualifier'), (30, b'Novice'), (40, b'Other')]),
        ),
    ]
