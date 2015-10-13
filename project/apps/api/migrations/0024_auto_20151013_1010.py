# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_award'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='arrangement',
            unique_together=set([('arranger', 'song')]),
        ),
    ]
