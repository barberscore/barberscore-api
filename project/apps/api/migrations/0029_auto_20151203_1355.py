# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_rename_panelist_to_judge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='score',
            old_name='panelist',
            new_name='judge',
        ),
        migrations.AlterField(
            model_name='judge',
            name='organization',
            field=mptt.fields.TreeForeignKey(related_name='judges', blank=True, to='api.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='judge',
            name='panel',
            field=models.ForeignKey(related_name='judges', to='api.Panel'),
        ),
    ]
