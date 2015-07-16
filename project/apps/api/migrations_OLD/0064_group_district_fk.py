# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0063_auto_20150618_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='district_fk',
            field=models.ForeignKey(blank=True, to='api.District', null=True),
        ),
    ]
