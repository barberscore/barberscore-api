# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0065_auto_20151025_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='duplicategroup',
            name='child',
        ),
        migrations.RemoveField(
            model_name='duplicategroup',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='duplicateperson',
            name='child',
        ),
        migrations.RemoveField(
            model_name='duplicateperson',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='duplicatesong',
            name='child',
        ),
        migrations.RemoveField(
            model_name='duplicatesong',
            name='parent',
        ),
        migrations.DeleteModel(
            name='DuplicateGroup',
        ),
        migrations.DeleteModel(
            name='DuplicatePerson',
        ),
        migrations.DeleteModel(
            name='DuplicateSong',
        ),
    ]
