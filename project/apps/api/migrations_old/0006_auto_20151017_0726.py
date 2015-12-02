# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20151017_0635'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='performance',
            options={'ordering': ['appearance', 'order']},
        ),
        migrations.AlterUniqueTogether(
            name='performance',
            unique_together=set([('appearance', 'order')]),
        ),
        migrations.RemoveField(
            model_name='performance',
            name='contestant',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='session',
        ),
    ]
