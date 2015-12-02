# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0071_auto_20151025_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='arranger',
            name='catalog',
            field=models.ForeignKey(blank=True, to='api.Catalog', null=True),
        ),
    ]
