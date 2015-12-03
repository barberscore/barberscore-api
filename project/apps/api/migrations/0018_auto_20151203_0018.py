# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_contestant_panel'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contestant',
            unique_together=set([('group', 'panel')]),
        ),
    ]
