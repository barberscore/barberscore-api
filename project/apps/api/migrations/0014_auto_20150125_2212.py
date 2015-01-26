# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20150125_2056'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chorusperformance',
            options={'ordering': ['chorus']},
        ),
        migrations.AlterModelOptions(
            name='singer',
            options={'ordering': ['name']},
        ),
    ]
