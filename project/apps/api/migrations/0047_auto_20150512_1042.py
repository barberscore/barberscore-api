# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0046_auto_20150512_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the convention.', unique=True, max_length=200),
        ),
    ]
