# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20151201_2252'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='performance',
            unique_together=set([('session', 'contestant')]),
        ),
    ]
