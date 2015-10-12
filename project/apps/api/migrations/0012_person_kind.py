# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20151012_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='kind',
            field=models.IntegerField(default=1, choices=[(1, b'Individual'), (2, b'Team')]),
        ),
    ]
