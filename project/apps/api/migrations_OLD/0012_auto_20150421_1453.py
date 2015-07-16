# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20150421_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='convention',
            field=models.ForeignKey(to='api.Convention'),
        ),
    ]
