# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_contest_parent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contest',
            options={},
        ),
        migrations.AddField(
            model_name='contest',
            name='lft',
            field=models.PositiveIntegerField(default=1, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contest',
            name='rght',
            field=models.PositiveIntegerField(default=1, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contest',
            name='tree_id',
            field=models.PositiveIntegerField(default=1, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contest',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='children', blank=True, to='api.Contest', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='contest',
            unique_together=set([]),
        ),
    ]
