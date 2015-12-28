# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0060_auto_20151222_1037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='kind',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='level',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='organization',
        ),
    ]
