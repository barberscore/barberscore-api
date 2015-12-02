# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0144_auto_20151201_1102'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ranking',
            unique_together=set([('contestant', 'contest')]),
        ),
        migrations.RemoveField(
            model_name='ranking',
            name='award',
        ),
    ]
