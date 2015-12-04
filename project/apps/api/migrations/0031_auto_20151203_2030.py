# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_rename_ranking_competitor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competitor',
            name='contest',
            field=models.ForeignKey(related_name='competitors', to='api.Contest'),
        ),
        migrations.AlterField(
            model_name='competitor',
            name='contestant',
            field=models.ForeignKey(related_name='competitors', to='api.Contestant'),
        ),
    ]
