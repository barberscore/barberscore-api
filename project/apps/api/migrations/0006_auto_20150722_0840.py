# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20150721_2142'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chart',
            old_name='arranger',
            new_name='arranger_OLD',
        ),
        migrations.RenameField(
            model_name='chart',
            old_name='arrangers',
            new_name='arrangers_OLD',
        ),
        migrations.AlterUniqueTogether(
            name='chart',
            unique_together=set([('song', 'arranger_OLD', 'is_parody', 'is_medley')]),
        ),
    ]
