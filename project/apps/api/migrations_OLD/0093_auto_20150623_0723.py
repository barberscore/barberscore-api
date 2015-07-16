# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0092_auto_20150622_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='baritone',
            field=models.ForeignKey(related_name='contestants_baritone', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Singer', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='bass',
            field=models.ForeignKey(related_name='contestants_bass', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Singer', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='director',
            field=models.ForeignKey(related_name='contestants', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Director', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='lead',
            field=models.ForeignKey(related_name='contestants_lead', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Singer', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='tenor',
            field=models.ForeignKey(related_name='contestants_tenor', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Singer', null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='baritone',
            field=models.ForeignKey(related_name='baritone_groups', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Singer', help_text=b'Baritone', null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='bass',
            field=models.ForeignKey(related_name='bass_groups', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Singer', help_text=b'Bass', null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='lead',
            field=models.ForeignKey(related_name='lead_groups', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Singer', help_text=b'Lead', null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='tenor',
            field=models.ForeignKey(related_name='tenor_groups', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Singer', help_text=b'Tenor', null=True),
        ),
    ]
