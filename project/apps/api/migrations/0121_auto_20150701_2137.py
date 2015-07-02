# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0120_auto_20150701_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='finals_draw',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='finals_stagetime',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_draw',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='quarters_stagetime',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_draw',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestant',
            name='semis_stagetime',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='baritone',
            field=models.ForeignKey(related_name='contestants_baritone', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='bass',
            field=models.ForeignKey(related_name='contestants_bass', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='director',
            field=models.ForeignKey(related_name='contestants_director', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='lead',
            field=models.ForeignKey(related_name='contestants_lead', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='tenor',
            field=models.ForeignKey(related_name='contestants_tenor', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='baritone',
            field=models.ForeignKey(related_name='groups_baritone', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='bass',
            field=models.ForeignKey(related_name='groups_bass', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='director',
            field=models.ForeignKey(related_name='groups', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='lead',
            field=models.ForeignKey(related_name='groups_lead', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='tenor',
            field=models.ForeignKey(related_name='groups_tenor', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
    ]
