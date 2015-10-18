# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20151017_1231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='contest',
        ),
        migrations.RemoveField(
            model_name='event',
            name='contestant',
        ),
        migrations.RemoveField(
            model_name='event',
            name='convention',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
    ]
