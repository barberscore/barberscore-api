# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_auto_20151216_1406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='stix_name',
        ),
        migrations.AddField(
            model_name='round',
            name='stix_name',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
    ]
