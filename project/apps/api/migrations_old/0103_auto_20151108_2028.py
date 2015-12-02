# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0102_auto_20151108_1414'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='score',
            options={'ordering': ('panelist', 'song__order')},
        ),
        migrations.RenameField(
            model_name='score',
            old_name='judge',
            new_name='panelist',
        ),
        migrations.AlterField(
            model_name='panelist',
            name='contest',
            field=models.ForeignKey(related_name='panelists', to='api.Contest'),
        ),
        migrations.AlterField(
            model_name='panelist',
            name='organization',
            field=models.ForeignKey(related_name='panelists', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Organization', null=True),
        ),
    ]
