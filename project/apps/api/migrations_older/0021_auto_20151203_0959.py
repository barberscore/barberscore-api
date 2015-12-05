# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20151203_0134'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contestant',
            options={'ordering': ('panel', 'group')},
        ),
    ]
