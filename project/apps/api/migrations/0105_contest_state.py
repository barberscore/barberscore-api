# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0104_auto_20151109_0814'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='state',
            field=django_fsm.FSMIntegerField(default=0),
        ),
    ]
