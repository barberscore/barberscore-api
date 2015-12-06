# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20151205_1128'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='award',
            unique_together=set([('level', 'kind', 'year', 'goal', 'organization', 'contest')]),
        ),
    ]
