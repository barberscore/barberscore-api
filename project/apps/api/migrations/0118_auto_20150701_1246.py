# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0117_auto_20150701_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='P_baritone',
            field=models.ForeignKey(related_name='contestants_P_baritone', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='P_bass',
            field=models.ForeignKey(related_name='contestants_P_bass', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='P_director',
            field=models.ForeignKey(related_name='contestants_P_director', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='P_lead',
            field=models.ForeignKey(related_name='contestants_P_lead', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='P_tenor',
            field=models.ForeignKey(related_name='contestants_P_tenor', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
    ]
