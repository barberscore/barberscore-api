# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20151211_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='round',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Finals'), (2, b'Semis'), (3, b'Quarters')]),
        ),
    ]
