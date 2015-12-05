# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20151201_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='kind',
            field=models.IntegerField(choices=[(1, b'Finals'), (2, b'Semis'), (3, b'Quarters')]),
        ),
        migrations.AlterField(
            model_name='session',
            name='panel',
            field=models.ForeignKey(related_name='sessions', to='api.Panel'),
        ),
    ]
