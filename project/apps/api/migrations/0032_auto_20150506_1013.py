# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_auto_20150506_0940'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='performance',
            unique_together=set([('contestant', 'round')]),
        ),
    ]
