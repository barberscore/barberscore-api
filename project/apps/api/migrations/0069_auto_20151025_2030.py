# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0068_auto_20151025_2025'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='score',
            options={'ordering': ('judge', 'song__order')},
        ),
        migrations.AlterField(
            model_name='arranger',
            name='song',
            field=models.ForeignKey(related_name='arrangers', blank=True, to='api.Song', null=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='song',
            field=models.ForeignKey(related_name='scores', blank=True, to='api.Song', null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='appearance',
            field=models.ForeignKey(related_name='songs', blank=True, to='api.Appearance', null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='catalog',
            field=models.ForeignKey(related_name='songs', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Catalog', null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='tune',
            field=models.ForeignKey(related_name='songs', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Tune', null=True),
        ),
    ]
