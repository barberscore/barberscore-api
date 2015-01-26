# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_auto_20150126_1056'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chorusperformance',
            options={'ordering': ['contest', 'round', 'queue']},
        ),
        migrations.AlterModelOptions(
            name='contest',
            options={'ordering': ['-year', 'level', 'kind']},
        ),
        migrations.AlterModelOptions(
            name='quartetperformance',
            options={'ordering': ['contest', 'round', 'queue']},
        ),
        migrations.RenameField(
            model_name='chorusperformance',
            old_name='appearance',
            new_name='queue',
        ),
        migrations.RenameField(
            model_name='quartetperformance',
            old_name='appearance',
            new_name='queue',
        ),
    ]
