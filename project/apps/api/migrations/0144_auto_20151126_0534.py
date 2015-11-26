# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0143_auto_20151126_0524'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contestant',
            unique_together=set([('entrant', 'award')]),
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='contest',
        ),
    ]
