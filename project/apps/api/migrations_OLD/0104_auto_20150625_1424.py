# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0103_auto_20150624_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='baritone',
            field=models.ForeignKey(related_name='groups_baritone', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Singer', null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='bass',
            field=models.ForeignKey(related_name='groups_bass', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Singer', null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='director',
            field=models.ForeignKey(related_name='groups', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Director', null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='lead',
            field=models.ForeignKey(related_name='groups_lead', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Singer', null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='tenor',
            field=models.ForeignKey(related_name='groups_tenor', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Singer', null=True),
        ),
    ]
