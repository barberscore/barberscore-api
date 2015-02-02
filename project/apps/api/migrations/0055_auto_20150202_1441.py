# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0054_auto_20150202_1431'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contest',
            old_name='csv_f1',
            new_name='csv_finals',
        ),
        migrations.RenameField(
            model_name='contest',
            old_name='csv_q1',
            new_name='csv_quarters',
        ),
        migrations.RenameField(
            model_name='contest',
            old_name='csv_q2',
            new_name='csv_semis',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='csv_q3',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='csv_s1',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='csv_s2',
        ),
    ]
