# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0041_auto_20150728_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duplicategroup',
            name='parent',
            field=models.ForeignKey(related_name='duplicates', to='api.Group'),
        ),
        migrations.AlterField(
            model_name='duplicateperson',
            name='parent',
            field=models.ForeignKey(related_name='duplicates', to='api.Person'),
        ),
        migrations.AlterField(
            model_name='duplicatesong',
            name='parent',
            field=models.ForeignKey(related_name='duplicates', to='api.Song'),
        ),
    ]
