# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0101_judge_status_monitor'),
    ]

    operations = [
        migrations.RenameModel('Judge', 'Panelist'),
    ]
