# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_auto_20150128_2010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quartetmembers',
            name='contest',
        ),
        migrations.RemoveField(
            model_name='quartetmembers',
            name='quartet',
        ),
        migrations.RemoveField(
            model_name='quartetmembers',
            name='singer',
        ),
        migrations.RemoveField(
            model_name='quartet',
            name='members',
        ),
        migrations.DeleteModel(
            name='QuartetMembers',
        ),
    ]
