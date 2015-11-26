# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0139_auto_20151125_1512'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contestant',
            unique_together=set([('entrant', 'contest')]),
        ),
        migrations.RemoveField(
            model_name='contestant',
            name='group',
        ),
    ]
