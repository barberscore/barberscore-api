# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0132_auto_20151128_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='contest',
            field=models.ForeignKey(related_name='awards', to='api.Contest'),
        ),
        migrations.AlterField(
            model_name='award',
            name='kind',
            field=models.IntegerField(choices=[(1, b'Championship'), (2, b'Qualifier')]),
        ),
    ]
