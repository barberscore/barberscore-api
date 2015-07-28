# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_auto_20150728_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duplicategroup',
            name='child',
            field=models.ForeignKey(related_name='duplicates', to='api.Group'),
        ),
        migrations.AlterField(
            model_name='duplicategroup',
            name='parent',
            field=models.ForeignKey(to='api.Group'),
        ),
    ]
