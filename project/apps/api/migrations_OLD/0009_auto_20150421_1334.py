# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20150308_0942'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='convention',
            unique_together=set([('district', 'kind', 'year')]),
        ),
    ]
