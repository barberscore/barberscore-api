# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0144_auto_20151126_0534'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contestant',
            options={'ordering': ('-entrant__contest__year', 'place')},
        ),
        migrations.RemoveField(
            model_name='entrant',
            name='convention',
        ),
        migrations.RemoveField(
            model_name='entrant',
            name='place',
        ),
    ]
