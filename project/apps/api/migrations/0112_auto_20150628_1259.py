# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0111_auto_20150627_2053'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='song',
            options={'ordering': ['name']},
        ),
    ]
