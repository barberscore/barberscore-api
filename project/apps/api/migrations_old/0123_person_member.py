# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0122_auto_20151112_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='member',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
