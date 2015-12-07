# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20151206_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='award',
            field=models.ForeignKey(related_name='contestants', to='api.Award'),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='performer',
            field=models.ForeignKey(related_name='contestants', to='api.Performer'),
        ),
    ]
