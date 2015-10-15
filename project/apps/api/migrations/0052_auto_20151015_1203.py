# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0051_auto_20151015_1009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contestant',
            name='end',
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='start',
        ),
        migrations.RemoveField(
            model_name='convention',
            name='end',
        ),
        migrations.RemoveField(
            model_name='convention',
            name='start',
        ),
        migrations.RemoveField(
            model_name='performance',
            name='contest',
        ),
    ]
