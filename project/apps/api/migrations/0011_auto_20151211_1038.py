# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20151210_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arranger',
            name='catalog',
            field=models.ForeignKey(related_name='arrangers', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Catalog', null=True),
        ),
        migrations.AlterField(
            model_name='catalog',
            name='tune',
            field=models.ForeignKey(related_name='catalogs', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Tune', null=True),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='organization',
            field=mptt.fields.TreeForeignKey(related_name='chapters', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='children', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Contest', null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='chapter',
            field=models.ForeignKey(related_name='groups', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Chapter', null=True),
        ),
        migrations.AlterField(
            model_name='judge',
            name='organization',
            field=mptt.fields.TreeForeignKey(related_name='judges', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='children', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='convention',
            field=models.ForeignKey(related_name='performances', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Convention', null=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='session',
            field=models.ForeignKey(related_name='performances', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Session', null=True),
        ),
        migrations.AlterField(
            model_name='performer',
            name='organization',
            field=mptt.fields.TreeForeignKey(related_name='performers', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='organization',
            field=mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Organization', null=True),
        ),
    ]
