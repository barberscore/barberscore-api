# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0103_auto_20151108_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='organization',
            field=mptt.fields.TreeForeignKey(related_name='contests', to='api.Organization'),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='organization',
            field=mptt.fields.TreeForeignKey(related_name='contestants', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='convention',
            name='organization',
            field=mptt.fields.TreeForeignKey(help_text=b"\n            The district for the convention.  If International, this is 'BHS'.", to='api.Organization'),
        ),
        migrations.AlterField(
            model_name='panelist',
            name='organization',
            field=mptt.fields.TreeForeignKey(related_name='panelists', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='organization',
            field=mptt.fields.TreeForeignKey(blank=True, to='api.Organization', null=True),
        ),
    ]
