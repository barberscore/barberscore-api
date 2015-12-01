# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0149_auto_20151201_1140'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='session',
            options={'ordering': ['panel', 'kind']},
        ),
        migrations.AlterUniqueTogether(
            name='session',
            unique_together=set([('panel', 'kind')]),
        ),
        migrations.RemoveField(
            model_name='session',
            name='contest',
        ),
    ]
