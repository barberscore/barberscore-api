# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_auto_20150726_2028'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='spot',
            unique_together=set([('bhs_arranger', 'bhs_songname', 'is_parody')]),
        ),
    ]
