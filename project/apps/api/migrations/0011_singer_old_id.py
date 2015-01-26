# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20150124_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='singer',
            name='old_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
