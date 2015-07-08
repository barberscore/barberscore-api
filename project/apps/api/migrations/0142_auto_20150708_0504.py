# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0141_auto_20150707_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='convention',
            field=models.ForeignKey(related_name='contests', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Convention', null=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.District', null=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='level',
            field=models.IntegerField(default=1, choices=[(1, b'International')]),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='district',
            field=models.ForeignKey(related_name='contestants', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.District', null=True),
        ),
        migrations.AlterField(
            model_name='convention',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.District', null=True),
        ),
        migrations.AlterField(
            model_name='director',
            name='contestant',
            field=models.ForeignKey(related_name='directors', to='api.Contestant'),
        ),
        migrations.AlterField(
            model_name='director',
            name='person',
            field=models.ForeignKey(related_name='choruses', to='api.Person'),
        ),
    ]
