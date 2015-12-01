# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0143_auto_20151130_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='goal',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Championship'), (2, b'Qualifier')]),
        ),
        migrations.AlterField(
            model_name='award',
            name='kind',
            field=models.IntegerField(choices=[(1, b'Quartet'), (2, b'Chorus'), (3, b'Senior'), (4, b'Collegiate')]),
        ),
    ]
