# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0121_auto_20160213_0805'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='award',
            unique_together=set([('organization', 'long_name', 'kind')]),
        ),
        migrations.RemoveField(
            model_name='award',
            name='year',
        ),
    ]
