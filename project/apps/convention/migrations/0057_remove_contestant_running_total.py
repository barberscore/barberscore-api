# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0056_auto_20140705_1310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contestant',
            name='running_total',
        ),
    ]
