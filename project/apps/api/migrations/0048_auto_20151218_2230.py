# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0047_auto_20151218_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judge',
            name='round',
            field=models.ForeignKey(related_name='judges', to='api.Round'),
        ),
        migrations.AlterField(
            model_name='judge',
            name='session',
            field=models.ForeignKey(related_name='judges', blank=True, to='api.Session', null=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='num',
            field=models.IntegerField(),
        ),
    ]
