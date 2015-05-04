# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20150504_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appearance',
            name='place',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='appearance',
            name='seed',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
