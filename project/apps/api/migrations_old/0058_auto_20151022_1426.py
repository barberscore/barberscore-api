# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0057_score_status_monitor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='score',
            options={'ordering': ('judge', 'performance__order')},
        ),
    ]
