# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20150501_1506'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupmember',
            name='contest',
        ),
        migrations.RemoveField(
            model_name='groupmember',
            name='group',
        ),
        migrations.RemoveField(
            model_name='groupmember',
            name='singer',
        ),
        migrations.RemoveField(
            model_name='group',
            name='members',
        ),
        migrations.DeleteModel(
            name='GroupMember',
        ),
    ]
