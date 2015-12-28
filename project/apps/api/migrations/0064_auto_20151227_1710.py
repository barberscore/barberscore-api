# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0063_auto_20151224_1849'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='award',
            options={'ordering': ('organization__level', 'organization__name', 'kind', 'long_name')},
        ),
        migrations.AlterField(
            model_name='judge',
            name='slot',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performer',
            name='organization',
            field=mptt.fields.TreeForeignKey(related_name='performers', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Organization', null=True),
        ),
    ]
