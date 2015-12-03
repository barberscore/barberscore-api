# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20151203_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='convention',
            field=models.ForeignKey(related_name='contestants', blank=True, to='api.Convention', null=True),
        ),
    ]
