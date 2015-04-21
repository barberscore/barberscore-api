# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20150421_1347'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contest',
            unique_together=set([('kind', 'convention', 'year', 'district')]),
        ),
    ]
