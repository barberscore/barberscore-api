# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0052_auto_20151015_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judge',
            name='person',
            field=models.ForeignKey(related_name='panels', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Person', null=True),
        ),
    ]
