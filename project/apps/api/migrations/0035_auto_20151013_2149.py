# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_auto_20151013_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='category',
            field=models.IntegerField(choices=[(1, b'Music'), (2, b'Presentation'), (3, b'Singing'), (4, b'Admin')]),
        ),
    ]
