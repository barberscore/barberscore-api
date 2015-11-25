# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0136_auto_20151125_0615'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entrant',
            name='convention',
        ),
        migrations.RemoveField(
            model_name='entrant',
            name='place',
        ),
        migrations.AlterUniqueTogether(
            name='performance',
            unique_together=set([('session', 'entrant')]),
        ),
        migrations.RemoveField(
            model_name='performance',
            name='contestant',
        ),
    ]
