# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_auto_20151204_1451'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='judge',
            options={'ordering': ('contest', 'category', 'slot')},
        ),
        migrations.RenameField(
            model_name='judge',
            old_name='kind',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='score',
            old_name='kind',
            new_name='category',
        ),
        migrations.AlterUniqueTogether(
            name='judge',
            unique_together=set([('contest', 'category', 'slot')]),
        ),
    ]
