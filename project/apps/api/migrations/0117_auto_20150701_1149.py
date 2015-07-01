# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0116_contestant_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='P_baritone',
            field=models.ForeignKey(related_name='P_contestants_baritone', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='P_bass',
            field=models.ForeignKey(related_name='P_contestants_bass', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='P_director',
            field=models.ForeignKey(related_name='P_contestants', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='P_lead',
            field=models.ForeignKey(related_name='P_contestants_lead', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='P_tenor',
            field=models.ForeignKey(related_name='P_contestants_tenor', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='P_baritone',
            field=models.ForeignKey(related_name='P_groups_baritone', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='P_bass',
            field=models.ForeignKey(related_name='P_groups_bass', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='P_director',
            field=models.ForeignKey(related_name='P_groups', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='P_lead',
            field=models.ForeignKey(related_name='P_groups_lead', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='P_tenor',
            field=models.ForeignKey(related_name='P_groups_tenor', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
    ]
