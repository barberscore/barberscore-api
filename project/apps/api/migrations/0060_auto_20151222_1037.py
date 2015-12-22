# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0059_auto_20151222_0459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='award',
            field=models.ForeignKey(related_name='contests', to='api.Award'),
        ),
    ]
