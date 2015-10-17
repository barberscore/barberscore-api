# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20151017_0726'),
    ]

    operations = [
        migrations.AddField(
            model_name='judge',
            name='district',
            field=models.ForeignKey(related_name='judges', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.District', null=True),
        ),
    ]
