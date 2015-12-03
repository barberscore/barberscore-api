# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20151203_0115'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contestant',
            options={'ordering': ('panel', 'group__kind', 'group')},
        ),
        migrations.AlterUniqueTogether(
            name='contestant',
            unique_together=set([('group', 'panel')]),
        ),
    ]
