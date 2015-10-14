# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0038_auto_20151014_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judge',
            name='person',
            field=models.ForeignKey(related_name='contests', on_delete=django.db.models.deletion.SET_NULL, to='api.Person', null=True),
        ),
    ]
