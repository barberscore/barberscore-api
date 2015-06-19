# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0064_group_district_fk'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='district_fk',
            field=models.ForeignKey(blank=True, to='api.District', null=True),
        ),
    ]
