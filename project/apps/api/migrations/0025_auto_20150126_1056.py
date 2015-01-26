# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20150126_1048'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chorus',
            options={'ordering': ('name',), 'verbose_name_plural': 'choruses'},
        ),
        migrations.AlterModelOptions(
            name='chorusperformance',
            options={'ordering': ['contest', 'round', 'appearance']},
        ),
        migrations.AlterModelOptions(
            name='contest',
            options={'ordering': ['year', 'level', 'kind']},
        ),
        migrations.AlterModelOptions(
            name='quartetperformance',
            options={'ordering': ['contest', 'round', 'appearance']},
        ),
    ]
