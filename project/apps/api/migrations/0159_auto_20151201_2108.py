# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0158_auto_20151201_1703'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='panelist',
            unique_together=set([('panel', 'category', 'slot')]),
        ),
    ]
