# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20151203_1005'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contestant',
            options={'ordering': ('panel', 'group')},
        ),
        migrations.AlterModelOptions(
            name='panel',
            options={'ordering': ('convention', 'kind')},
        ),
        migrations.AlterModelOptions(
            name='performance',
            options={'ordering': ('position',)},
        ),
        migrations.AlterModelOptions(
            name='ranking',
            options={'ordering': ('contest', 'contestant')},
        ),
        migrations.AlterModelOptions(
            name='session',
            options={'ordering': ('panel', 'kind')},
        ),
    ]
