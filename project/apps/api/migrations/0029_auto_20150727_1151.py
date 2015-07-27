# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_auto_20150727_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spot',
            name='name',
            field=models.CharField(unique=True, max_length=200),
        ),
    ]
