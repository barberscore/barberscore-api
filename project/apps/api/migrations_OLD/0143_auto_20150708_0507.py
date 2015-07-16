# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0142_auto_20150708_0504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupaward',
            name='award',
        ),
        migrations.RemoveField(
            model_name='groupaward',
            name='contest',
        ),
        migrations.RemoveField(
            model_name='groupaward',
            name='group',
        ),
        migrations.RemoveField(
            model_name='group',
            name='awards',
        ),
        migrations.DeleteModel(
            name='Award',
        ),
        migrations.DeleteModel(
            name='GroupAward',
        ),
    ]
