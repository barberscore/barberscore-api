# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_auto_20150727_1129'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='spot',
            unique_together=set([('bhs_arranger', 'bhs_songname')]),
        ),
    ]
