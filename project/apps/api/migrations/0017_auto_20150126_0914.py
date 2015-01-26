# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20150126_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='quartetmembership',
            name='from_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quartetmembership',
            name='to_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
