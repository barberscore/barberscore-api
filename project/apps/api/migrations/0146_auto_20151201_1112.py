# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0145_auto_20151201_1110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='award',
            name='contest',
        ),
        migrations.DeleteModel(
            name='Award',
        ),
    ]
