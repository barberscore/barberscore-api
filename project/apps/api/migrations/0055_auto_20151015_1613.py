# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0054_auto_20151015_1606'),
    ]

    operations = [
        migrations.RenameField(
            model_name='performance',
            old_name='arrangement',
            new_name='catalog',
        ),
        migrations.AlterField(
            model_name='catalog',
            name='arranger',
            field=models.ForeignKey(related_name='catalogs', blank=True, to='api.Person', null=True),
        ),
        migrations.AlterField(
            model_name='catalog',
            name='song',
            field=models.ForeignKey(related_name='catalogs', blank=True, to='api.Song', null=True),
        ),
    ]
