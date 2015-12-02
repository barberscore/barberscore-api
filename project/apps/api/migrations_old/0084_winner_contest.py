# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0083_auto_20151027_2112'),
    ]

    operations = [
        migrations.AddField(
            model_name='winner',
            name='contest',
            field=models.ForeignKey(related_name='winners', blank=True, to='api.Contest', null=True),
        ),
    ]
