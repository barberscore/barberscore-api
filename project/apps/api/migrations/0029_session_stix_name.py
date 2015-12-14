# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_auto_20151214_0837'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='stix_name',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
    ]
