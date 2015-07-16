# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0095_auto_20150623_0943'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contest',
            unique_together=set([('level', 'kind', 'year', 'district')]),
        ),
    ]
