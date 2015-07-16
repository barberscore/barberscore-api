# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0051_auto_20150517_1033'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contestant',
            options={'ordering': ('-contest', 'place', '-score')},
        ),
        migrations.AlterModelOptions(
            name='performance',
            options={'ordering': ['contestant', 'round', 'queue', 'stagetime']},
        ),
    ]
