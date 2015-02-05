# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_performance_men'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupfinish',
            name='group',
            field=models.ForeignKey(related_name='finishes', blank=True, to='api.Group', null=True),
        ),
    ]
