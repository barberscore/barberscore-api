# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0043_auto_20150512_0848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chorus',
            name='group_ptr',
        ),
        migrations.RemoveField(
            model_name='quartet',
            name='baritone',
        ),
        migrations.RemoveField(
            model_name='quartet',
            name='bass',
        ),
        migrations.RemoveField(
            model_name='quartet',
            name='group_ptr',
        ),
        migrations.RemoveField(
            model_name='quartet',
            name='lead',
        ),
        migrations.RemoveField(
            model_name='quartet',
            name='tenor',
        ),
        migrations.DeleteModel(
            name='Chorus',
        ),
        migrations.DeleteModel(
            name='Quartet',
        ),
    ]
