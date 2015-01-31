# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0060_contest_scoresheet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='contestant',
        ),
        migrations.RemoveField(
            model_name='note',
            name='profile',
        ),
        migrations.DeleteModel(
            name='Note',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
