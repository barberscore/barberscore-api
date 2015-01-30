# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0042_auto_20150129_2132'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chorusperformance',
            options={'ordering': ['contest', 'round', 'chorus']},
        ),
        migrations.AlterModelOptions(
            name='quartetmember',
            options={'ordering': ['quartet', 'part', 'singer', 'contest']},
        ),
        migrations.AlterModelOptions(
            name='quartetperformance',
            options={'ordering': ['contest', 'round', 'quartet']},
        ),
    ]
