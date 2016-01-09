# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0068_auto_20160107_1901'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contestant',
            options={'ordering': ('contest', 'place')},
        ),
    ]
