# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0065_contest_district_fk'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='name',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
