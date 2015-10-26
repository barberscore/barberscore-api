# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0066_auto_20151025_1906'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Song',
            new_name='Tune',
        ),
        migrations.RenameField(
            model_name='catalog',
            old_name='song',
            new_name='tune',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='song',
            new_name='tune',
        ),
        migrations.AlterUniqueTogether(
            name='catalog',
            unique_together=set([('person', 'tune')]),
        ),
    ]
