# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_singer_old_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='quartet',
            name='old_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
