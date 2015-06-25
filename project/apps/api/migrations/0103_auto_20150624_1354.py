# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0102_auto_20150623_1608'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contestant',
            options={'ordering': ('-contest__year', 'place', '-score')},
        ),
    ]
