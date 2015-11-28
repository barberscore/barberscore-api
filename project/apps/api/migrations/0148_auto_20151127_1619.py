# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0147_auto_20151126_0615'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='winner',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='winner',
            name='award',
        ),
        migrations.RemoveField(
            model_name='winner',
            name='contest',
        ),
        migrations.RemoveField(
            model_name='winner',
            name='contestant',
        ),
        migrations.DeleteModel(
            name='Winner',
        ),
    ]
