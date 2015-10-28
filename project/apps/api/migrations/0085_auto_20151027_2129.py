# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0084_winner_contest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winner',
            name='contest',
            field=models.ForeignKey(related_name='winners', to='api.Contest'),
        ),
    ]
