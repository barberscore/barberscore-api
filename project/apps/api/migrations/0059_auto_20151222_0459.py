# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0058_auto_20151221_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performer',
            name='organization',
            field=mptt.fields.TreeForeignKey(related_name='performers', on_delete=django.db.models.deletion.SET_NULL, blank=True, editable=False, to='api.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='performer',
            name='prelim',
            field=models.FloatField(help_text=b'\n            The incoming prelim score.', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='performer',
            name='seed',
            field=models.IntegerField(help_text=b'\n            The incoming rank based on prelim score.', null=True, editable=False, blank=True),
        ),
    ]
