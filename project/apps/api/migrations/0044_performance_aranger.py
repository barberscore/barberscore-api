# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0043_auto_20151020_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='aranger',
            field=models.ForeignKey(related_name='performances', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='api.Arranger', null=True),
        ),
    ]
