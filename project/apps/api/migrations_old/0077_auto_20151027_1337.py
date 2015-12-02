# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0076_auto_20151027_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arranger',
            name='catalog',
            field=models.ForeignKey(related_name='arrangers', blank=True, to='api.Catalog', null=True),
        ),
    ]
