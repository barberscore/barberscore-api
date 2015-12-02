# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_session_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='panel',
            field=models.ForeignKey(related_name='contests', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Panel', null=True),
        ),
    ]
