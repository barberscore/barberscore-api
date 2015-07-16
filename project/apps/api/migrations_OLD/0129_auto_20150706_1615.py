# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0128_auto_20150706_0619'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='performance',
            options={'ordering': ['contestant', 'round', 'order']},
        ),
    ]
