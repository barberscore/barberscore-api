# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0129_auto_20151128_1504'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rank',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='rank',
            name='performance',
        ),
        migrations.RemoveField(
            model_name='rank',
            name='session',
        ),
        migrations.DeleteModel(
            name='Rank',
        ),
    ]
