# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20150722_0844'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='chart',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='chart',
            name='arranger_OLD',
        ),
        migrations.RemoveField(
            model_name='chart',
            name='arrangers_OLD',
        ),
    ]
