# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0059_auto_20150616_1008'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='note',
            unique_together=set([('performance', 'user')]),
        ),
    ]
