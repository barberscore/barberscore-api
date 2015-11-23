# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0132_auto_20151122_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrant',
            name='contest',
            field=models.ForeignKey(related_name='entrants', blank=True, to='api.Contest', null=True),
        ),
    ]
