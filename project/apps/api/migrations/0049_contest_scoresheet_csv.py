# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0048_auto_20150131_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='scoresheet_csv',
            field=models.FileField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
    ]
