# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20150721_1050'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='chart',
            unique_together=set([('song', 'arranger', 'is_parody', 'is_medley')]),
        ),
        migrations.AlterUniqueTogether(
            name='director',
            unique_together=set([('contestant', 'person')]),
        ),
        migrations.AlterUniqueTogether(
            name='performance',
            unique_together=set([('contestant', 'round', 'order')]),
        ),
        migrations.AlterUniqueTogether(
            name='singer',
            unique_together=set([('contestant', 'person')]),
        ),
    ]
